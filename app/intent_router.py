from app.llm import llm
from app.schemas import IntentResult


intent_llm = llm.with_structured_output(IntentResult)

INTENT_PROMPT = """
You are an intent classifier.

Determine whether the user wants to:

1. Continue chatting
2. Update an issue

If the intent is update_issue:

Extract:

- issue_id
- customer_name (if present)
- status

Valid statuses:

Open
In Progress
Resolved
Closed

Never answer the user.

Only return the structured result.
"""


async def detect_intent(
    message: str,
) -> IntentResult:

    return await intent_llm.ainvoke(
        [
            (
                "system",
                INTENT_PROMPT,
            ),
            (
                "user",
                message,
            ),
        ]
    )