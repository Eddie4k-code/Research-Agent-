from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph

from research_agent.utils.nodes import create_analyst
from research_agent.utils.state import GenerateAnalystsState
from .utils.edges import should_continue
from .utils.nodes import human_feedback


load_dotenv()

# Create the Graph
# GenerateAnlysis state
# nodes
# edges no need / simple

builder = StateGraph(GenerateAnalystsState)

builder.add_node("create_analyst", create_analyst)
builder.add_node("human_feedback", human_feedback)

# Crate the analysts
builder.add_edge(START, "create_analyst")
builder.add_edge("create_analyst", "human_feedback")
builder.add_conditional_edges("human_feedback", should_continue)

graph = builder.compile()


