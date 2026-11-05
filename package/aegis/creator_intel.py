"""AegisBrain Creator Intelligence, Cultural Memory & Community Radar.

Maintains:
1. Creator Profile Knowledge Graph: Tracks creators from user links, their niches,
   typical stacks, and linked repositories.
2. Proactive Content Discovery: Scrapes tracked creators and tech subreddits (r/LocalLLaMA,
   r/MachineLearning, r/ClaudeAI, r/programming) so the agent possesses fresh context before you even ask.
3. Nerd Culture & Meme Lexicon: Deep dictionary of developer jokes, memes ("I use Arch btw",
   "vibe coding", "GPU poor", "p(doom)", "e/acc", "slop"), hacker slang, and nuances.
"""

from __future__ import annotations

import json
import logging
import re
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from aegis.browser import fetch_url_content
from aegis.db import get_connection

logger = logging.getLogger(__name__)

# Pre-seeded Hacker & Developer Culture Lexicon
NERD_LEXICON: Dict[str, Dict[str, str]] = {
    "i use arch btw": {
        "meaning": "The ultimate Linux DIY flex. Indicates pride in minimal, non-bloated, user-configured systems.",
        "context": "Used jokingly whenever someone showcases extreme customization, terminal minimalism, or hatred of Windows/macOS telemetry.",
        "vibe": "Elite tinkerer / hacker ethos."
    },
    "vibe coding": {
        "meaning": "Andrej Karpathy's term for programming entirely via conversational prompts with AI agents (Claude, Cursor, Gemini), guiding the architecture while letting the LLM write the diffs.",
        "context": "Focuses on intent and test verification rather than typing syntax.",
        "vibe": "Post-syntax AI engineering."
    },
    "slop": {
        "meaning": "Low-quality, unchecked, generic boilerplate spit out by AI models without human review or testing.",
        "context": "AegisBrain's 4-stage pipeline is specifically engineered to strip AI slop.",
        "vibe": "Critical quality filter."
    },
    "gpu poor": {
        "meaning": "Developers, indie hackers, and researchers running local quantized models (GGUF, Ollama) on consumer hardware (e.g. RTX 3050/3060) without million-dollar H100 clusters.",
        "context": "Relatable badge of honor for engineers who optimize model size, RAM headroom, and quantization.",
        "vibe": "Resourceful optimization."
    },
    "e/acc": {
        "meaning": "Effective Accelerationism. A movement advocating for accelerating technological and AI compute progress without artificial regulatory slowing.",
        "context": "Often contrasted with decels (decelerationists) or doomers.",
        "vibe": "Techno-optimist builder culture."
    },
    "p(doom)": {
        "meaning": "Probability of Doom: subjective statistical probability that superintelligent AI leads to existential catastrophe for humanity.",
        "context": "Common discussion topic among safety researchers, YC founders, and frontier labs.",
        "vibe": "AI safety calibration."
    },
    "skill issue": {
        "meaning": "Playful internet/gaming dismissive response implying the issue is caused by the operator's technique rather than system flaws.",
        "context": "Used lightheartedly in tech chats when someone complains about a tool.",
        "vibe": "Hacker banter."
    },
    "poka-yoke": {
        "meaning": "Mistake-proofing (Japanese manufacturing / Toyota Production System). Designing interfaces or systems so mistakes are physically or logically impossible.",
        "context": "Applied to software design (e.g., restore-point safety reflexes before running dangerous commands).",
        "vibe": "Robust defensive engineering."
    },
    "yak shaving": {
        "meaning": "Doing a chain of seemingly unrelated trivial tasks just to complete a primary goal (e.g. updating python to run pip to install a tool to fix a script).",
        "context": "Every developer's daily experience when configuring dev environments.",
        "vibe": "Relatable software friction."
    },
    "bikeshedding": {
        "meaning": "Parkinson's Law of Triviality: spending hours arguing over simple, minor details (like the color of a bike shed) while ignoring critical complex architecture.",
        "context": "Avoided in AegisBrain through the Karpathy surgical changes rule.",
        "vibe": "Anti-overengineering warning."
    },
    "karpathy guidelines": {
        "meaning": "Core principles of AI-assisted engineering: surgical changes, minimal code, zero speculation, goal-driven test verification.",
        "context": "Active system rule in AegisBrain.",
        "vibe": "Top-tier AI engineering standard."
    },
    "claude code / cursor rules": {
        "meaning": "Declarative steerability documents (.cursorrules, AGENTS.md, CLAUDE.md) instructing agents on architectural constraints and project patterns.",
        "context": "The foundation of agentic software development in 2026.",
        "vibe": "Agent steering."
    }
}


