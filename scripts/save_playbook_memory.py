import sqlite3
from pathlib import Path
import time

db_path = Path.home() / ".aegis" / "brain.db"
if db_path.exists():
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    # Check tables
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r[0] for r in cur.fetchall()]
    print("Tables:", tables)
    # Check if memories table exists
    if "memories" in tables:
        topic = "video_production_playbook"
        content = (
            "Deep-Tech Product Demo Video Production Playbook: "
            "Architecture combines Explainroo (editorial title cards, monospace telemetry), "
            "Huashu Art Motion Y2 Vox (continuous easing zooms, fx=600 anchor preventing left margin text crop, "
            "targeted fy focal action tracking for prompt typing, worker synthesis, and pytest pass results), "
            "and Active Word-by-Word Focus Captions (ASS format with {\\c&H0020E0FF\\b1} active word glow on charcoal pill). "
            "Full playbook documented in docs/guides/video_production_playbook.md."
        )
        cur.execute(
            "INSERT INTO memories (category, key, content, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            ("guide", topic, content, int(time.time()), int(time.time()))
        )
        conn.commit()
        print("Successfully saved playbook to AegisBrain neural memory bus!")
    conn.close()
