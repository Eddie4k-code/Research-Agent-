from dotenv import load_dotenv
from .state import GenerateAnalystsState
from typing import Literal
from langgraph.graph import END


load_dotenv()

# Conditional edges
def should_continue(state: GenerateAnalystsState):
    """
    Return the next node to execute
    """

    human_analyst_feedback = state.get("human_analyst_feedback", None)

    if human_analyst_feedback:
        # Regenerate analysts with the context of the human feedback
        return "create_analysts"

    return END