@dataclass
class CreatorProfile:
    handle: str
    platform: str
    name: str = ""
    niche: str = "general_tech"
    quality_score: float = 8.5
    videos_count: int = 1
    topics: List[str] = field(default_factory=list)
    sample_links: List[str] = field(default_factory=list)
    bio_links: List[str] = field(default_factory=list)
    last_seen: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def init_creator_tables() -> None:
    """Ensure creator intelligence tables exist in SQLite."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tracked_creators (
                handle TEXT PRIMARY KEY,
                platform TEXT NOT NULL,
                name TEXT,
                niche TEXT,
                quality_score REAL DEFAULT 8.0,
                videos_count INTEGER DEFAULT 1,
                topics TEXT,
                sample_links TEXT,
                bio_links TEXT,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS community_trends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                score INTEGER DEFAULT 0,
                summary TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)


def track_creator(
    handle: str,
    platform: str,
    title: str = "",
    topics: Optional[List[str]] = None,
    link: str = "",
    bio_links: Optional[List[str]] = None,
) -> CreatorProfile:
    """Register or update a content creator into the user's taste graph."""
    init_creator_tables()
    h = handle.replace("@", "").strip().lower()
    if not h:
        h = "unknown_creator"

    topics = topics or []
    bio_links = bio_links or []

    with get_connection() as conn:
        row = conn.execute("SELECT * FROM tracked_creators WHERE handle = ?", (h,)).fetchone()
        if row:
            existing_topics = json.loads(row["topics"] or "[]")
            for t in topics:
                if t not in existing_topics:
                    existing_topics.append(t)

            existing_links = json.loads(row["sample_links"] or "[]")
            if link and link not in existing_links:
                existing_links.append(link)

            existing_bio = json.loads(row["bio_links"] or "[]")
            for b in bio_links:
                if b not in existing_bio:
                    existing_bio.append(b)

            v_count = row["videos_count"] + 1

            conn.execute("""
                UPDATE tracked_creators
                SET videos_count = ?, topics = ?, sample_links = ?, bio_links = ?, last_seen = CURRENT_TIMESTAMP
                WHERE handle = ?
            """, (v_count, json.dumps(existing_topics), json.dumps(existing_links[:10]), json.dumps(existing_bio[:10]), h))

            return CreatorProfile(
                handle=h,
                platform=platform,
                name=row["name"] or h,
                niche=row["niche"] or "tech",
                quality_score=row["quality_score"],
                videos_count=v_count,
                topics=existing_topics,
                sample_links=existing_links,
                bio_links=existing_bio,
            )
        else:
            conn.execute("""
                INSERT INTO tracked_creators (handle, platform, name, niche, quality_score, videos_count, topics, sample_links, bio_links)
                VALUES (?, ?, ?, ?, ?, 1, ?, ?, ?)
            """, (h, platform, h, "ai_and_software", 8.5, json.dumps(topics), json.dumps([link] if link else []), json.dumps(bio_links)))

            return CreatorProfile(
                handle=h,
                platform=platform,
                name=h,
                niche="ai_and_software",
                quality_score=8.5,
                videos_count=1,
                topics=topics,
                sample_links=[link] if link else [],
                bio_links=bio_links,
            )


def get_all_tracked_creators(limit: int = 50) -> List[CreatorProfile]:
    """Retrieve all tracked creators in user profile."""
    init_creator_tables()
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM tracked_creators ORDER BY videos_count DESC, last_seen DESC LIMIT ?", (limit,)).fetchall()
        profiles = []
        for r in rows:
            profiles.append(CreatorProfile(
                handle=r["handle"],
                platform=r["platform"],
                name=r["name"] or r["handle"],
                niche=r["niche"],
                quality_score=r["quality_score"],
                videos_count=r["videos_count"],
                topics=json.loads(r["topics"] or "[]"),
                sample_links=json.loads(r["sample_links"] or "[]"),
                bio_links=json.loads(r["bio_links"] or "[]"),
                last_seen=str(r["last_seen"]),
            ))
        return profiles


