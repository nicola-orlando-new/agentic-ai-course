# Guardrails (later exercise): see the "Later Exercise: Guardrails" section in README.md.
#
# ADK callbacks are hooks that run at fixed points of the agent loop.
# If a callback returns None, execution continues normally.
# If it returns a value, that value replaces the step, so the model or the tool never runs.

from google.adk.models import LlmResponse
from google.genai import types


BLOCKED_PHRASES = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "reveal your system prompt",
    "reveal your instructions",
    "you are now",
]
REFUSAL = "Sorry, I can't help with that. I can only help with travel information for your trip, like weather, local time, and currency conversion."


def input_guardrail(callback_context, llm_request):
    """before_model_callback: runs before every LLM call. Blocks prompt-injection attempts."""
    last = llm_request.contents[-1] if llm_request.contents else None
    if last and last.role == "user":
        text = " ".join(part.text or "" for part in last.parts).lower()
        if any(phrase in text for phrase in BLOCKED_PHRASES):
            # Returning an LlmResponse skips the model call entirely.
            return LlmResponse(
                content=types.Content(role="model", parts=[types.Part(text=REFUSAL)])
            )
    return None


def tool_guardrail(tool, args, tool_context):
    """before_tool_callback: runs before every tool call. Validates the arguments the LLM chose."""
    if tool.name == "convert_currency" and args.get("amount", 0) < 0:
        # Returning a dict skips the tool and uses this dict as the tool result.
        return {"error": "Amount must not be negative."}
    return None
