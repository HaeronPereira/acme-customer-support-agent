# AI Tool Usage Notes

## Overview

AI coding tools were used throughout the development of this project as an engineering assistant to accelerate implementation, review code structure, and explore alternative approaches. All architectural decisions, testing, validation, and final implementation decisions remained under my control.

## What was delegated to AI tools and why

AI tools were primarily used for:

- Exploring implementation approaches for FastAPI, LangGraph, MCP, and Redis integration.
- Generating boilerplate code and documentation.
- Reviewing code structure and identifying potential improvements.
- Explaining library behaviour and API usage.
- Assisting with troubleshooting during development.

Using AI for these tasks allowed development time to be focused on solution design, integration, debugging, and testing.

---

## Review, validation and testing

AI-generated suggestions were never accepted without verification.

All generated code was reviewed, integrated manually, and validated by:

- Running the application locally using Docker Compose.
- Testing REST endpoints through the Streamlit interface and FastAPI.
- Verifying authentication and role-based access control using Keycloak.
- Confirming database operations against PostgreSQL.
- Inspecting Redis conversation checkpoints.
- Reviewing LangSmith traces, structured logs, and latency measurements.

---

## Identifying and correcting AI errors

Where AI-generated suggestions were incorrect or incompatible with the chosen libraries, the implementation was corrected through debugging and testing.

Examples included:

- Resolving library compatibility issues during LangGraph and Redis integration.
- Correcting authentication and container configuration.
- Verifying framework behaviour against official documentation and runtime testing before adoption.

---

## Human oversight

For a client engagement, I would not rely on AI without human review for:

- Security-sensitive implementation.
- Authentication and authorization logic.
- Architectural decisions.
- Production deployment configuration.
- Client-specific business rules.

These areas require engineering judgement, testing, and validation before implementation.