def detect_cultural_references(text: str) -> List[Dict[str, str]]:
    """Scan transcript or user text for developer memes, slang, and cultural jokes."""
    found = []
    text_lower = text.lower()
    for term, data in NERD_LEXICON.items():
        if term in text_lower:
            found.append({
                "term": term,
                "meaning": data["meaning"],
                "context": data["context"],
                "vibe": data["vibe"]
            })
    return found


def scrape_tech_subreddit(subreddit: str = "LocalLLaMA", limit: int = 5) -> List[Dict[str, Any]]:
    """Fetch top trending developer discussions from Reddit directly."""
    init_creator_tables()
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 AegisBrainRadar/1.0"},
    )
    trends = []
    try:
        with urllib.request.urlopen(req, timeout=6.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            children = data.get("data", {}).get("children", [])
            with get_connection() as conn:
                for item in children:
                    d = item.get("data", {})
                    title = d.get("title", "")
                    permalink = f"https://reddit.com{d.get('permalink', '')}"
                    score = d.get("score", 0)
                    selftext = d.get("selftext", "")[:400]
                    t_item = {
                        "source": f"r/{subreddit}",
                        "title": title,
                        "url": permalink,
                        "score": score,
                        "summary": selftext,
                    }
                    trends.append(t_item)
                    conn.execute("""
                        INSERT INTO community_trends (source, title, url, score, summary)
                        VALUES (?, ?, ?, ?, ?)
                    """, (f"r/{subreddit}", title, permalink, score, selftext))
    except Exception as e:
        logger.debug("Failed scraping r/%s: %s", subreddit, e)

    return trends


def scrape_hacker_news(limit: int = 5) -> List[Dict[str, Any]]:
    """Fetch top trending engineering & startup discussions from Hacker News."""
    init_creator_tables()
    trends = []
    try:
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        req = urllib.request.Request(url, headers={"User-Agent": "AegisBrain/1.0"})
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            ids = json.loads(resp.read().decode("utf-8"))[:limit]

        with get_connection() as conn:
            for item_id in ids:
                item_url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
                req_item = urllib.request.Request(item_url, headers={"User-Agent": "AegisBrain/1.0"})
                with urllib.request.urlopen(req_item, timeout=4.0) as item_resp:
                    data = json.loads(item_resp.read().decode("utf-8"))
                    title = data.get("title", "")
                    target_url = data.get("url") or f"https://news.ycombinator.com/item?id={item_id}"
                    score = data.get("score", 0)
                    summary = f"By {data.get('by', 'anon')} &bull; {data.get('descendants', 0)} comments"
                    t_item = {
                        "source": "HackerNews",
                        "title": title,
                        "url": target_url,
                        "score": score,
                        "summary": summary,
                    }
                    trends.append(t_item)
                    conn.execute("""
                        INSERT INTO community_trends (source, title, url, score, summary)
                        VALUES (?, ?, ?, ?, ?)
                    """, ("HackerNews", title, target_url, score, summary))
    except Exception as e:
        logger.debug("Failed scraping HackerNews: %s", e)
    return trends


def get_recent_trends(limit: int = 5) -> List[Dict[str, Any]]:
    """Retrieve recent community and tech trends from database, or fallback to scrape."""
    init_creator_tables()
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM community_trends ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        if rows:
            return [dict(r) for r in rows]
    try:
        return scrape_hacker_news(limit=limit)
    except Exception:
        return []


def radar_sweep() -> Dict[str, Any]:
    """Execute community & creator radar sweep across tracked niches."""
    creators = get_all_tracked_creators(limit=10)
    trends = scrape_hacker_news(limit=5)

    return {
        "tracked_creators_count": len(creators),
        "recent_creators": [asdict(c) for c in creators[:5]],
        "fresh_community_trends": trends,
        "lexicon_terms_indexed": len(NERD_LEXICON),
    }
