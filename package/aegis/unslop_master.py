"""
UnslopMaster - AI-generated content cleanup and detection.
Standard library only: re, ast, dataclasses, typing, pathlib, sys.
"""

import re
import ast
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union
from pathlib import Path


class FindingsList(list):
    """Subclass of list that overrides __contains__ for string matching in findings."""

    def __contains__(self, item: Any) -> bool:
        if isinstance(item, str):
            item_lower = item.lower()
            for entry in self:
                if isinstance(entry, dict):
                    for value in entry.values():
                        if item_lower in str(value).lower():
                            return True
                elif isinstance(entry, str):
                    if item_lower in entry.lower():
                        return True
                else:
                    if item_lower in str(entry).lower():
                        return True
            return False
        return super().__contains__(item)


class UnslopResult(str):
    """Subclass of str that carries metadata about the cleanup."""

    def __new__(
        cls,
        cleaned_text: str,
        slop_detected: bool = False,
        score: int = 100,
        findings=None,
        categories=None,
        summary: str = "",
    ):
        obj = super().__new__(cls, cleaned_text)
        obj.cleaned_text = cleaned_text
        obj.slop_detected = slop_detected
        obj.score = score
        obj.findings = FindingsList(findings or [])
        obj.categories = categories or []
        obj.summary = summary
        return obj

    @property
    def cleaned(self) -> str:
        return self.cleaned_text

    @property
    def original(self) -> str:
        return getattr(self, "_original", self.cleaned_text)


class _UniversalMethod:
    """Descriptor that binds target to instance if called on instance, or to class if called on class."""

    def __init__(self, fn):
        self.fn = fn

    def __get__(self, obj, cls=None):
        target = obj if obj is not None else cls
        return lambda *args, **kwargs: self.fn(target, *args, **kwargs)


