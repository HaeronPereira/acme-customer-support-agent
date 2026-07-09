import requests
import streamlit as st
import uuid
from app.config import API_URL

st.set_page_config(
    page_title="ACME Customer Support Agent",
    page_icon="🤖",
    layout="wide",
)

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "token" not in st.session_state:
    st.session_state.token = ""

if "user" not in st.session_state:
    st.session_state.user = None

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.title("🔐 Authentication")

    username = st.text_input("Username")

    password = st.text_input(
    "Password",
    type="password",
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Authenticate", use_container_width=True):

            try:
                  
                login = requests.post(
                    f"{API_URL}/login",
                    json={
                        "username": username,
                        "password": password,
                    },
                )

                if login.status_code != 200:
                    st.error("Invalid username or password")
                    st.stop()

                token = login.json()["access_token"]
                response = requests.get(
                    f"{API_URL}/me",
                    headers={
                        "Authorization": f"Bearer {token}"
                    },
                    timeout=30,
                )

                if response.status_code == 200:

                    st.session_state.token = token
                    st.session_state.user = response.json()

                    st.success("Authentication successful")

                else:

                    st.error("Authentication failed")

            except Exception as e:

                st.error(str(e))

    with col2:

        if st.button("Logout", use_container_width=True):

            st.session_state.user = None
            st.session_state.token = ""
            st.session_state.messages = []

            st.rerun()

    st.divider()

    if st.session_state.user:

        st.success("Authenticated")

        st.markdown("### User")

        st.write(st.session_state.user["name"])

        st.markdown("### Username")

        st.write(st.session_state.user["username"])

        st.markdown("### Role")

        st.write(", ".join(st.session_state.user["roles"]))

        st.markdown("### Conversation")
        st.code(st.session_state.conversation_id[:8])

    else:

        st.warning("Not authenticated")

    st.divider()

    st.subheader("🛠 Operations")

    issue_id = st.number_input(
        "Issue ID",
        min_value=1,
        value=1,
    )

    status = st.selectbox(
        "Status",
        [
            "Open",
            "In Progress",
            "Resolved",
            "Closed",
        ],
    )

    if st.button("Update Issue"):

        response = requests.patch(
            f"{API_URL}/issues/{issue_id}",
            json={
                "status": status,
            },
            headers={
                "Authorization":
                    f"Bearer {st.session_state.token}"
            },
        )

        if response.status_code == 200:

            st.success("Issue updated successfully")

        else:

            st.error(response.text)
    st.divider()

    next_issue = st.number_input(
        "Issue ID for Next Action",
        min_value=1,
        value=1,
    )

    action = st.text_input("Action")

    owner = st.text_input("Owner")
    if st.button("Create Next Action"):

        response = requests.post(
            f"{API_URL}/next-actions",
            json={
                "issue_id": next_issue,
                "action": action,
                "owner": owner,
            },
            headers={
                "Authorization":
                    f"Bearer {st.session_state.token}"
            },
        )

        if response.status_code == 200:

            st.success("Next Action created")

        else:

            st.error(response.text)
    st.divider()

    if st.button("🗑 New chat", use_container_width=True):

        st.session_state.messages = []
        st.session_state.conversation_id = str(uuid.uuid4())

        st.rerun()


# -----------------------------
# Main Page
# -----------------------------
st.title("🤖 ACME Customer Support Agent")

st.caption(
    "LangGraph • OpenAI • PostgreSQL • Redis • Keycloak"
)

st.markdown("### Example Questions")

examples = [
    "Show me all open issues for Nova Retail Ltd",
    "Give me an executive escalation summary for Orion Financial",
    "Show issue history for Customer Portal Login Failure",
    "What is the next action for Payment Gateway Timeout?",
]

for example in examples:

    st.markdown(f"- {example}")

st.divider()

# -----------------------------
# Authentication Required
# -----------------------------
if not st.session_state.user:

    st.info(
        "Authenticate using a Keycloak access token before using the assistant."
    )

    st.stop()


# -----------------------------
# Chat History
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# -----------------------------
# Chat Input
# -----------------------------
question = st.chat_input(
    "Ask a question..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    with st.spinner("Thinking..."):

        try:

            response = requests.post(
                f"{API_URL}/chat",
                json={
                    "message": question,
                    "conversation_id": st.session_state.conversation_id,
                },
                headers={
                    "Authorization":
                        f"Bearer {st.session_state.token}"
                },
                timeout=120,
            )

            if response.status_code == 200:

                answer = response.json()["response"]

            else:

                try:

                    answer = response.json()

                except Exception:

                    answer = response.text

        except Exception as e:

            answer = str(e)

    with st.chat_message("assistant"):

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    st.rerun()