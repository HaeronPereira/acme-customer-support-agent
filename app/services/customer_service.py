from sqlalchemy.orm import Session

from app.models import (
    Customer,
    Issue,
    IssueUpdate,
    NextAction,
)



# ==========================================================
# DATABASE FUNCTIONS
# ==========================================================

def get_customer_profile(db: Session, customer_name: str):
    """
    Retrieve a customer using their name.
    """
    return (
        db.query(Customer)
        .filter(Customer.name.ilike(f"%{customer_name}%"))
        .first()
    )


def get_open_issues(db: Session, customer_id: int):
    """
    Retrieve all open issues for a customer.
    """
    return (
        db.query(Issue)
        .filter(
            Issue.customer_id == customer_id,
            Issue.status == "Open",
        )
        .all()
    )



def get_next_action(db: Session, issue_id: int):
    """
    Retrieve the next action for an issue.
    """
    return (
        db.query(NextAction)
        .filter(NextAction.issue_id == issue_id)
        .first()
    )


def update_issue_status(db: Session, issue_id: int, new_status: str):
    """
    Update the status of an issue.
    """

    issue = (
        db.query(Issue)
        .filter(Issue.issue_id == issue_id)
        .first()
    )

    if issue is None:
        return None

    issue.status = new_status

    db.commit()
    db.refresh(issue)

    return issue

def create_next_action(
    db: Session,
    issue_id: int,
    action: str,
    owner: str,
    ):

    next_action = NextAction(
        issue_id=issue_id,
        action=action,
        owner=owner,
    )

    db.add(next_action)

    db.commit()

    db.refresh(next_action)

    return next_action

def get_issue_history(
    db,
    issue_id: int,
):
    """
    Return the update history for an issue.
    """

    issue = (
        db.query(Issue)
        .filter(Issue.issue_id == issue_id)
        .first()
    )

    if issue is None:
        return None

    return [
        {
            "updated_by": update.updated_by,
            "update_text": update.update_text,
            "created_at": (
                update.created_at.isoformat()
                if update.created_at
                else None
            ),
        }
        for update in issue.updates
    ]

def get_recommended_next_actions(
    db,
    issue_id: int,
):
    """
    Retrieve all recommended next actions for an issue.
    """

    actions = (
        db.query(NextAction)
        .filter(
            NextAction.issue_id == issue_id
        )
        .all()
    )

    return [
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
        for action in actions
    ]