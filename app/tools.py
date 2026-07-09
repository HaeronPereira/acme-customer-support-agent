from sqlalchemy.orm import Session
from langchain_core.tools import tool
from app.skills.escalation_summary import customer_escalation_summary
from app.database import get_session
from app.services.customer_service import (
    get_customer_profile,
    get_open_issues,
    get_issue_history,
    get_next_action,
    update_issue_status,
)



# ==========================================================
# LANGCHAIN TOOLS
# ==========================================================


@tool
def customer_escalation_summary_tool(customer_name: str) -> str:
    """
    Executive customer escalation summary.
    """
    return customer_escalation_summary(customer_name)


@tool
def update_issue_status_tool(
    issue_id: int,
    new_status: str,
    
) -> dict:
    """
    Update the status of an issue.
    """

    db = get_session()

    try:

        issue = update_issue_status(
            db,
            issue_id,
            new_status,
        )

        if issue is None:

            return {
                "success": False,
                "error": "Issue not found.",
            }

        return {
            "success": True,
            "message": f"Issue {issue_id} updated successfully."
        }

    finally:
        db.close()

# ==========================================================
# TOOL REGISTRY
# ==========================================================

TOOLS = [
      
    update_issue_status_tool,
    customer_escalation_summary_tool,
]