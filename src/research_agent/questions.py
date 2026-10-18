from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph

from research_agent.utils.state import InterviewState
from .utils.edges import routes_messages
from .utils.nodes import (
    generate_answer,
    generate_question,
    save_interview,
    search_web,
    search_web2,
    write_section,
)

load_dotenv()

interview_builder = StateGraph(InterviewState)

interview_builder.add_node("ask_question", generate_question)
interview_builder.add_node("search_web", search_web)
interview_builder.add_node("search_web2", search_web2)
interview_builder.add_node("answer_question", generate_answer)
interview_builder.add_node("save_interview", save_interview)
interview_builder.add_node("write_section", write_section)

interview_builder.add_edge(START, "ask_question")
interview_builder.add_edge("ask_question", "search_web")
interview_builder.add_edge("ask_question", "search_web2")
interview_builder.add_edge("search_web", "answer_question")
interview_builder.add_edge("search_web2", "answer_question")
interview_builder.add_conditional_edges(
    "answer_question", routes_messages, ["ask_question", "save_interview"]
)
interview_builder.add_edge("save_interview", "write_section")
interview_builder.add_edge("write_section", END)

graph = interview_builder.compile()
