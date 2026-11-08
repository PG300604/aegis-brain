import sqlite3
import os
import re
import json
import shutil
from pathlib import Path
from contextlib import contextmanager
from typing import Optional, Union, Dict, Any, List

# Core Invariants
CORE_NATIVE_SKILLS = {
    "andrej-karpathy-skills",
    "artemis",
    "ponytail",
    "diagram-design",
    "superpowers",
    "ecc",
    "aegis",
    "unslop-master",
    "unslop",
}

def is_core_skill(name: str) -> bool:
    return name.strip().lower() in CORE_NATIVE_SKILLS

def get_armory_dir() -> Path:
    env_path = os.environ.get("AEGIS_ARMORY_DIR")
    if env_path:
        p = Path(env_path)
    else:
        p = Path.home() / ".aegis-brain" / "armory"
    p.mkdir(parents=True, exist_ok=True)
    (p / ".quarantine").mkdir(parents=True, exist_ok=True)
    return p

@contextmanager
def get_armory_connection(conn: Optional[sqlite3.Connection] = None, db_path: Optional[Path] = None):
    if conn is not None:
        yield conn
    else:
        path = db_path or (get_armory_dir() / "armory.db")
        path.parent.mkdir(parents=True, exist_ok=True)
        c = sqlite3.connect(str(path))
        c.row_factory = sqlite3.Row
        try:
            yield c
        finally:
            c.close()

def init_armory_db(conn: Optional[sqlite3.Connection] = None, db_path: Optional[Path] = None) -> None:
    with get_armory_connection(conn, db_path) as c:
        c.execute('''
            CREATE TABLE IF NOT EXISTS armory_skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                path TEXT NOT NULL,
                source TEXT DEFAULT 'native',
                status TEXT DEFAULT 'active',
                security_score INTEGER DEFAULT 100,
                tags TEXT DEFAULT '',
                manifest_json TEXT DEFAULT '{}',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        c.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS armory_fts USING fts5(
                name,
                description,
                tags,
                category,
                content='armory_skills',
                content_rowid='id'
            );
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS armory_miner_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_url TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed_at TIMESTAMP,
                log TEXT DEFAULT ''
            );
        ''')
        c.execute('''
            CREATE TRIGGER IF NOT EXISTS armory_skills_ai AFTER INSERT ON armory_skills BEGIN
                INSERT INTO armory_fts(rowid, name, description, tags, category)
                VALUES (new.id, new.name, new.description, new.tags, new.category);
            END;
        ''')
        c.execute('''
            CREATE TRIGGER IF NOT EXISTS armory_skills_ad AFTER DELETE ON armory_skills BEGIN
                INSERT INTO armory_fts(armory_fts, rowid, name, description, tags, category)
                VALUES('delete', old.id, old.name, old.description, old.tags, old.category);
            END;
        ''')
        c.execute('''
            CREATE TRIGGER IF NOT EXISTS armory_skills_au AFTER UPDATE ON armory_skills BEGIN
                INSERT INTO armory_fts(armory_fts, rowid, name, description, tags, category)
                VALUES('delete', old.id, old.name, old.description, old.tags, old.category);
                INSERT INTO armory_fts(rowid, name, description, tags, category)
                VALUES (new.id, new.name, new.description, new.tags, new.category);
            END;
        ''')
        c.commit()

