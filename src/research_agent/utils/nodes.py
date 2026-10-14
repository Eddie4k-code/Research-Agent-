from dotenv import load_dotenv
from langchain.messages import HumanMessage, SystemMessage

from .models import llm
from .objects import Analyst, Perspective
from .prompts import analyst_instructions
from .state import GenerateAnalystsState

load_dotenv()

def create_analyst(state: GenerateAnalystsState) -> dict:
    """
    Create Analysts
    """

    topic = state["topic"]
    max_analysts = state["max_analysts"]
    human_analyst_feedback = state.get("human_analyst_feedback", None)

    # Enforce Structed output
    structured_llm = llm.with_structured_output(Perspective)

    # System Message
    system_message = analyst_instructions.format(topic=topic, max_analysts=max_analysts, human_analyst_feedback=human_analyst_feedback or "")

    # Generate Analysts
    analysts = structured_llm.invoke([SystemMessage(system_message)]+[HumanMessage(content="Please Generate the set of analysts")])

    return {"analysts": analysts.analysts}