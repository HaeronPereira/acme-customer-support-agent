from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from app.checkpointer import initialize_checkpointer,shutdown_checkpointer
from app.agent import chat, get_graph
from app.schemas import ChatRequest, ChatResponse, IssueStatusUpdate, IssueUpdateResponse,LoginRequest, NextActionCreate
from app.database import get_db
from app.auth import get_current_user, login
from app.rbac import require_role
from app.logger import logger
import time
from app.intent_router import detect_intent
from app.schemas import CustomerResponse, IssueResponse
from app.services.customer_service import (
    get_customer_profile,
    get_open_issues,
    update_issue_status,
    create_next_action,
)

app = FastAPI(
    title="Acme Operations AI Assistant",
    version="1.0.0",
)


@app.middleware("http")
async def log_requests(request, call_next):

    start = time.perf_counter()

    logger.info(
        f"Incoming {request.method} {request.url.path}"
    )

    try:

        response = await call_next(request)

    except Exception as ex:

        logger.exception(ex)

        raise

    duration = (
        time.perf_counter() - start
    ) * 1000

    logger.info(
        f"{request.method} {request.url.path} "
        f"{response.status_code} "
        f"{duration:.2f} ms"
    )

    return response

@app.get("/")
def root():
    return {
        "message": "Acme Operations AI Assistant API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get(
    "/customers/{customer_name}",
    response_model=CustomerResponse,
)
def customer_profile(
    customer_name: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    require_role(
        user,
        [
            "sales_user",
            "support_user",
            "admin",
        ],
    )

    customer = get_customer_profile(db, customer_name)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


@app.get(
    "/customers/{customer_id}/issues",
    response_model=list[IssueResponse],
    
)
def customer_issues(
    customer_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    require_role(
        user,
        [
            "sales_user",
            "support_user",
            "admin",
        ],
    )
    return get_open_issues(db, customer_id)


@app.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat_endpoint(
    request: ChatRequest,
    user=Depends(get_current_user),
):
    logger.info(
        "User %s asked: %s",
        user["username"],
        request.message,
    )

    # --------------------------------------------------
    # Detect issue update requests
    # --------------------------------------------------
    intent = await detect_intent(request.message)
    
    if intent.intent=="update_issue":

        require_role(
            user,
            [
                "support_user",
                "admin",
            ],
        )


        db = next(get_db())

        try:

            if intent.issue_id:

                issue = update_issue_status(
                    db,
                    intent.issue_id,
                    intent.status,
                )

            else:

                return ChatResponse(
                    response=(
                        "Please specify the issue ID."
                    )
                )

        finally:

            db.close()

        if issue is None:

            return ChatResponse(
                response="Issue not found."
            )

        return ChatResponse(
            response=(
                f"✅ Issue {issue.issue_id} "
                f"updated to "
                f"{intent.status}."
            )
        )

    
    session_id = (
        f"{user['username']}:{request.conversation_id}"
    )

    answer = await chat(
        request.message,
        session_id=session_id,
    )

    return ChatResponse(
        response=answer
    )

@app.on_event("startup")
async def startup():
    await get_graph()
    await initialize_checkpointer()

@app.on_event("shutdown")
async def shutdown():
    await shutdown_checkpointer()

@app.get("/me")
def me(user=Depends(get_current_user)):
    return user



@app.patch(
    "/issues/{issue_id}",
    response_model=IssueUpdateResponse,
)
def update_issue(
    issue_id: int,
    request: IssueStatusUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    require_role(
        user,
        ["support_user", "admin"],
    )

    issue = update_issue_status(
        db,
        issue_id,
        request.status,
    )

    if issue is None:
        raise HTTPException(
            status_code=404,
            detail="Issue not found",
        )

    return issue

@app.post("/next-actions")
def create_action(
    request: NextActionCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    require_role(
        user,
        ["admin"],
    )

    return create_next_action(
        db,
        request.issue_id,
        request.action,
        request.owner,
    )

@app.post("/login")
def login_endpoint(request: LoginRequest):

    return login(
        request.username,
        request.password,
    )
