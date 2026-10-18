from langgraph.graph import StateGraph, START, END
from .questions import interview_builder
from .utils.edges import initate_all_interviews
from .utils.state import ResearchState
from .utils.nodes import create_analyst, human_feedback, write_report, write_introduction, write_conclusion, finalize_report


# Add nodes and edges 
builder = StateGraph(ResearchState)

builder.add_node("create_analyst", create_analyst)
builder.add_node("human_feedback", human_feedback)
builder.add_node("conduct_interview", interview_builder.compile())
builder.add_node("write_report", write_report)
builder.add_node("write_introduction", write_introduction)
builder.add_node("write_conclusion", write_conclusion)
builder.add_node("finalize_report", finalize_report)


# Logic
builder.add_edge(START, "create_analyst")
builder.add_edge("create_analyst", "human_feedback")
builder.add_conditional_edges("human_feedback", initate_all_interviews, ["conduct_interview", "write_report"])
builder.add_edge("conduct_interview", "write_report")
builder.add_edge("write_report", "write_introduction")
builder.add_edge("write_introduction", "write_conclusion")
builder.add_edge("write_conclusion", "finalize_report")
builder.add_edge("finalize_report", END)

graph = builder.compile()




