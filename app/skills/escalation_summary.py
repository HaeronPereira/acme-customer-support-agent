from app.database import get_session
from app.llm import llm
import time
from app.logger import logger
from app.services.customer_service import (
    get_customer_profile,
    get_open_issues,
    get_issue_history,
    get_next_action,
)


def customer_escalation_summary(customer_name: str) -> str:
    """
    Reusable Customer Escalation Summary Skill.
    """
    start = time.perf_counter()

    db = get_session()

    try:
        customer = get_customer_profile(db, customer_name)

        if customer is None:
            return "Customer not found."

        issues = get_open_issues(db, customer.customer_id)

        context = []

        for issue in issues:

            history = get_issue_history(db, issue.issue_id)
            action = get_next_action(db, issue.issue_id)

            context.append(
                {
                    "issue": {
                        "title": issue.title,
                        "description": issue.description,
                        "priority": issue.priority,
                        "status": issue.status,
                    },
                    "history": [
                        {
                            "updated_by": h["updated_by"],
                            "update": h["update_text"],
                            "created_at": h["created_at"],
                        }
                        for h in history
                    ],
                    "next_action": (
                        {
                            "action": action.action,
                            "owner": action.owner,
                            "status": action.status,
                            "due_date": (
                                action.due_date.isoformat()
                                if action.due_date
                                else None
                            ),
                        }
                        if action
                        else None
                    ),
                }
            )

        prompt = f"""
You are a Senior Customer Success Manager preparing an executive briefing.

Customer Profile:
{customer}

Issue Context:
{context}

Instructions:

- Base your analysis ONLY on the supplied data.
- If a Next Action already exists, reference it before suggesting a new action.
- recommend one more actions if there is only one next action but mention it is from AI
- Mention the action owner whenever available.
- Mention due dates when available.
- Do not invent engineering updates.
- If information is missing, explicitly state it.

Return the report with these headings:

1. Executive Summary
2. Customer Health
3. Open Issues
4. Existing Next Actions
5. Business Risk
6. Recommendations
7. Missing Information
8. Overall Priority
"""

        return llm.invoke(prompt).content

    finally:
        db.close()
        duration = (
                time.perf_counter() - start
            ) * 1000

        logger.info(
            f"Skill customer_escalation_summary "
            f"completed in {duration:.2f} ms"
        )