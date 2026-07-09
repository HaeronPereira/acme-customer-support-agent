from typing import Annotated, Optional

from typing_extensions import TypedDict

from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    Shared state across the LangGraph workflow.
    """

    messages: Annotated[list, add_messages]

    customer_name: Optional[str]

    customer_id: Optional[int]

    issue_id: Optional[int]

