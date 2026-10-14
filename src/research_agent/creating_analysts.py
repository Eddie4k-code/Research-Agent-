from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph

from research_agent.utils.nodes import create_analyst
from research_agent.utils.state import GenerateAnalystsState

load_dotenv()

# Create the Graph
# GenerateAnlysis state
# nodes
# edges no need / simple

builder = StateGraph(GenerateAnalystsState)

builder.add_node("create_analyst", create_analyst)

# Crate the analysts
builder.add_edge(START, "create_analyst")
builder.add_edge("create_analyst", END)

graph = builder.compile()


