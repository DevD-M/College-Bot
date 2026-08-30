import os
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict

from langchain_core.tools import tool
from langchain_core.messages import ToolMessage, SystemMessage, AIMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from retriever import retrieve

load_dotenv()
SYSTEM_PROMPT = SystemMessage(content="""You are CollegeBot, an assistant 
for Bennett University. Use the search tool ONCE per question. If the 
tool returns relevant information, use it to answer immediately — do not 
search again with different queries. Answer only based on the retrieved 
information.""")

# ---- TOOL ----
@tool
def search_bennett_info(query: str) -> str:
    """Search Bennett University's knowledge base for information about
    fees, admissions, courses, scholarships, hostels, campus life,
    placements, and other university-related topics.

    Use this tool when the user asks a specific question about Bennett
    University. Do NOT use this tool for greetings (hi, hello, how are you)
    or general conversation unrelated to Bennett University."""
    chunks = retrieve(query)
    return "\n\n".join(chunks)

# ---- STATE ----
class CollegeBotState(TypedDict):
    messages: Annotated[list, add_messages]

# ---- LLM + TOOLS ----
llm = ChatGroq(model="openai/gpt-oss-20b")
llm_with_tools = llm.bind_tools([search_bennett_info])

# ---- NODES ----
def call_llm(state: CollegeBotState):
    messages = state["messages"]
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SYSTEM_PROMPT] + messages

    tool_call_count = sum(1 for m in messages if isinstance(m, ToolMessage))

    try:
        # FIX: cap lowered from 3 -> 1. Ab safe hai kyunki tool result khud
        # mein explicit "don't search again" instruction carry karta hai
        # (see call_tool below), so LLM ko dobara confuse hone ki zarurat nahi.
        if tool_call_count >= 1:
            response = llm.invoke(messages)
        else:
            response = llm_with_tools.invoke(messages)
    except Exception as e:
        response = AIMessage(content="Sorry, I had trouble processing that. Could you rephrase your question?")

    return {"messages": [response]}

def call_tool(state: CollegeBotState):
    print("DEBUG: call_tool node activated!")
    last_message = state["messages"][-1]

    # FIX: handle ALL tool calls in this turn, not just tool_calls[0].
    # Groq models can emit parallel tool calls; previously only the first
    # one ever got a ToolMessage, leaving the graph in an incomplete state.
    tool_messages = []
    for tool_call in last_message.tool_calls:
        result = search_bennett_info.invoke(tool_call["args"])
        print(f"DEBUG: Tool returned: {result[:200]}")

        # FIX: inject explicit instruction into the tool result itself.
        # Root cause of the loop was that "search ONCE" only existed as a
        # soft system-prompt instruction — nothing at the code/state level
        # stopped the LLM from deciding a 2nd/3rd search was needed if it
        # judged the first result insufficient. Putting the instruction
        # directly in the ToolMessage gives the LLM a hard, local signal
        # right where it's making the next decision.
        annotated_result = (
            f"{result}\n\n"
            "[System note: This is the retrieved information for the query. "
            "Answer the user's question using ONLY this information. "
            "Do not call the search tool again for this question.]"
        )
        tool_messages.append(
            ToolMessage(content=annotated_result, tool_call_id=tool_call["id"])
        )

    return {"messages": tool_messages}

# ---- CONDITIONAL EDGE ----
def should_continue(state: CollegeBotState):
    last_message = state["messages"][-1]
    tool_call_count = sum(1 for m in state["messages"] if isinstance(m, ToolMessage))

    # FIX: cap lowered from 3 -> 1, matching call_llm's cap above.
    if last_message.tool_calls and tool_call_count < 1:
        return "call_tool"
    return "end"

# ---- GRAPH ----
graph = StateGraph(CollegeBotState)
graph.add_node("call_llm", call_llm)
graph.add_node("call_tool", call_tool)
graph.set_entry_point("call_llm")
graph.add_conditional_edges(
    "call_llm",
    should_continue,
    {"call_tool": "call_tool", "end": END}
)
graph.add_edge("call_tool", "call_llm")

app_graph = graph.compile()

# ---- TEST ----
if __name__ == "__main__":
    print("Agentic CollegeBot ready! Type 'quit' to exit\n")
    while True:
        question = input("You: ")
        if question.lower() == "quit":
            break
        result = app_graph.invoke({"messages": [("user", question)]})
        print(f"\nCollegeBot: {result['messages'][-1].content}\n")