import asyncio
from langchain_core.messages import SystemMessage

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from app.mcp_client import get_mcp_tools
from app.llm import llm
from app.prompts import SYSTEM_PROMPT
from app.state import AgentState
from app.tools import TOOLS
from app.checkpointer import initialize_checkpointer
from app.logger import logger



graph = None
llm_with_tools = None
tool_node = None



async def chatbot(state: AgentState):
    """
    Main LLM node.
    """
    logger.info("Invoking LangGraph")
    response = await llm_with_tools.ainvoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            *state["messages"],
        ]
    )
    logger.info("LangGraph completed")
    return {
        "messages": [response]
    }



async def get_graph():

    global graph
    global llm_with_tools
    global tool_node

    if graph is not None:
        return graph

    checkpointer = await initialize_checkpointer()

    mcp_tools = await get_mcp_tools()

    all_tools = TOOLS + mcp_tools

    llm_with_tools = llm.bind_tools(all_tools)

    tool_node = ToolNode(all_tools)

    builder = StateGraph(AgentState)

    builder.add_node("chatbot", chatbot)

    builder.add_node("tools", tool_node)

    builder.add_edge(
        START,
        "chatbot",
    )

    builder.add_conditional_edges(
        "chatbot",
        tools_condition,
    )

    builder.add_edge(
        "tools",
        "chatbot",
    )

    builder.add_edge(
        "chatbot",
        END,
    )

    graph = builder.compile(
        checkpointer=checkpointer,
        name="acme_customer_support_agent",
    )

    return graph

async def chat(
    user_message: str,
    session_id: str = "default",
):

    config = {
        "configurable": {
            "thread_id": session_id
        }
    }
    graph = await get_graph()
    result = await graph.ainvoke(
        {
            "messages": [
                (
                    "user",
                    user_message,
                )
            ]
        },
        config=config,
    )

    return result["messages"][-1].content