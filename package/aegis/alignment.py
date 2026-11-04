"""AegisBrain Alignment & Educational Concept Visualizer.

Implements the 2-Stage User-Agent Alignment Protocol:
1. Concept Education (Archify-Style):
   - When a user is exploring or unfamiliar with technology choices, provides intuitive
     conceptual models, ASCII/Mermaid architectural blueprints, and curated video/doc links.
2. "Grill Me" Diagnostic Interview (Matt Pocock Protocol):
   - Generates 3-5 high-leverage questions to extract non-obvious constraints,
     trade-offs, acceptance criteria, and edge cases before coding begins.
"""

from typing import Any, Dict, List, Optional
from .ceo_stress_test import YCCEOStressTester, CEOCritique


CURATED_TECH_RESOURCES = {
    "spring": {
        "title": "Spring Boot & Spring AI Architecture",
        "description": "Enterprise Java framework for building cloud-native, observable, reactive microservices and AI applications.",
        "video": "https://www.youtube.com/watch?v=9SGDpanrc8U",
        "docs": "https://docs.spring.io/spring-ai/reference/",
        "key_concepts": ["Inversion of Control (IoC)", "Observability Conventions", "Micrometer Tracing", "OpenAI ChatOptions"]
    },
    "fastapi": {
        "title": "FastAPI & Modern Python Asynchronous APIs",
        "description": "High-performance ASGI framework powered by Pydantic type hints and Starlette.",
        "video": "https://www.youtube.com/watch?v=0sOvCWFmrtA",
        "docs": "https://fastapi.tiangolo.com/",
        "key_concepts": ["ASGI event loop", "Pydantic V2 serialization", "Dependency Injection", "OpenAPI docs"]
    },
    "react": {
        "title": "React 19 & Next.js Server Components",
        "description": "Declarative component-driven UI library with streaming server rendering and modern concurrent hooks.",
        "video": "https://www.youtube.com/watch?v=8pDqJVdNa44",
        "docs": "https://react.dev/",
        "key_concepts": ["Server vs Client components", "Suspense boundaries", "Hydration", "Tailwind CSS"]
    },
    "postgres": {
        "title": "PostgreSQL & TimescaleDB / pgvector",
        "description": "Battle-tested relational database with ACID compliance, relational graphs, and vector similarity search.",
        "video": "https://www.youtube.com/watch?v=qw--VYLpxG4",
        "docs": "https://www.postgresql.org/docs/",
        "key_concepts": ["WAL indexing", "B-Tree vs GIN indexes", "Vector HNSW", "Foreign key constraints"]
    },
    "remotion": {
        "title": "Remotion (React Video Creation)",
        "description": "Programmatic video synthesis and animation framework using React, Canvas, and FFmpeg.",
        "video": "https://www.youtube.com/watch?v=deg8bOoziaE",
        "docs": "https://www.remotion.dev/docs",
        "key_concepts": ["useCurrentFrame()", "Composition metadata", "Spring physics animations", "Serverless rendering"]
    }
}


class AlignmentEngine:
    """Orchestrates concept awareness, architecture visualization, and Grill-Me interviews."""

    @classmethod
    def stress_test_concept(cls, idea: str, context: Optional[str] = None) -> CEOCritique:
        """Run Y-Combinator CEO stress test against an idea or technical approach."""
        return YCCEOStressTester.evaluate(idea, context)

    @classmethod
    def find_relevant_education(cls, prompt_or_tech: str) -> Optional[Dict[str, Any]]:
        lower = prompt_or_tech.lower()
        for key, res in CURATED_TECH_RESOURCES.items():
            if key in lower:
                return res
        return None

    @classmethod
    def generate_educational_blueprint(cls, topic: str, tech_key: Optional[str] = None) -> str:
        """Render Archify-style architecture education block with video link and Mermaid diagram."""
        resource = CURATED_TECH_RESOURCES.get(tech_key or "") if tech_key else cls.find_relevant_education(topic)

        title = resource["title"] if resource else f"Architecture Overview: {topic}"
        desc = resource["description"] if resource else "Modular micro-service and layered component architecture."
        video_link = resource["video"] if resource else "https://www.youtube.com/results?search_query=" + topic.replace(" ", "+")
        docs_link = resource["docs"] if resource else "https://devdocs.io"
        concepts = resource["key_concepts"] if resource else ["Layered Separation", "Safe Error Boundaries", "Automated Testing"]

        blueprint = f"""
### 🎓 Technology & Concept Briefing: {title}

**Core Intuition**: {desc}

#### Key Architectural Pillars
{chr(10).join(f"- **{c}**" for c in concepts)}

```mermaid
graph TD
    Client["User Interface / CLI Client"] --> Controller["API Gateway / Controller Layer"]
    Controller --> Service["Business Logic & Service Engine"]
    Service --> Safety["Security & Validation Boundary"]
    Safety --> Storage[("Database & State Repository")]
    Safety --> External["External Model / Cloud APIs"]
```

- 📖 **Documentation**: [{title}]({docs_link})
- 📺 **Visual Video Walkthrough**: [Watch Architectural Walkthrough]({video_link})
"""
        return blueprint.strip()

    @classmethod
    def generate_grill_me_interview(cls, task_summary: str) -> List[Dict[str, Any]]:
        """Generate 3 Matt Pocock 'Grill Me' clarifying questions for the task."""
        return [
            {
                "id": "deliverable_scope",
                "question": f"For '{task_summary}', what is the primary delivery format and boundary?",
                "options": [
                    "(Recommended) Production-ready implementation with automated unit tests & docs",
                    "Minimal working proof-of-concept (PoC) to validate architecture first",
                    "Modular library package with standalone CLI and extensible hooks",
                    "Detailed architectural design specification (ADR) prior to any coding"
                ]
            },
            {
                "id": "ui_aesthetic_or_interface",
                "question": "What is the expected user interaction mode or aesthetic style?",
                "options": [
                    "(Recommended) Clean, dense terminal CLI with rich ANSI progress indicators",
                    "Modern web UI (Tailwind CSS, high-contrast, accessible tokens)",
                    "Headless background daemon with zero-elevation autostart & HTTP REST API",
                    "Strictly programmatic Python/TypeScript SDK without UI bloat"
                ]
            },
            {
                "id": "error_tolerance_and_rollback",
                "question": "How should unexpected exceptions or configuration failures be handled?",
                "options": [
                    "(Recommended) Create automated restore point snapshot & rollback instantly on error",
                    "Log warning, gracefully degrade to fallback, and continue execution",
                    "Fail fast with explicit stack trace and diagnostic GitHub report URL"
                ]
            }
        ]
