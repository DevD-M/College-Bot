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
llm = ChatGroq(model="llama-3.1-8b-instant")
llm_with_tools = llm.bind_tools([search_bennett_info])

# ---- NODES ----
def call_llm(state: CollegeBotState):
    messages = state["messages"]
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SYSTEM_PROMPT] + messages
    
    tool_call_count = sum(1 for m in messages if isinstance(m, ToolMessage))
    
    try:
        if tool_call_count >= 3:
            # Limit hit ho gaya — LLM ko tools bind hi nahi karna, 
            # sirf available info se answer banane do
            response = llm.invoke(messages)
        else:
            response = llm_with_tools.invoke(messages)
    except Exception as e:
        response = AIMessage(content="Sorry, I had trouble processing that. Could you rephrase your question?")
    
    return {"messages": [response]}

def call_tool(state: CollegeBotState):
    print("DEBUG: call_tool node activated!")  # 🆕 yeh line add kar
    last_message = state["messages"][-1]
    tool_call = last_message.tool_calls[0]
    result = search_bennett_info.invoke(tool_call["args"])
    print(f"DEBUG: Tool returned: {result[:200]}")  # 🆕 yeh bhi add kar
    tool_message = ToolMessage(content=result, tool_call_id=tool_call["id"])
    return {"messages": [tool_message]}

# ---- CONDITIONAL EDGE ----
def should_continue(state: CollegeBotState):
    last_message = state["messages"][-1]
    tool_call_count = sum(1 for m in state["messages"] if isinstance(m, ToolMessage))
    
    if last_message.tool_calls and tool_call_count < 3:
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