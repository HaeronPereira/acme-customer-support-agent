# AI Tool Usage Notes

## Overview

AI coding tools were used throughout the development of this project as an engineering assistant to accelerate implementation, review code structure, and explore alternative approaches. All architectural decisions, testing, validation, and final implementation decisions were decided by the user.

## What was delegated to AI tools and why

AI tools were primarily used for:

- Exploring implementation approaches for FastAPI, LangGraph, MCP, and Redis integration.
- Identifying potential improvements.
- Explaining library behaviour and API usage.
- Assisting with troubleshooting during development.
- Assisting with Document structure.     
Using AI for these tasks allowed development time to be focused on solution design, integration, debugging, and testing.

---

## Review, validation and testing

AI-generated suggestions were never accepted without verification.

All generated code was reviewed, tested and validated before integrating manually:

- Running the application locally using Docker Compose.
- Unit testing using pyton test files.
- Testing REST endpoints through the Streamlit interface and FastAPI.
- Verifying authentication and role-based access control using Keycloak.
- Confirming database operations against PostgreSQL.
- Inspecting Redis conversation checkpoints.
- Reviewing LangSmith traces, structured logs, and latency measurements.


---

## Identifying and correcting AI errors

Where AI-generated suggestions were incorrect or incompatible with our chosen libraries, we corrected the implementation thorough debugging and testing.

Key examples included:
- Resolving library compatibility issues during LangGraph and Redis integration.
- Correcting authentication flaws and container configurations.
- Verifying framework behavior against official documentation and runtime testing prior to adoption.
- Testing code modules in isolation before full system integration.
- Reviewing AI-generated code to understand its logic, ensuring it aligned with our architecture, and unit testing it before deployment.
- Using AI for documentation primarily to fix grammar, followed by proofreading to eliminate errors and hallucinations.

---

## Human oversight

For a client engagement, I would not rely on AI without human review for:

- Security-sensitive implementation like update or delete informations in database.
- Authentication and authorization logic - RBAC should be setup by system admin itself not agent.
- Architectural decisions.
- Production deployment configuration.
- Client-specific business rules.
