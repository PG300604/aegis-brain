import json
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional
from .config import get_current_mode
from .db import record_session
from .distiller import distill_rules_for_prompt
from .governor import generate_active_context

DEFAULT_OLLAMA_UPSTREAM = "http://127.0.0.1:11434/v1/chat/completions"


def augment_chat_completion_payload(
    body: Dict[str, Any],
    workspace_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Inject active context and distilled skill guardrails into the system message."""
    messages: List[Dict[str, str]] = body.get("messages", [])

    # Find the latest user message text for skill matching
    last_user_prompt = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            last_user_prompt = m.get("content", "")
            break

    # Compile context and distilled skills
    active_ctx = generate_active_context()
    distilled_skills = distill_rules_for_prompt(last_user_prompt)

    system_injection = f"{active_ctx}\n\n{distilled_skills}\n"

    # If first message is system, prepend to it. Otherwise insert a system message.
    if messages and messages[0].get("role") == "system":
        messages[0]["content"] = f"{system_injection}\n\n{messages[0]['content']}"
    else:
        messages.insert(0, {"role": "system", "content": system_injection})

    body["messages"] = messages
    return body


def forward_chat_completion(
    body: Dict[str, Any],
    upstream_url: str = DEFAULT_OLLAMA_UPSTREAM,
    agent_name: str = "local-agent",
) -> tuple[int, Dict[str, Any]]:
    """Forward augmented payload to local model runtime (Ollama/Hermes)."""
    augmented = augment_chat_completion_payload(body)
    data = json.dumps(augmented).encode("utf-8")

    req = urllib.request.Request(
        upstream_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as res:
            res_body = json.loads(res.read().decode("utf-8"))

            if get_current_mode() == "public":
                # Record session trace silently
                record_session(
                    session_id=res_body.get("id", f"{agent_name}-run"),
                    agent_name=agent_name,
                    workspace_path="local",
                    summary="Local model chat completion forwarded through Aegis Proxy",
                )

            return res.status, res_body
    except urllib.error.URLError as e:
        return 502, {
            "error": "Upstream local engine offline",
            "details": f"Could not connect to {upstream_url}. Is Ollama or Hermes running?",
            "raw": str(e),
        }
    except Exception as e:
        return 500, {"error": "Proxy failure", "details": str(e)}
