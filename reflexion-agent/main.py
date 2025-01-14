from dotenv import load_dotenv

from typing import List

from langchain_core.messages import BaseMessage, ToolMessage, HumanMessage
from langgraph.graph import END, MessageGraph

from chains import revisor, first_responder
from tool_exector import execute_tools

load_dotenv()

MAX_ITERATIONS = 2
builder = MessageGraph()
builder.add_node("draft", first_responder)
builder.add_node("execute_tools", execute_tools)
builder.add_node("revise", revisor)
builder.add_edge("draft", "execute_tools")
builder.add_edge("execute_tools", "revise")


def event_loop(state: List[BaseMessage]) -> str:
    count_tool_visits = sum(isinstance(item, ToolMessage) for item in state)

    if count_tool_visits < MAX_ITERATIONS:
        return "execute_tools"
    else:
        return END
    
builder.add_conditional_edges("revise", event_loop)
builder.set_entry_point("draft")

graph = builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

if __name__ == '__main__':
    print("Welcome to the graph boys")

    res = graph.invoke(
        "Write about AI-Powered SOC / autonomous soc problem domain, list startups that do that and raised capital."
    )
    
    print(res[-1].tool_calls[0]["args"]["answer"])