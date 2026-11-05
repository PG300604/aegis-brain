"""AegisBrain Lightweight Telegram Asynchronous Queue & Idle Ingestion Worker.

Eliminates manual copy-pasting of reels/posts from phone to PC.
1. When on mobile: share any Instagram Reel, Reddit thread, X post, or link to your personal Telegram Bot.
2. Telegram stores incoming messages on its server regardless of whether your PC is online or offline.
3. When AegisBrain is running:
   - Polls updates from the bot into the local SQLite `telegram_inbox` queue.
   - Monitors system activity via zero-dependency CPU & lock checks (`is_system_idle()`).
   - Only processes pending links when the machine and agent are completely idle.
   - Ingests media via `SensoryPipeline`, tracks creator intel, and replies with a concise <300 token summary.
"""

from __future__ import annotations

import ctypes
import json
import logging
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from aegis.config import get_aegis_dir
from aegis.db import get_connection, init_db

logger = logging.getLogger(__name__)

URL_REGEX = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)

HEAVY_PROCESS_NAMES = {
    "ninja.exe", "cargo.exe", "rustc.exe", "cl.exe", "link.exe",
    "pytest.exe", "ffmpeg.exe", "whisper.exe", "devenv.exe", "cmake.exe"
}


def get_config_path() -> Path:
    return get_aegis_dir() / "config.json"