def evaluate_skill_security(content_or_path: Union[str, Path]) -> Dict[str, Any]:
    content = ""
    if isinstance(content_or_path, Path):
        try:
            content = content_or_path.read_text(encoding='utf-8')
        except Exception as e:
            return {
                "passed": False,
                "score": 0,
                "gates": {"structure": False, "prompt_defense": False, "shell_security": False, "secret_leak": False},
                "violations": [f"File read error: {e}"]
            }
    elif isinstance(content_or_path, str):
        content = content_or_path

    violations = []
    # Gate 1: Structure & Syntax
    g1_passed = len(content) >= 10 and '\x00' not in content
    if not g1_passed:
        violations.append("Structure_Too_Short_Or_NullByte")

    # Gate 2: Prompt Defense
    injection_patterns = [
        r"ignore previous instructions",
        r"ignore all prior instructions",
        r"system override",
        r"bypass rules",
        r"developer mode",
        r"jailbreak",
        r"exfiltrate",
    ]
    g2_passed = not any(re.search(p, content, re.IGNORECASE) for p in injection_patterns)
    if not g2_passed:
        violations.append("Prompt_Injection")

    # Gate 3: Red-Team Shell Security
    shell_patterns = [
        r"rm -rf /",
        r"mkfs",
        r"format ",
        r"curl .* \| bash",
        r"powershell -enc",
        r"nc -e",
        r"reverse shell",
    ]
    g3_passed = not any(re.search(p, content, re.IGNORECASE) for p in shell_patterns)
    if not g3_passed:
        violations.append("Shell_Injection")

    # Gate 4: Secret Leaks
    secret_patterns = [
        r"AKIA[0-9A-Z]{16}",
        r"ghp_[a-zA-Z0-9]{36}",
        r"sk-[a-zA-Z0-9]{20,}",
        r"-----BEGIN .*PRIVATE KEY-----",
    ]
    g4_passed = not any(re.search(p, content) for p in secret_patterns)
    if not g4_passed:
        violations.append("Secret_Leak")

    violation_count = len(violations)
    score = max(0, 100 - (25 * violation_count))
    passed = (violation_count == 0 and score >= 80)

    return {
        "passed": passed,
        "score": score,
        "gates": {
            "structure": g1_passed,
            "prompt_defense": g2_passed,
            "shell_security": g3_passed,
            "secret_leak": g4_passed,
        },
        "violations": violations,
    }