class UnslopMaster:
    """Main class for detecting and cleaning AI-generated slop."""

    # --- Constant Patterns ---

    AI_CONVERSATIONAL_WATERMARKS = [
        r"^(?:Certainly!|Sure!|Of course!|Here is the (?:code|implementation|solution|file):?)\s*",
        r"^(?:I(?:'ve| have) implemented the requested changes\.?)\s*",
        r"^(?:I would be happy to (?:help|delve).*?\.?)\s*",
        r"^(?:Let's dive in(?: to (?:the code|this))?!?:?)\s*",
        r"^(?:As an AI language model,?\s*)",
        r"\b(?:Certainly!|Sure!|Of course!)\s*",
        r"\bHere is the (?:code|implementation|solution|file):?\s*",
        r"\bI would be happy to help\.?\s*",
        r"\bLet's dive in\.?\s*",
        r"\bAs an AI language model,?\s*",
        r"(?:\n\s*)*I hope this helps!?.*$",
        r"(?:\n\s*)*Feel free to ask (?:me )?if you have any(?: further)? questions!?.*$",
        r"(?:\n\s*)*Let me know if you (?:need|would like) any further changes!?.*$",
        r"(?:\n\s*)*Let me know if you have any questions!?.*$",
    ]

    REDUNDANT_COMMENT_PATTERNS = [
        (r"(?i)#\s*Import.*?\n", ""),
        (r"(?i)//\s*Import.*?\n", ""),
        (r"(?i)#\s*Constructor\s*\n", ""),
        (r"(?i)//\s*Constructor\s*\n", ""),
        (r"(?i)#\s*Helper function\s*\n", ""),
        (r"(?i)//\s*Helper function\s*\n", ""),
        (r"(?i)#\s*Initialize.*?\n", ""),
        (r"(?i)//\s*Initialize.*?\n", ""),
        (r"(?i)#\s*Return.*?\n", ""),
        (r"(?i)#\s*Main function.*?\n", ""),
        (r"(?i)#\s*Variables.*?\n", ""),
        (r"(?i)#\s*(?:OpenAI|API|Token)\s*(?:token|key)?.*?\n", ""),
        # Inline comments
        (r"\s*#\s*Initialize variable\s*$", ""),
        (r"\s*//\s*Initialize variable\s*$", ""),
        (r"\s*#\s*Helper function\s*$", ""),
    ]

    ROBOTIC_TRANSITIONS = [
        r"\bMoreover,\s*",
        r"\bFurthermore,\s*",
        r"\bAdditionally,\s*",
        r"\bIn conclusion,\s*",
        r"\bTo summarize,\s*",
        r"\bIt is worth noting that\s*",
    ]

    STOCK_VOCAB_MAP = {
        r"\bdelve into\b": "explore",
        r"\bdelve\b": "dig",
        r"\btestament to\b": "evidence of",
        r"\btapestry of\b": "collection of",
        r"\brich tapestry\b": "collection",
        r"\bpivotal\b": "key",
        r"\bseamlessly\b": "smoothly",
        r"\bseamless\b": "smooth",
        r"\brobustly\b": "reliably",
        r"\brobust\b": "reliable",
        r"\bleveraging\b": "using",
        r"\bleverage\b": "use",
        r"in today's fast-paced world": "today",
        r"in today's world": "today",
        r"\bsupercharge\b": "boost",
        r"\bgame-changer\b": "major change",
        r"\bcutting-edge\b": "modern",
        r"\belevate\b": "improve",
        r"\bunleash\b": "release",
        r"\bdemystify\b": "explain",
    }

    UI_SLOP_PATTERNS = [
        r"filter:\s*blur\([^)]+\);?",
        r"backdrop-filter:\s*blur\([^)]+\);?",
        r"\bbg-gradient-to-[a-z]+\s+from-(?:purple|pink|indigo|violet)-\d+\s+via-(?:pink|purple|fuchsia)-\d+\s+to-(?:red|indigo|blue)-\d+;?",
    ]

    # --- Initialization ---

    def __init__(self, mode: str = "auto", deep: bool = False):
        self.mode = mode
        self.deep = deep

    # --- Core Scrub Methods ---

    @_UniversalMethod
    def scrub_code(target, code: str, deep: bool = False) -> Tuple[str, bool]:
        """Strip watermarks and redundant comments from code. If deep=True, check AST for stubs."""
        cleaned = code
        changed = False

        # Remove conversational watermarks
        for pattern in target.AI_CONVERSATIONAL_WATERMARKS:
            new_cleaned = re.sub(pattern, "", cleaned, flags=re.MULTILINE)
            if new_cleaned != cleaned:
                changed = True
                cleaned = new_cleaned

        # Remove redundant comments
        for pattern, replacement in target.REDUNDANT_COMMENT_PATTERNS:
            new_cleaned = re.sub(pattern, replacement, cleaned)
            if new_cleaned != cleaned:
                changed = True
                cleaned = new_cleaned

        # Deep mode: check AST for stubs (pass through, detection happens in detect_slop)
        if deep:
            try:
                ast.parse(cleaned)
            except SyntaxError:
                pass  # Not valid Python, skip AST analysis

        return cleaned, changed

    @_UniversalMethod
    def scrub_prose(target, text: str, deep: bool = False) -> Tuple[str, bool]:
        """Strip conversational watermarks and robotic transitions from prose."""
        cleaned = text
        changed = False

        # Remove conversational watermarks
        for pattern in target.AI_CONVERSATIONAL_WATERMARKS:
            new_cleaned = re.sub(pattern, "", cleaned, flags=re.MULTILINE | re.IGNORECASE)
            if new_cleaned != cleaned:
                changed = True
                cleaned = new_cleaned

        # Remove robotic transitions
        for pattern in target.ROBOTIC_TRANSITIONS:
            new_cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
            if new_cleaned != cleaned:
                changed = True
                cleaned = new_cleaned

        # Normalize em-dashes
        new_cleaned = re.sub(r"\s*—\s*", ", ", cleaned)
        if new_cleaned != cleaned:
            changed = True
            cleaned = new_cleaned

        if deep:
            # Replace stock vocabulary
            for pattern, replacement in target.STOCK_VOCAB_MAP.items():
                new_cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
                if new_cleaned != cleaned:
                    changed = True
                    cleaned = new_cleaned

            # Normalize negative tricolons (e.g., "no X, no Y, no Z" or "not X, not Y, not Z")
            tricolon_pattern = r"(\b(?:not|no)\s+\w+),\s*((?:not|no)\s+\w+),\s*((?:not|no)\s+\w+)"
            def replace_tricolon(match):
                g1 = match.group(1)
                g2 = re.sub(r"^(?:not|no)\s+", "", match.group(2), flags=re.IGNORECASE)
                g3 = re.sub(r"^(?:not|no)\s+", "", match.group(3), flags=re.IGNORECASE)
                return f"{g1}, {g2}, or {g3}"
            new_cleaned = re.sub(tricolon_pattern, replace_tricolon, cleaned, flags=re.IGNORECASE)
            if new_cleaned != cleaned:
                changed = True
                cleaned = new_cleaned

        return cleaned, changed

    @_UniversalMethod
    def scrub_ui(target, markup: str, deep: bool = False) -> Tuple[str, bool]:
        """Strip blur styles and rainbow gradient blobs from UI markup."""
        cleaned = markup
        changed = False

        for pattern in target.UI_SLOP_PATTERNS:
            new_cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
            if new_cleaned != cleaned:
                changed = True
                cleaned = new_cleaned

        return cleaned, changed

    # --- Detection ---

    @_UniversalMethod
    def detect_slop(target, text: str) -> Dict[str, Any]:
        """Scan all 4 pillars and return detection results."""
        findings = FindingsList()
        categories = []
        slop_detected = False

        # Pillar 1: Conversational watermarks
        for pattern in target.AI_CONVERSATIONAL_WATERMARKS:
            matches = list(re.finditer(pattern, text, flags=re.MULTILINE | re.IGNORECASE))
            if matches:
                slop_detected = True
                categories.append("conversational_watermark")
                for match in matches:
                    findings.append({
                        "pillar": "conversational_watermark",
                        "details": f"Found watermark: {match.group()[:100]}",
                        "position": match.span(),
                    })

        # Pillar 2: Redundant comments
        for pattern, _ in target.REDUNDANT_COMMENT_PATTERNS:
            matches = list(re.finditer(pattern, text, flags=re.IGNORECASE))
            if matches:
                slop_detected = True
                categories.append("redundant_comment")
                for match in matches:
                    findings.append({
                        "pillar": "redundant_comment",
                        "details": f"Found redundant comment: {match.group()[:100]}",
                        "position": match.span(),
                    })

        # Pillar 3: Robotic transitions
        for pattern in target.ROBOTIC_TRANSITIONS:
            matches = list(re.finditer(pattern, text, flags=re.IGNORECASE))
            if matches:
                slop_detected = True
                categories.append("robotic_transition")
                for match in matches:
                    findings.append({
                        "pillar": "robotic_transition",
                        "details": f"Found robotic transition: {match.group()}",
                        "position": match.span(),
                    })

        # Pillar 4: Stock vocabulary
        for pattern, replacement in target.STOCK_VOCAB_MAP.items():
            matches = list(re.finditer(pattern, text, flags=re.IGNORECASE))
            if matches:
                slop_detected = True
                categories.append("stock_vocabulary")
                for match in matches:
                    findings.append({
                        "pillar": "stock_vocabulary",
                        "details": f"Found stock phrase '{match.group()}' -> '{replacement}'",
                        "position": match.span(),
                    })

        # Pillar 5: UI slop
        for pattern in target.UI_SLOP_PATTERNS:
            matches = list(re.finditer(pattern, text, flags=re.IGNORECASE))
            if matches:
                slop_detected = True
                categories.append("ui_slop")
                for match in matches:
                    findings.append({
                        "pillar": "ui_slop",
                        "details": f"Found UI slop: {match.group()[:100]}",
                        "position": match.span(),
                    })

        # Deep mode: Check for Python stubs
        if getattr(target, 'deep', False):
            try:
                tree = ast.parse(text)
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        # Check if function body is just pass or ...
                        if len(node.body) == 1:
                            stmt = node.body[0]
                            if isinstance(stmt, ast.Pass) or (
                                isinstance(stmt, ast.Expr) and
                                isinstance(stmt.value, ast.Constant) and
                                stmt.value.value is Ellipsis
                            ):
                                slop_detected = True
                                categories.append("stub")
                                findings.append({
                                    "pillar": "stub",
                                    "details": f"Function '{node.name}' is a stub (pass/...)",
                                    "position": (node.lineno, node.end_lineno or node.lineno),
                                })
                            # Also check for explicit "stub" in name
                            if "stub" in node.name.lower():
                                slop_detected = True
                                categories.append("stub")
                                findings.append({
                                    "pillar": "stub",
                                    "details": f"Function '{node.name}' has 'stub' in name",
                                    "position": (node.lineno, node.end_lineno or node.lineno),
                                })
                    elif isinstance(node, ast.ClassDef):
                        if len(node.body) == 1:
                            stmt = node.body[0]
                            if isinstance(stmt, ast.Pass) or (
                                isinstance(stmt, ast.Expr) and
                                isinstance(stmt.value, ast.Constant) and
                                stmt.value.value is Ellipsis
                            ):
                                slop_detected = True
                                categories.append("stub")
                                findings.append({
                                    "pillar": "stub",
                                    "details": f"Class '{node.name}' is a stub (pass/...)",
                                    "position": (node.lineno, node.end_lineno or node.lineno),
                                })
            except SyntaxError:
                pass  # Not valid Python

        # Deduplicate categories
        categories = list(dict.fromkeys(categories))

        # Calculate score: 100 if clean, 100 - count*5 otherwise (min 0)
        score = 100
        if slop_detected:
            score = max(0, 100 - len(findings) * 5)

        summary = f"Found {len(findings)} slop instances across {len(categories)} categories" if slop_detected else "Clean"

        return {
            "slop_detected": slop_detected,
            "score": score,
            "findings": findings,
            "categories": categories,
            "summary": summary,
        }

    # --- Dispatch ---

    @_UniversalMethod
    def scrub(target, text: str, mode: Optional[str] = None, deep: Optional[bool] = None) -> Tuple[str, bool]:
        """Resolve mode/deep and dispatch to appropriate scrubber."""
        resolved_mode = mode if mode is not None else getattr(target, "mode", "auto")
        resolved_deep = deep if deep is not None else getattr(target, "deep", False)

        # Auto-detect mode if needed
        if resolved_mode == "auto":
            # Heuristic: check for code patterns
            if re.search(r"^\s*(def|class|import|from)\s", text, re.MULTILINE):
                resolved_mode = "code"
            elif re.search(r"(filter:|backdrop-filter:|bg-gradient-to-)", text, re.IGNORECASE):
                resolved_mode = "ui"
            else:
                resolved_mode = "prose"

        if resolved_mode == "code":
            return target.scrub_code(text, resolved_deep)
        elif resolved_mode == "ui":
            return target.scrub_ui(text, resolved_deep)
        else:  # prose
            return target.scrub_prose(text, resolved_deep)

    @_UniversalMethod
    def run(target, text: str, mode: Optional[str] = None, deep: Optional[bool] = None) -> UnslopResult:
        """Run scrub + detect_slop and return UnslopResult."""
        # Store original for the .original property
        original_text = text

        cleaned, _ = target.scrub(text, mode, deep)
        detection = target.detect_slop(text)

        result = UnslopResult(
            cleaned_text=cleaned,
            slop_detected=detection["slop_detected"],
            score=detection["score"],
            findings=detection["findings"],
            categories=detection["categories"],
            summary=detection["summary"],
        )
        result._original = original_text
        return result


# --- Convenience Function ---

def unslop(text: str, deep: bool = False, mode: str = "auto") -> UnslopResult:
    """
    Run UnslopMaster on text and return UnslopResult.
    Since UnslopResult subclasses str, it is both an UnslopResult and a str!
    """
    master = UnslopMaster(mode=mode, deep=deep)
    return master.run(text, mode=mode, deep=deep)


# --- Module exports ---
__all__ = [
    "FindingsList",
    "UnslopResult",
    "_UniversalMethod",
    "UnslopMaster",
    "unslop",
]