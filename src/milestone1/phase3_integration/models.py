from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class PromptPayload:
    """
    The payload that will be sent to the LLM.
    This contains both the system instructions (rules) and the user content (preferences + candidates).
    """
    system_message: str
    user_message: str
