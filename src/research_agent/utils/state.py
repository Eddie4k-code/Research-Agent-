from typing_extensions import TypedDict, NotRequired, Annotated
from typing import Optional, List
from .objects import Analyst
from langgraph.graph import MessagesState
import operator

# State
class GenerateAnalystsState(TypedDict):
    topic: str # Research Topic
    max_analysts: int # Number of Analysts to Generate
    human_analyst_feedback: NotRequired[Optional[str]] # Human Feedback for what is generated
    analysts: NotRequired[Optional[List[Analyst]]] # List of Analysts

class InterviewState(MessagesState):
    max_num_turns: int # Number of turns of conversation
    context: Annotated[list, operator.add] # Source of docs
    analyst: Analyst # Analyst to interview
    interview: str # Interview transcript
    sections: list # final key we duplicate in outer state for Send() api


class ResearchState(TypedDict):
    topic: str
    max_analysts: int
    human_analyst_feedback: NotRequired[Optional[str]]
    analysts: List[Analyst]
    sections: Annotated[list, operator.add] # List of sections
    introduction: str
    content: str
    conclusion: str
    final_report: str