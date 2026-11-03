"""AegisBrain Media Generation Bridge.

Integrates with OpenHiggsfield (https://github.com/wide-trace/open-higgsfield)
to generate AI imagery and videos while cataloging prompts, seeds, and asset
URIs in the local neural memory bus.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

from aegis.config import get_current_mode
from aegis.db import record_decision


DEFAULT_HF_API_URL = "https://api.higgsfield.ai"


def generate_media(
    model: str,
    prompt: str,
    aspect_ratio: str = "16:9",
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    record_decision: bool = True,
) -> Dict[str, Any]:
    """Dispatch a media generation request to OpenHiggsfield / Higgsfield API.

    Zero external dependencies - uses standard library urllib.
    """
    key = api_key or os.getenv("HF_API_KEY") or os.getenv("OPEN_HIGGSFIELD_API_KEY")
    url = (base_url or os.getenv("HF_API_BASE_URL") or DEFAULT_HF_API_URL).rstrip("/")

    payload = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
    }

    if not key:
        # Dry-run or local fallback mode when key is absent
        mock_result = {
            "status": "simulated",
            "model": model,
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "message": "Set HF_API_KEY (id:secret) or OPEN_HIGGSFIELD_API_KEY to execute live model dispatch.",
        }
        if record_decision and get_current_mode() != "private":
            _record_media_asset(model, prompt, "simulated", mock_result)
        return mock_result

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Key {key}",
    }

    req = urllib.request.Request(
        f"{url}/{model}",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        return {"status": "error", "code": exc.code, "error": err_body}
    except Exception as exc:
        return {"status": "error", "error": str(exc)}

    req_id = data.get("request_id") or data.get("id")
    status_url = data.get("status_url") or f"{url}/requests/{req_id}/status"

    # Poll status until terminal
    result = _poll_status(status_url, headers)

    if record_decision and get_current_mode() != "private":
        _record_media_asset(model, prompt, result.get("status", "unknown"), result)

    return result


def _poll_status(status_url: str, headers: Dict[str, str], timeout_sec: int = 120) -> Dict[str, Any]:
    """Poll generation status until completed or failed."""
    start = time.time()
    while time.time() - start < timeout_sec:
        req = urllib.request.Request(status_url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                status = data.get("status")
                if status in ("completed", "failed", "nsfw", "canceled"):
                    return data
        except Exception:
            pass
        time.sleep(3)
    return {"status": "timeout", "message": "Generation polling exceeded timeout."}


def _record_media_asset(model: str, prompt: str, status: str, details: Dict[str, Any]) -> None:
    """Store generated asset metadata in AegisBrain SQLite memory bus."""
    record_decision(
        category="MEDIA",
        title=f"Generated Media Asset [{model}]",
        decision=f"Prompt: {prompt}\nStatus: {status}",
        rationale=json.dumps(details),
        tags=["media", "open-higgsfield", model, status],
    )
