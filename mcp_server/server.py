from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
#from app.skills.escalation_summary import customer_escalation_summary
from app.database import get_session
from app.logger import logger
import time
from app.services.customer_service import (
    get_customer_profile,
    get_open_issues,
    get_issue_history,
    get_recommended_next_actions,
)

security = TransportSecuritySettings(
    enable_dns_rebinding_protection=True,
    allowed_hosts=[
        "mcp",
        "mcp:8000",
        "localhost",
        "127.0.0.1",
    ],
    allowed_origins=["*"],
)

mcp = FastMCP(
    "ACME Support MCP",
    host="0.0.0.0",
    port=8000,
    transport_security=security,
)


@mcp.tool()
def customer_lookup(customer_name: str) -> dict:
    """
    Retrieve customer information using the customer's name.

    Use this tool whenever the user asks about a customer,
    their account, profile or company.
    """

    start = time.perf_counter()

    logger.info(
        f"MCP customer_lookup({customer_name})"
    )

    db = get_session()

    try:

        customer = get_customer_profile(
            db,
            customer_name,
        )

        if customer is None:
            return {
                "success": False,
                "error": "Customer not found",
            }

        return {
            "customer_id": customer.customer_id,
            "name": customer.name,
            "industry": customer.industry,
            "status": customer.status,
            "contact_name":customer.contact_name,
            "contact_email":customer.contact_email,
            "account_manager":customer.account_manager,
            "created_at":customer.created_at,

        }

    finally:
        db.close()
        duration = (
            time.perf_counter() - start
        ) * 1000

        logger.info(
            f"MCP customer_lookup completed in "
            f"{duration:.2f} ms"
        )

@mcp.tool()
def open_customer_issues(customer_name: str):
    """
    Retrieve all open issues for a customer.
    """
    start= time.perf_counter()
    db = get_session()
    logger.info(
    f"MCP open_customer_issues({customer_name})"
    )
    try:

        customer = get_customer_profile(
            db,
            customer_name,
        )

        if customer is None:
            return []

        issues = get_open_issues(
            db,
            customer.customer_id,
        )

        return [
            {
                "issue_id": i.issue_id,
                "title": i.title,
                "priority": i.priority,
                "status": i.status,
                "description": i.description
            }
            for i in issues
        ]

    finally:
        db.close()
        duration = (
            time.perf_counter() - start
        ) * 1000

        logger.info(
            f"MCP open_custommer_issues completed in "
            f"{duration:.2f} ms"
        )

@mcp.tool()
def issue_history(issue_id: int):
    """
    Retrieve the complete history for an issue.
    """

    start = time.perf_counter()

    logger.info(
    f"MCP issue_history({issue_id})"
    )
    db = get_session()

    try:
        
        history = get_issue_history(
            db,
            issue_id,
        )

        if history is None:
            return {
                "success": False,
                "error": "Issue not found",
            }

        return {
            "success": True,
            "issue_id": issue_id,
            "history": history,
        }

    finally:
        db.close()
        duration = (
            time.perf_counter() - start
        ) * 1000

        logger.info(
            f"MCP issue_history completed in "
            f"{duration:.2f} ms"
        )

@mcp.tool()
def recommended_next_actions(issue_id: int):
    """
    Retrieve the recommended next actions for an issue.
    """
    start =time.perf_counter()

    db = get_session()

    try:
        logger.info(
                "recommended_next_actions called for issue %s",
                issue_id,
            )
        actions = get_recommended_next_actions(
            db,
            issue_id,
        )

        return {
            "success": True,
            "issue_id": issue_id,
            "next_actions": actions,
        }

    finally:
        db.close()
        duration = (
            time.perf_counter() - start
        ) * 1000

        logger.info(
            f"MCP recomended_next_actions completed in "
            f"{duration:.2f} ms"
        )

app = mcp.streamable_http_app()
from starlette.middleware.base import BaseHTTPMiddleware


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print("METHOD:", request.method)
        print("PATH:", request.url.path)
        print("HOST:", request.headers.get("host"))
        print("CONTENT-TYPE:", request.headers.get("content-type"))
        response = await call_next(request)
        print("STATUS:", response.status_code)
        return response


app.add_middleware(LogMiddleware)