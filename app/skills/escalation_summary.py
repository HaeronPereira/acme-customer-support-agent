from app.database import get_session
from app.llm import llm
import time
from app.logger import logger
from app.services.customer_service import (
    get_customer_profile,
    get_open_issues,
    get_issue_history,
    get_recommended_next_actions,
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
            actions = get_recommended_next_actions(db, issue.issue_id)

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
                    "next_actions": actions,
                }
            )

        prompt = f"""
        You are a Senior Customer Success Manager preparing an executive escalation report.

        Customer Profile:
        {customer}

        Issue Context:
        {context}

        Instructions:

        - Use ONLY the supplied data.
        - Never invent customer facts, issue history or engineering updates.
        - Existing Next Actions come directly from the database.
        - AI Recommended Next Steps must be clearly labelled as AI-generated recommendations and must not contradict Existing Next Actions (Database).
        - If information is unavailable, write "No information available."
        - Always include every heading exactly as shown below.

        # Executive Summary

        # Customer Health

        # Open Issues

        # Existing Next Actions (Database)

        # AI Recommended Next Steps

        # Business Risk

        # Missing Information

        # Overall Priority
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