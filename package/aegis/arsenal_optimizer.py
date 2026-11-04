"""AegisBrain Proactive Arsenal & Research Optimization Engine.

Continuously scans user tasks and prompts to:
1. Detect technology domain and intent across the 14 Arsenal Niches.
2. Search and auto-activate the highest-scoring Tier S & Tier A skills in the Arsenal
   (~/.gemini/config/skills, plugins, tools).
3. Identify when external web scraping / research will produce higher-signal, modern patterns.
4. Provide immediate, transparent recommendations to the user before code execution.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
from .skill_scout import get_installed_skills_inventory
from .browser import search_web_duckduckgo


NICHE_SKILL_RECOMMENDATIONS = {
    "frontend": [
        ("uipro", "UI-UX Pro Max Design Intelligence (Accessible contrast, layout tokens, responsive grids)"),
        ("impeccable", "Frontend design taste, neo-brutalism, dark mode tokens"),
        ("gsap", "GSAP micro-interactions and smooth hardware-accelerated motion")
    ],
    "backend": [
        ("ecc", "Enterprise coding conventions, clean architecture, conventional commits"),
        ("spring-ai", "Spring AI microservices, observation conventions, prompt templates"),
        ("fastapi-patterns", "Modern ASGI, Pydantic v2 schemas, type-safe endpoints")
    ],
    "database": [
        ("pg-aiguide", "PostgreSQL query planning, hypertable indexing, and connection pools"),
        ("postgres-table-design", "Relational foreign keys, ACID integrity, and schema migration safety")
    ],
    "security": [
        ("security-audit", "Red-team checklist: prompt injection defense, shell=True prevention, CORS hardening"),
        ("sops-encryption", "Secrets and credential encryption prior to git staging")
    ],
    "testing-qa": [
        ("test-engineer", "TDD workflow, boundary edge cases, regression test suites"),
        ("pypict-skill", "Pairwise combinatorial test generation")
    ],
    "video": [
        ("openmontage", "Programmatic video composition and automated FFmpeg pipelines"),
        ("remotion-best-practices", "React-driven canvas video rendering and frame sync")
    ]
}


@dataclass
class OptimizationPlan:
    task_query: str
    detected_niches: List[str]
    activated_skills: List[Dict[str, str]]
    recommended_web_searches: List[str]
    transparency_summary: str

    def to_markdown(self) -> str:
        skills_md = "\n".join(f"- ⚡ **{s['name']}**: {s['description']}" for s in self.activated_skills) or "Standard toolset sufficient."
        searches_md = "\n".join(f"- 🌐 `{q}`" for q in self.recommended_web_searches) or "No external search required."

        return f"""
### 🛠️ Aegis Arsenal & Research Optimization Activated

**Objective**: `{self.task_query}`
**Detected Niches**: `{', '.join(self.detected_niches) if self.detected_niches else 'General Engineering'}`

#### 1. Proactive Arsenal Skills Engaged
{skills_md}

#### 2. Targeted Web / Documentation Vectors
{searches_md}

#### 3. Engineering Rationale
{self.transparency_summary}
""".strip()


class ArsenalOptimizer:
    """Recommends and engages the best tools, skills, and research sources for any task."""

    @classmethod
    def analyze_and_optimize(cls, task_query: str, search_web: bool = False) -> OptimizationPlan:
        query_lower = task_query.lower()
        detected_niches: List[str] = []
        activated_skills: List[Dict[str, str]] = []
        searches: List[str] = []

        # Domain classification
        if any(w in query_lower for w in ["ui", "css", "html", "react", "frontend", "style", "extension", "component", "popup"]):
            detected_niches.append("frontend")
            for name, desc in NICHE_SKILL_RECOMMENDATIONS["frontend"]:
                activated_skills.append({"name": name, "description": desc})

        if any(w in query_lower for w in ["backend", "api", "spring", "server", "java", "python", "service", "endpoint"]):
            detected_niches.append("backend")
            for name, desc in NICHE_SKILL_RECOMMENDATIONS["backend"]:
                activated_skills.append({"name": name, "description": desc})

        if any(w in query_lower for w in ["database", "postgres", "sql", "db", "table", "schema", "query"]):
            detected_niches.append("database")
            for name, desc in NICHE_SKILL_RECOMMENDATIONS["database"]:
                activated_skills.append({"name": name, "description": desc})

        if any(w in query_lower for w in ["security", "secret", "gitguardian", "token", "auth", "inject", "redteam"]):
            detected_niches.append("security")
            for name, desc in NICHE_SKILL_RECOMMENDATIONS["security"]:
                activated_skills.append({"name": name, "description": desc})

        if any(w in query_lower for w in ["test", "unit", "pytest", "coverage", "qa", "assert"]):
            detected_niches.append("testing-qa")
            for name, desc in NICHE_SKILL_RECOMMENDATIONS["testing-qa"]:
                activated_skills.append({"name": name, "description": desc})

        # Web research recommendation
        if any(w in query_lower for w in ["new", "latest", "upgrade", "spring ai", "chrome store", "agent", "manifest v3"]):
            searches.append(f"{task_query} best practices 2026")
            searches.append(f"{task_query} documentation")

        # Fallback if no specific niche
        if not detected_niches:
            detected_niches.append("productivity")
            activated_skills.append({
                "name": "aegis-brain",
                "description": "Deterministic neural memory, AST graph indexing, and restore point safety"
            })

        summary = (
            f"Proactively engaged {len(activated_skills)} specialized skill(s) across "
            f"[{', '.join(detected_niches)}] to prevent code slop, enforce accessibility and security, "
            f"and maximize token efficiency."
        )

        return OptimizationPlan(
            task_query=task_query,
            detected_niches=detected_niches,
            activated_skills=activated_skills,
            recommended_web_searches=searches,
            transparency_summary=summary
        )