def get_telegram_token() -> Optional[str]:
    """Retrieve Telegram Bot Token from environment variable, remote.json, or config.json."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if token:
        return token.strip()
    
    # 1. Check ~/.aegis-brain/remote.json (Primary remote config)
    remote_cfg = get_aegis_dir() / "remote.json"
    if remote_cfg.exists():
        try:
            with open(remote_cfg, "r", encoding="utf-8") as f:
                data = json.load(f)
                tok = data.get("telegram_token") or data.get("telegram_bot_token")
                if tok:
                    return tok.strip()
        except Exception:
            pass

    # 2. Check ~/.aegis-brain/config.json
    cfg_file = get_config_path()
    if cfg_file.exists():
        try:
            with open(cfg_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                tok = data.get("telegram_bot_token") or data.get("telegram_token")
                if tok:
                    return tok.strip()
        except Exception as e:
            logger.warning("Failed to read aegis config: %s", e)
    return None


def set_telegram_token(token: str) -> None:
    """Store Telegram Bot Token in ~/.aegis/config.json."""
    cfg_file = get_config_path()
    cfg_file.parent.mkdir(parents=True, exist_ok=True)
    data: Dict[str, Any] = {}
    if cfg_file.exists():
        try:
            with open(cfg_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}
    data["telegram_bot_token"] = token.strip()
    with open(cfg_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


class FILETIME(ctypes.Structure):
    _fields_ = [("dwLowDateTime", ctypes.c_uint32), ("dwHighDateTime", ctypes.c_uint32)]


def _filetime_to_int(ft: FILETIME) -> int:
    return (ft.dwHighDateTime << 32) | ft.dwLowDateTime


def get_cpu_usage_sample(sample_duration: float = 0.15) -> float:
    """Measure instantaneous CPU usage percentage without third-party dependencies."""
    if sys.platform == "win32":
        try:
            kernel32 = ctypes.windll.kernel32
            idle1, kernel1, user1 = FILETIME(), FILETIME(), FILETIME()
            if not kernel32.GetSystemTimes(ctypes.byref(idle1), ctypes.byref(kernel1), ctypes.byref(user1)):
                return 0.0
            time.sleep(sample_duration)
            idle2, kernel2, user2 = FILETIME(), FILETIME(), FILETIME()
            if not kernel32.GetSystemTimes(ctypes.byref(idle2), ctypes.byref(kernel2), ctypes.byref(user2)):
                return 0.0

            idle_diff = _filetime_to_int(idle2) - _filetime_to_int(idle1)
            kernel_diff = _filetime_to_int(kernel2) - _filetime_to_int(kernel1)
            user_diff = _filetime_to_int(user2) - _filetime_to_int(user1)
            total = kernel_diff + user_diff
            if total <= 0:
                return 0.0
            return max(0.0, min(100.0, (1.0 - (idle_diff / total)) * 100.0))
        except Exception:
            return 0.0
    else:
        try:
            load = os.getloadavg()[0]
            cores = os.cpu_count() or 1
            return min(100.0, (load / cores) * 100.0)
        except Exception:
            return 0.0


def is_system_idle(cpu_threshold: float = 35.0) -> Tuple[bool, str]:
    """Determine whether the local machine and agent are idle.
    
    Checks:
    1. Active lock file (~/.aegis/busy.lock).
    2. CPU load < cpu_threshold.
    """
    lock_file = get_aegis_dir() / "busy.lock"
    if lock_file.exists():
        return False, "Agent busy lock file exists (~/.aegis/busy.lock)"

    cpu_load = get_cpu_usage_sample(0.12)
    if cpu_load > cpu_threshold:
        return False, f"CPU usage is high ({cpu_load:.1f}% > {cpu_threshold:.1f}%)"

    return True, f"System is idle (CPU {cpu_load:.1f}%)"


class TelegramClient:
    """Zero-dependency Telegram Bot API client using standard urllib."""

    def __init__(self, token: Optional[str] = None):
        self.token = token or get_telegram_token()
        if not self.token:
            raise ValueError(
                "Telegram Bot Token not configured. Set TELEGRAM_BOT_TOKEN environment variable "
                "or run `aegis telegram setup <TOKEN>`."
            )
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def _request(self, endpoint: str, data: Optional[Dict[str, Any]] = None, timeout: int = 15) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint}"
        req_data = None
        headers = {"User-Agent": "AegisBrain/1.0 (Windows NT 10.0; Win64)"}
        if data is not None:
            req_data = json.dumps(data).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = urllib.request.Request(url, data=req_data, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8")
                res = json.loads(raw)
                if not res.get("ok"):
                    raise RuntimeError(f"Telegram API error: {res.get('description')}")
                return res
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            logger.error("Telegram API HTTP error: %s - %s", e.code, err_body)
            raise RuntimeError(f"Telegram API HTTP {e.code}: {err_body}") from e
        except Exception as e:
            logger.error("Telegram request failed: %s", e)
            raise

    def get_me(self) -> Dict[str, Any]:
        res = self._request("getMe")
        return res.get("result", {})

    def get_updates(self, offset: Optional[int] = None, limit: int = 100, timeout: int = 2) -> List[Dict[str, Any]]:
        payload: Dict[str, Any] = {"limit": limit, "timeout": timeout}
        if offset is not None:
            payload["offset"] = offset
        res = self._request("getUpdates", payload, timeout=timeout + 10)
        return res.get("result", [])

    def send_message(self, chat_id: Any, text: str, parse_mode: Optional[str] = "Markdown") -> Dict[str, Any]:
        payload: Dict[str, Any] = {"chat_id": chat_id, "text": text}
        if parse_mode:
            payload["parse_mode"] = parse_mode
        try:
            res = self._request("sendMessage", payload)
            return res.get("result", {})
        except Exception as e:
            # Fallback without markdown formatting in case text has special characters
            if parse_mode:
                payload.pop("parse_mode", None)
                return self._request("sendMessage", payload).get("result", {})
            raise e


class TelegramQueue:
    """Manages ingestion of mobile links into SQLite and drains them during idle periods."""

    def __init__(self, token: Optional[str] = None):
        self.token = token or get_telegram_token()
        init_db()

    def get_client(self) -> Optional[TelegramClient]:
        if not self.token:
            return None
        try:
            return TelegramClient(self.token)
        except Exception as e:
            logger.error("Failed to initialize Telegram client: %s", e)
            return None

    def poll(self) -> Tuple[int, int]:
        """Poll unread messages from Telegram and save to SQLite telegram_inbox.
        
        Returns (new_messages_queued, highest_update_id).
        """
        client = self.get_client()
        if not client:
            return 0, 0

        # Find highest update_id already in DB
        with get_connection() as conn:
            row = conn.execute("SELECT MAX(update_id) AS max_id FROM telegram_inbox").fetchone()
            max_id = row["max_id"] if row and row["max_id"] is not None else 0

        next_offset = max_id + 1 if max_id > 0 else None
        try:
            updates = client.get_updates(offset=next_offset, limit=100)
        except Exception as e:
            logger.warning("Error fetching updates from Telegram: %s", e)
            return 0, max_id

        if not updates:
            return 0, max_id

        queued_count = 0
        new_max_id = max_id

        with get_connection() as conn:
            for upd in updates:
                uid = upd.get("update_id", 0)
                if uid > new_max_id:
                    new_max_id = uid

                msg = upd.get("message") or upd.get("channel_post") or {}
                if not msg:
                    continue

                chat = msg.get("chat", {})
                chat_id = str(chat.get("id", ""))
                sender = msg.get("from", {})
                sender_username = sender.get("username", "")
                sender_name = f"{sender.get('first_name', '')} {sender.get('last_name', '')}".strip()
                message_id = msg.get("message_id", 0)

                # Collect text and caption (reels shared with caption)
                raw_text = msg.get("text") or msg.get("caption") or ""
                urls = URL_REGEX.findall(raw_text)

                # Skip duplicate update_id
                existing = conn.execute("SELECT id FROM telegram_inbox WHERE update_id = ?", (uid,)).fetchone()
                if existing:
                    continue

                conn.execute(
                    """
                    INSERT INTO telegram_inbox
                    (update_id, chat_id, sender_username, sender_name, message_id, text, extracted_urls, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')
                    """,
                    (
                        uid,
                        chat_id,
                        sender_username,
                        sender_name,
                        message_id,
                        raw_text,
                        json.dumps(urls)
                    )
                )
                queued_count += 1

        return queued_count, new_max_id

    def drain(
        self,
        idle_only: bool = True,
        max_items: int = 5,
        cpu_threshold: float = 35.0,
        reply_to_user: bool = True
    ) -> List[Dict[str, Any]]:
        """Process pending items in the queue when system is idle.
        
        Args:
            idle_only: If True, halts if system is currently active/busy.
            max_items: Number of queue items to process in one drain cycle.
            cpu_threshold: Max CPU percentage allowed to consider system idle.
            reply_to_user: Send confirmation message back to Telegram sender.
        """
        if idle_only:
            is_idle, reason = is_system_idle(cpu_threshold)
            if not is_idle:
                logger.info("TelegramQueue drain skipped: %s", reason)
                return []

        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT id, update_id, chat_id, sender_name, text, extracted_urls
                FROM telegram_inbox
                WHERE status = 'pending'
                ORDER BY id ASC
                LIMIT ?
                """,
                (max_items,)
            ).fetchall()

        if not rows:
            return []

        processed_items: List[Dict[str, Any]] = []
        client = self.get_client()

        # Late import to prevent circular dependency
        from aegis.sensory import process_sensory_link

        for row in rows:
            item_id = row["id"]
            chat_id = row["chat_id"]
            urls: List[str] = json.loads(row["extracted_urls"] or "[]")
            text = row["text"] or ""

            # Mark as processing
            with get_connection() as conn:
                conn.execute("UPDATE telegram_inbox SET status = 'processing' WHERE id = ?", (item_id,))

            results_for_item: List[Dict[str, Any]] = []
            summaries: List[str] = []

            try:
                if urls:
                    for url in urls:
                        logger.info("Processing queued URL: %s", url)
                        result = process_sensory_link(url)
                        results_for_item.append(result)

                        art = result.get("artifact", {})
                        analysis = result.get("analysis", {})
                        yc = analysis.get("yc_ceo_feasibility", {})

                        # Build ultra-lightweight summary (<150 tokens)
                        title = art.get("title", "Video")
                        creator_tag = f"@{art.get('author', 'creator')}"
                        score_tag = f"{yc.get('feasibility_score', 'N/A')}/10"
                        res_urls = art.get("gated_resource_urls", [])
                        res_tag = f"\n🔗 Gated Resource: {res_urls[0]}" if res_urls else ""
                        summary_text = analysis.get("summary", "")
                        summary_line = (
                            f"🎬 **{title[:60]}**\n"
                            f"👤 Creator: {creator_tag} | 📊 Feasibility: {score_tag}\n"
                            f"💡 Takeaway: {summary_text[:140]}...{res_tag}"
                        )
                        summaries.append(summary_line)
                else:
                    summaries.append(f"📝 Note ingested: {text[:120]}")

                final_summary = "\n\n".join(summaries)

                # Send reply to Telegram
                if reply_to_user and client and chat_id:
                    reply_text = f"🛡️ **AegisBrain Ingested:**\n\n{final_summary}"
                    try:
                        client.send_message(chat_id, reply_text)
                    except Exception as e:
                        logger.warning("Could not send Telegram confirmation: %s", e)

                # Mark completed
                now_iso = datetime.now(timezone.utc).isoformat()
                with get_connection() as conn:
                    conn.execute(
                        """
                        UPDATE telegram_inbox
                        SET status = 'completed', processed_at = ?, result_summary = ?
                        WHERE id = ?
                        """,
                        (now_iso, final_summary, item_id)
                    )

                processed_items.append({
                    "id": item_id,
                    "urls": urls,
                    "summary": final_summary,
                    "status": "completed"
                })

            except Exception as e:
                logger.error("Failed processing item #%s: %s", item_id, e)
                with get_connection() as conn:
                    conn.execute(
                        "UPDATE telegram_inbox SET status = 'failed', result_summary = ? WHERE id = ?",
                        (str(e), item_id)
                    )

        return processed_items

    def status(self) -> Dict[str, Any]:
        """Return status metrics for the Telegram queue."""
        with get_connection() as conn:
            pending = conn.execute("SELECT COUNT(*) AS c FROM telegram_inbox WHERE status = 'pending'").fetchone()["c"]
            completed = conn.execute("SELECT COUNT(*) AS c FROM telegram_inbox WHERE status = 'completed'").fetchone()["c"]
            failed = conn.execute("SELECT COUNT(*) AS c FROM telegram_inbox WHERE status = 'failed'").fetchone()["c"]
            total = conn.execute("SELECT COUNT(*) AS c FROM telegram_inbox").fetchone()["c"]

        idle, idle_reason = is_system_idle()
        bot_info = None
        client = self.get_client()
        if client:
            try:
                me = client.get_me()
                bot_info = f"@{me.get('username', 'bot')} ({me.get('first_name', '')})"
            except Exception as e:
                bot_info = f"Token error: {e}"

        return {
            "bot": bot_info or "Not configured",
            "system_idle": idle,
            "idle_reason": idle_reason,
            "pending": pending,
            "completed": completed,
            "failed": failed,
            "total": total
        }
