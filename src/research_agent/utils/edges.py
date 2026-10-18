from dotenv import load_dotenv
from langchain.messages import AIMessage
from langgraph.graph import END
from langgraph.types import Send
from .state import GenerateAnalystsState, InterviewState, ResearchState
from langchain.messages import HumanMessage


load_dotenv()

# Conditional edges
def should_continue(state: GenerateAnalystsState):
    """
    Return the next node to execute
    """

    human_analyst_feedback = state.get("human_analyst_feedback", None)

    if human_analyst_feedback:
        # Regenerate analysts with the context of the human feedback
        return "create_analyst"

    return END


def routes_messages(state: InterviewState):
    """Route between question and answer"""

    messages = state["messages"]

    max_num_turns = state.get("max_num_turns", 2)

    num_responses = len([m for m in messages if isinstance(m, AIMessage) and m.name == "expert"])

    if num_responses >= max_num_turns:
        return "save_interview"

    return "ask_question"



def initate_all_interviews(state: ResearchState):
    """
    This is the map step where we run each interview in sub graph using Send() api
    """


    human_analyst_feedback = state.get("human_analyst_feedback")

    if human_analyst_feedback:
        return "create_analyst"

    else:
        topic = state.get("topic")
        return [
            Send("conduct_interview", {
                "analyst": analyst,
                "messages": [HumanMessage(content=f"Please conduct an interview with the following analyst: {analyst.description}")]
            }) for analyst in state.get("analysts", [])
        ]

