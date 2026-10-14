from typing_extensions import TypedDict, NotRequired
from typing import Optional

# State
class GenerateAnalystsState(TypedDict):
    topic: str # Research Topic
    max_analysts: int # Number of Analysts to Generate
    human_analyst_feedback: NotRequired[Optional[str]] # Human Feedback for what is generated