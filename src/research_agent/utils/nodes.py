from dotenv import load_dotenv
from langchain.messages import HumanMessage, SystemMessage
from langgraph.types import interrupt

from .models import llm
from .objects import Analyst, Perspective, SearchQuery
from .prompts import (
    analyst_instructions,
    search_instructions,
    question_instructions,
    answer_instructions,
    section_writer_instructions,
    intro_conclusion_instructions,
    report_writer_instructions,
)
from .state import GenerateAnalystsState, InterviewState, ResearchState
from langchain_tavily import TavilySearch
from langchain_core.messages import get_buffer_string

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

def human_feedback(state: GenerateAnalystsState) -> dict:
    """
    Human gives feedback about the analysts
    """

    # Interrupt
    feedback = interrupt({
        "question": "Are these analysts okay for your research?",
        "analysts": [
            analyst.model_dump() if hasattr(analyst, "model_dump") else analyst for analyst in state.get("analysts", [])
        ],
        "instructions": "Return feedback to regenerate analysts or return empty/perfect/continue/okay to approve and continue the graph"
    })


    if feedback is None:
        return {"human_analyst_feedback": None}

    if isinstance(feedback, str):
        feedback = feedback.strip().lower()

        if feedback == "":
            return {"human_analyst_feedback": None}

        if feedback in {"perfect", "okay", "continue"}:
            return {"human_analyst_feedback": None}

        return {"human_analyst_feedback": feedback}

    return {"human_analyst_feedback": None}


def generate_question(state: InterviewState):
    """
    Node to generate the question
    """

    analyst = state["analyst"]

    if isinstance(analyst, dict):
        analyst = Analyst.model_validate(analyst)

    messages = state["messages"]

    # generate question
    system_message = question_instructions.format(goals=analyst.persona)

    question = llm.invoke([SystemMessage(system_message)]+messages)

    return {"messages": [question]}


def search_web(state: InterviewState):
    """
    Retrieve docs from the web
    """

    # Search Query
    structured_llm = llm.with_structured_output(SearchQuery)

    # Search Instruction
    search_instruction_system_message = SystemMessage(content=search_instructions)

    tavily_search = TavilySearch(max_results=3)

    search_query = structured_llm.invoke([search_instruction_system_message]+state["messages"])

    data = tavily_search.invoke({"query": search_query.search_query})

    search_docs = data.get("results", [])

    formatted_search_docs = "\n\n---\n\n".join(
        [f'<Document href="{doc["url"]}"/>\n{doc["content"]}' for doc in search_docs]
    )

    return {"context": [formatted_search_docs]}


def search_web2(state: InterviewState):
    """
    Retrieve docs from the web
    """

    # Search Query
    structured_llm = llm.with_structured_output(SearchQuery)

    # Search Instruction
    search_instruction_system_message = SystemMessage(content=search_instructions)

    tavily_search = TavilySearch(max_results=3)

    search_query = structured_llm.invoke([search_instruction_system_message]+state["messages"])

    data = tavily_search.invoke({"query": search_query.search_query})

    search_docs = data.get("results", [])

    formatted_search_docs = "\n\n---\n\n".join(
        [f'<Document href="{doc["url"]}"/>\n{doc["content"]}' for doc in search_docs]
    )

    return {"context": [formatted_search_docs]}


def generate_answer(state: InterviewState):
    
    """ Node to answer a question """

    # Get state
    analyst = state["analyst"]
    messages = state["messages"]
    context = state["context"]

    if isinstance(analyst, dict):
            analyst = Analyst.model_validate(analyst)

    # Answer question
    system_message = answer_instructions.format(goals=analyst.persona, context=context)
    answer = llm.invoke([SystemMessage(content=system_message)]+messages)
            
    # Name the message as coming from the expert
    answer.name = "expert"
    
    # Append it to state
    return {"messages": [answer]}

def save_interview(state: InterviewState):
    """ Save interviews """

    # Get messages
    messages = state["messages"]
    
    # Convert interview to a string
    interview = get_buffer_string(messages)
    
    # Save to interviews key
    return {"interview": interview}

tavily_search = TavilySearch(max_results=3)

search_instructions_system_message = SystemMessage(content=search_instructions)


def write_section(state: InterviewState):
    """ Node to answer a question """
    # Get state
    interview = state["interview"]
    context = state["context"]
    analyst = state["analyst"]

    if isinstance(analyst, dict):
            analyst = Analyst.model_validate(analyst)
    
    # Write section using either the gathered source docs from interview (context) or the interview itself (interview)
    system_message = section_writer_instructions.format(focus=analyst.description)
    section = llm.invoke([SystemMessage(content=system_message)]+[HumanMessage(content=f"Use this source to write your section: {context}")]) 


def write_report(state: ResearchState):
    """ Node to write the report """

    sections = state["sections"] # all the interviews which occurred in the graph
    topic = state["topic"]

    formatted_str_sections = "\n\n---\n\n".join(f"{section}" for section in sections)

    system_message = report_writer_instructions.format(topic=topic, context=formatted_str_sections)

    report = llm.invoke([SystemMessage(content=system_message)]+[HumanMessage(content=f"Write a report based on these memos.")])

    return {"content": report.content}


def write_introduction(state: ResearchState):
    # Full set of sections
    sections = state["sections"]
    topic = state["topic"]

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])
    
    # Summarize the sections into a final report
    
    instructions = intro_conclusion_instructions.format(topic=topic, formatted_str_sections=formatted_str_sections)    
    intro = llm.invoke([instructions]+[HumanMessage(content=f"Write the report introduction")]) 
    return {"introduction": intro.content}

def write_conclusion(state: ResearchState):

    # Full set of sections
    sections = state["sections"]
    topic = state["topic"]

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])
    
    # Summarize the sections into a final report
    
    instructions = intro_conclusion_instructions.format(topic=topic, formatted_str_sections=formatted_str_sections)    
    conclusion = llm.invoke([instructions]+[HumanMessage(content=f"Write the report conclusion")]) 
    return {"conclusion": conclusion.content}


def finalize_report(state: ResearchState):
    content = state["content"]

    final_report = state["introduction"] + "\n\n" + content + "\n\n" + state["conclusion"]

    return {"final_report": final_report}





