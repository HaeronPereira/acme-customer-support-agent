from datetime import datetime
from typing import Optional
from typing import Literal
from pydantic import BaseModel, ConfigDict



class CustomerResponse(BaseModel):
    customer_id: int
    name: str
    industry: str
    contact_name: str
    contact_email: str
    account_manager: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)



class IssueResponse(BaseModel):
    issue_id: int
    customer_id: int
    title: str
    description: str
    priority: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ChatRequest(BaseModel):
    message: str
    conversation_id: str


class ChatResponse(BaseModel):
    response: str

class IntentResult(BaseModel):
    """
    Structured output returned by the intent classifier.
    """

    intent: Literal[
        "chat",
        "update_issue",
    ]

    issue_id: Optional[int] = None

    customer_name: Optional[str] = None

    status: Optional[
        Literal[
            "Open",
            "In Progress",
            "Resolved",
            "Closed",
        ]
    ] = None

class IssueStatusUpdate(BaseModel):
    status: str


class IssueUpdateResponse(BaseModel):
    issue_id: int
    status: str

    model_config = ConfigDict(from_attributes=True)

class NextActionCreate(BaseModel):
    issue_id: int
    action: str
    owner: str
    
class LoginRequest(BaseModel):
    username: str
    password: str