def register_skill(
    name: str,
    description: str = "",
    category: str = "general",
    content: str = "",
    source: str = "native",
    tags: Optional[str] = None,
    armory_dir: Optional[Path] = None,
    conn: Optional[sqlite3.Connection] = None,
) -> Dict[str, Any]:
    armory_root = armory_dir or get_armory_dir()
    if re.search(r"\.\./|\/|\\", name) or not re.fullmatch(r"[a-zA-Z0-9_-]+", name):
        raise ValueError(f"invalid name: {name}")

    if not description:
        m = re.search(r"description:\s*([^\n]+)", content, re.IGNORECASE)
        if m:
            description = m.group(1).strip()
    if category == "general":
        m = re.search(r"category:\s*([^\n]+)", content, re.IGNORECASE)
        if m:
            category = m.group(1).strip()
    if not tags:
        m = re.search(r"tags:\s*([^\n]+)", content, re.IGNORECASE)
        if m:
            tags = m.group(1).strip()

    security_result = evaluate_skill_security(content)
    if security_result["passed"]:
        status = "active"
        target_file = armory_root / name / "SKILL.md"
    else:
        status = "quarantined"
        target_file = armory_root / ".quarantine" / name / "SKILL.md"

    target_file.parent.mkdir(parents=True, exist_ok=True)
    target_file.write_text(content, encoding='utf-8')

    with get_armory_connection(conn, armory_root / "armory.db") as c:
        existing = c.execute("SELECT id FROM armory_skills WHERE name = ?", (name,)).fetchone()
        if existing:
            c.execute('''
                UPDATE armory_skills
                SET description=?, category=?, path=?, source=?, status=?, security_score=?, tags=?, manifest_json=?, updated_at=CURRENT_TIMESTAMP
                WHERE name=?
            ''', (description, category, str(target_file), source, status, security_result["score"], tags or "", json.dumps({}), name))
        else:
            c.execute('''
                INSERT INTO armory_skills (name, description, category, path, source, status, security_score, tags, manifest_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, description, category, str(target_file), source, status, security_result["score"], tags or "", json.dumps({})))
        c.commit()

    return {
        "name": name,
        "status": status,
        "path": str(target_file),
        "security_score": security_result["score"],
        "violations": security_result["violations"],
    }

def delete_skill(name: str, armory_dir: Optional[Path] = None, conn: Optional[sqlite3.Connection] = None) -> bool:
    if is_core_skill(name):
        raise ValueError(f"Core native skill '{name}' is protected and cannot be unmounted or deleted.")

    armory_root = armory_dir or get_armory_dir()
    skill_dir = armory_root / name
    if skill_dir.exists():
        if skill_dir.is_symlink():
            skill_dir.unlink()
        elif skill_dir.is_dir():
            shutil.rmtree(skill_dir)

    quarantine_dir = armory_root / ".quarantine" / name
    if quarantine_dir.exists():
        if quarantine_dir.is_symlink():
            quarantine_dir.unlink()
        elif quarantine_dir.is_dir():
            shutil.rmtree(quarantine_dir)

    with get_armory_connection(conn, armory_root / "armory.db") as c:
        c.execute("DELETE FROM armory_skills WHERE name=?", (name,))
        c.commit()
    return True

# Track active projection targets for seamless unmounting
_PROJECTIONS: Dict[tuple, Path] = {}

def project_skill(
    name: str,
    target_agent: Optional[str] = None,
    target_dir: Optional[Path] = None,
    armory_dir: Optional[Path] = None,
    conn: Optional[sqlite3.Connection] = None,
    target: Optional[str] = None,
    path: Optional[Path] = None,
) -> Dict[str, Any]:
    armory_root = armory_dir or get_armory_dir()
    target_agent = target or target_agent or "claude"
    target_root = path or target_dir or (Path.home() / ".aegis-brain" / target_agent)
    target_root.mkdir(parents=True, exist_ok=True)
    _PROJECTIONS[(name.lower(), target_agent.lower())] = target_root

    with get_armory_connection(conn, armory_root / "armory.db") as c:
        skill_data = c.execute("SELECT * FROM armory_skills WHERE name=?", (name,)).fetchone()
        if not skill_data:
            return {"name": name, "status": "not_found", "agent": target_agent, "target_path": "", "mode": "not_found"}

        skill_file = Path(skill_data['path'])

    agent_lower = target_agent.lower()
    if agent_lower in ('antigravity', 'claude'):
        dest_file = target_root / "SKILL.md"
        dest_dir = target_root / name
        try:
            shutil.copyfile(skill_file, dest_file)
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(skill_file, dest_dir / "SKILL.md")
            mode = "copy"
        except Exception as e:
            return {"name": name, "status": "error", "agent": target_agent, "target_path": str(target_root), "mode": f"failed: {e}"}

        return {"name": name, "agent": target_agent, "target_path": str(target_root), "mode": mode}

    elif agent_lower in ('hermes', 'opencode'):
        manifest = {
            "name": name,
            "description": skill_data["description"],
            "category": skill_data["category"],
            "path": str(skill_file),
            "tool_spec": {
                "name": name,
                "description": skill_data["description"],
            }
        }
        spec_json = json.dumps(manifest, indent=2)
        (target_root / "SKILL.json").write_text(spec_json, encoding='utf-8')
        (target_root / f"{name}.json").write_text(spec_json, encoding='utf-8')
        return {"name": name, "agent": target_agent, "target_path": str(target_root / "SKILL.json"), "mode": "json_spec"}

    return {"name": name, "status": "error", "agent": target_agent, "target_path": "", "mode": "unsupported_agent"}

def mount_skill(
    name: str,
    target_agent: Optional[str] = None,
    target_dir: Optional[Path] = None,
    armory_dir: Optional[Path] = None,
    conn: Optional[sqlite3.Connection] = None,
    target: Optional[str] = None,
    path: Optional[Path] = None,
) -> Dict[str, Any]:
    return project_skill(name, target_agent, target_dir, armory_dir, conn, target=target, path=path)

def unmount_skill(name: str, target_agent: str, target_dir: Optional[Path] = None) -> bool:
    if is_core_skill(name):
        raise ValueError(f"Core native skill '{name}' is protected and cannot be unmounted.")

    agent_lower = target_agent.lower()
    target_root = target_dir or _PROJECTIONS.get((name.lower(), agent_lower)) or (Path.home() / ".aegis-brain" / target_agent)

    if agent_lower in ('antigravity', 'claude'):
        if target_root.exists():
            if (target_root / "SKILL.md").exists() and target_root.name.endswith("_skills"):
                shutil.rmtree(target_root)
                return True
            for item in list(target_root.glob("*")):
                if item.name == name or item.name == "SKILL.md":
                    if item.is_file() or item.is_symlink():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
            return True
        return False

    elif agent_lower in ('hermes', 'opencode'):
        removed = False
        for fname in ("SKILL.json", f"{name}.json"):
            spec_file = target_root / fname
            if spec_file.exists():
                spec_file.unlink()
                removed = True
        return removed

    return False

def project_all_skills(
    target_agent: str = "claude",
    target_dir: Optional[Path] = None,
    armory_dir: Optional[Path] = None,
    conn: Optional[sqlite3.Connection] = None,
) -> List[str]:
    armory_root = armory_dir or get_armory_dir()
    with get_armory_connection(conn, armory_root / "armory.db") as c:
        rows = c.execute("SELECT name FROM armory_skills WHERE status='active'").fetchall()
        projected = []
        for r in rows:
            res = project_skill(r["name"], target_agent=target_agent, target_dir=target_dir, armory_dir=armory_root, conn=c)
            if res.get("mode") in ("symlink", "copy", "json_spec"):
                projected.append(r["name"])
        return projected

def queue_skill_for_mining(source_url: str, conn: Optional[sqlite3.Connection] = None) -> int:
    with get_armory_connection(conn, None) as c:
        cursor = c.cursor()
        cursor.execute("INSERT INTO armory_miner_queue (source_url, status) VALUES (?, 'pending')", (source_url,))
        c.commit()
        return cursor.lastrowid

def process_miner_queue(
    limit: int = 5,
    armory_dir: Optional[Path] = None,
    conn: Optional[sqlite3.Connection] = None,
) -> List[Dict[str, Any]]:
    armory_root = armory_dir or get_armory_dir()
    results = []
    with get_armory_connection(conn, armory_root / "armory.db") as c:
        queue_items = c.execute(
            "SELECT id, source_url FROM armory_miner_queue WHERE status = 'pending' LIMIT ?",
            (limit,)
        ).fetchall()

        for item in queue_items:
            item_id = item["id"]
            source_url = item["source_url"]

            extracted_name = f"mined-{item_id}"
            extracted_content = (
                f"---\nname: {extracted_name}\ndescription: Mined skill from {source_url}\n---\n"
                f"# {extracted_name}\nSimulated clean skill content mined from {source_url}."
            )

            skill_res = register_skill(
                name=extracted_name,
                description=f"Mined skill from {source_url}",
                category="mined",
                content=extracted_content,
                source="miner",
                armory_dir=armory_root,
                conn=c,
            )

            status = "completed" if skill_res["status"] == "active" else "quarantined"
            c.execute(
                "UPDATE armory_miner_queue SET status=?, processed_at=CURRENT_TIMESTAMP, log=? WHERE id=?",
                (status, json.dumps(skill_res), item_id)
            )
            c.commit()
            skill_res["queue_id"] = item_id
            skill_res["queue_status"] = status
            results.append(skill_res)

    return results

def search_armory(
    query: str,
    limit: int = 10,
    conn: Optional[sqlite3.Connection] = None,
) -> List[Dict[str, Any]]:
    with get_armory_connection(conn, None) as c:
        try:
            fts_rows = c.execute('''
                SELECT s.* FROM armory_skills s
                JOIN armory_fts f ON s.id = f.rowid
                WHERE armory_fts MATCH ?
                LIMIT ?
            ''', (query, limit)).fetchall()
            if fts_rows:
                return [dict(r) for r in fts_rows]
        except Exception:
            pass

        like_rows = c.execute('''
            SELECT * FROM armory_skills
            WHERE name LIKE ? OR description LIKE ? OR tags LIKE ? OR category LIKE ?
            LIMIT ?
        ''', (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", limit)).fetchall()
        return [dict(r) for r in like_rows]

def list_armory_skills(
    category: Optional[str] = None,
    status: str = "active",
    conn: Optional[sqlite3.Connection] = None,
) -> List[Dict[str, Any]]:
    with get_armory_connection(conn, None) as c:
        if category:
            rows = c.execute("SELECT * FROM armory_skills WHERE status = ? AND category = ?", (status, category)).fetchall()
        else:
            rows = c.execute("SELECT * FROM armory_skills WHERE status = ?", (status,)).fetchall()
        return [dict(r) for r in rows]

def get_skill(name: str, conn: Optional[sqlite3.Connection] = None) -> Optional[Dict[str, Any]]:
    with get_armory_connection(conn, None) as c:
        row = c.execute("SELECT * FROM armory_skills WHERE name = ?", (name,)).fetchone()
        return dict(row) if row else None

def format_armory_status(conn: Optional[sqlite3.Connection] = None) -> str:
    with get_armory_connection(conn, None) as c:
        active = c.execute("SELECT name FROM armory_skills WHERE status='active'").fetchall()
        quarantined = c.execute("SELECT name FROM armory_skills WHERE status='quarantined'").fetchall()
        pending = c.execute("SELECT COUNT(*) FROM armory_miner_queue WHERE status='pending'").fetchone()[0]

        lines = [
            "Aegis Global Skill Armory Status",
            f"Active Skills: {len(active)} ({', '.join([r['name'] for r in active]) if active else 'None'})",
            f"Quarantined Skills: {len(quarantined)} ({', '.join([r['name'] for r in quarantined]) if quarantined else 'None'})",
            f"Pending Mining Count: {pending}",
        ]
        return "\n".join(lines)


# Role-Based Dynamic Arsenal Archetype System
ARSENAL_ARCHETYPES: Dict[str, Dict[str, Any]] = {
    "developer": {
        "name": "Developer",
        "description": "Core systems, testing, git, AST code graph, and token arbitrage workers (Hermes, OpenCode, uv).",
        "skills": [
            "andrej-karpathy-skills",
            "ecc",
            "superpowers",
            "unslop-master",
            "unslop",
            "diagram-design",
            "python",
            "typescript",
        ],
        "tools": ["git", "python", "sqlite3", "uv", "hermes", "opencode"],
        "tags": ["dev", "system", "testing", "code", "ast", "arbitrage", "git"],
    },
    "creator": {
        "name": "Creator",
        "description": "Sensory perception (FFmpeg, Whisper speech-to-text, keyframe extraction), OpenMontage, design-taste, UI-UX Pro Max, reel-ingest, comment-gate-bypass.",
        "skills": [
            "ui-ux-pro-max-skill",
            "remotion-best-practices",
            "openmontage",
            "unslop-master",
            "sensory-accelerators",
            "diagram-design",
        ],
        "tools": ["ffmpeg", "whisper", "satori"],
        "tags": ["media", "video", "audio", "ui", "ux", "design", "reel", "sensory", "creator", "transcribe"],
    },
    "security": {
        "name": "Security",
        "description": "Artemis scanner, DAST scanning, AST vulnerability auditor, red-team sandbox, GitGuardian secret scanning.",
        "skills": [
            "artemis",
            "dast-scanning",
            "sandbox-vulnerability",
            "gitguardian",
            "penetration-testing",
            "unslop-master",
        ],
        "tools": ["artemis", "secret-scanner", "dast-scanner"],
        "tags": ["security", "pentest", "redteam", "vulnerability", "audit", "cve", "dast", "secret"],
    },
    "omni": {
        "name": "Omni",
        "description": "All system capabilities, media engines, and security auditing tools fully mounted.",
        "skills": [
            "andrej-karpathy-skills",
            "ecc",
            "superpowers",
            "unslop-master",
            "unslop",
            "diagram-design",
            "python",
            "typescript",
            "ui-ux-pro-max-skill",
            "remotion-best-practices",
            "openmontage",
            "sensory-accelerators",
            "artemis",
            "dast-scanning",
            "sandbox-vulnerability",
            "gitguardian",
            "penetration-testing",
        ],
        "tools": ["git", "python", "sqlite3", "uv", "hermes", "opencode", "ffmpeg", "whisper", "artemis"],
        "tags": ["omni", "all", "full"],
    },
}


def get_active_archetype(conn: Optional[sqlite3.Connection] = None, db_path: Optional[Path] = None) -> str:
    """Return active archetype profile name (defaults to 'developer')."""
    try:
        from .config import get_db_path
        brain_path = db_path or get_db_path()
        if brain_path.exists():
            with sqlite3.connect(str(brain_path)) as c:
                c.row_factory = sqlite3.Row
                cols = {row["name"] for row in c.execute("PRAGMA table_info(host_capabilities)").fetchall()}
                if "archetype" in cols:
                    row = c.execute("SELECT archetype FROM host_capabilities WHERE id = 1").fetchone()
                    if row and row["archetype"]:
                        return str(row["archetype"]).lower()
    except Exception:
        pass
    return "developer"


def apply_archetype_profile(
    profile_name: str,
    target_agent: str = "claude",
    target_dir: Optional[Path] = None,
    armory_dir: Optional[Path] = None,
    conn: Optional[sqlite3.Connection] = None,
) -> Dict[str, Any]:
    """Mounts skills in archetype profile and updates armory.db and host_capabilities."""
    norm = profile_name.strip().lower()
    if norm not in ARSENAL_ARCHETYPES:
        valid_keys = ", ".join(ARSENAL_ARCHETYPES.keys())
        raise ValueError(f"Unknown archetype profile '{profile_name}'. Available profiles: {valid_keys}")

    archetype_info = ARSENAL_ARCHETYPES[norm]
    armory_root = armory_dir or get_armory_dir()

    mounted: List[str] = []
    init_armory_db(conn, armory_root / "armory.db")
    with get_armory_connection(conn, armory_root / "armory.db") as c:
        for skill_name in archetype_info["skills"]:
            existing = c.execute("SELECT id FROM armory_skills WHERE name = ?", (skill_name,)).fetchone()
            if not existing:
                content = (
                    f"---\nname: {skill_name}\ndescription: {archetype_info['name']} capability\ncategory: {norm}\n---\n"
                    f"# {skill_name}\nStandard active capability provided by the {archetype_info['name']}."
                )
                register_skill(
                    name=skill_name,
                    description=f"{archetype_info['name']} capability",
                    category=norm,
                    content=content,
                    source="archetype",
                    armory_dir=armory_root,
                    conn=c,
                )
            res = project_skill(
                skill_name,
                target_agent=target_agent,
                target_dir=target_dir,
                armory_dir=armory_root,
                conn=c,
            )
            if res.get("status") != "error":
                mounted.append(skill_name)

    # Update host_capabilities in brain.db
    try:
        from .config import get_db_path
        from .environment import init_host_capabilities_table
        init_host_capabilities_table()
        brain_path = get_db_path()
        with sqlite3.connect(str(brain_path)) as c_brain:
            cols = {row[1] for row in c_brain.execute("PRAGMA table_info(host_capabilities)").fetchall()}
            if cols and "archetype" not in cols:
                c_brain.execute("ALTER TABLE host_capabilities ADD COLUMN archetype TEXT DEFAULT 'developer'")
            cur = c_brain.execute("UPDATE host_capabilities SET archetype = ?, updated_at = CURRENT_TIMESTAMP WHERE id = 1", (norm,))
            if cur.rowcount == 0:
                c_brain.execute("INSERT INTO host_capabilities (id, os, shell, pkg_manager, archetype, updated_at) VALUES (1, 'unknown', 'unknown', 'unknown', ?, CURRENT_TIMESTAMP)", (norm,))
            c_brain.commit()
    except Exception:
        pass

    # Invalidate environment cache
    try:
        from . import environment
        environment._HOST_CAPABILITIES_CACHE = None
    except Exception:
        pass
    try:
        import sys
        if "aegis.environment" in sys.modules:
            sys.modules["aegis.environment"]._HOST_CAPABILITIES_CACHE = None
    except Exception:
        pass

    return {
        "profile": norm,
        "name": archetype_info["name"],
        "description": archetype_info["description"],
        "status": "active",
        "mounted_skills": mounted,
        "tools": archetype_info.get("tools", []),
        "message": f"Successfully activated '{archetype_info['name']}' pack ({len(mounted)} skills mounted).",
    }


def recommend_archetype_for_prompt(prompt: str, active_profile: Optional[str] = None) -> Optional[str]:
    """Detect if prompt demands skills outside the active archetype pack (Just-In-Time skill expansion)."""
    active = (active_profile or get_active_archetype()).strip().lower()
    if active == "omni":
        return None

    p_lower = prompt.lower()

    # Creator triggers
    creator_triggers = [
        "video", "ffmpeg", "whisper", "transcribe", "speech", "animation",
        "remotion", "ui-ux", "reel", "montage", "canvas", "keyframes",
        "audio extraction", "subtitles", "voiceover", "openmontage"
    ]
    if active != "creator":
        if any(w in p_lower for w in creator_triggers):
            return "creator"

    # Security triggers
    security_triggers = [
        "pentest", "vulnerability", "cve", "dast", "artemis", "redteam", "red team",
        "injection", "secret leak", "reverse shell", "port scan", "exploit",
        "security audit", "gitguardian"
    ]
    if active != "security":
        if any(w in p_lower for w in security_triggers):
            return "security"

    # Developer triggers
    dev_triggers = [
        "git pr", "pytest", "ast graph", "token arbitrage", "benchmark bottleneck",
        "backend", "sqlite", "fastapi", "django"
    ]
    if active not in ("developer", "omni"):
        if any(w in p_lower for w in dev_triggers):
            return "developer"

    return None

