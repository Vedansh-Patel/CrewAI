import streamlit as st
import os
from crewai import Agent, Task, Crew
from crewai.tools import tool
from langchain_community.utilities.serpapi import SerpAPIWrapper
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
serpapi_api_key = os.getenv("SERPAPI_API_KEY")

llm = ChatGroq(
    groq_api_key=groq_api_key,
    model="llama-3.1-8b-instant"
)

@tool("SerpAPISearch")
def serpapi_search(query: str) -> str:
    """Search the web using SerpAPI and return results."""
    try:
        search = SerpAPIWrapper(serpapi_api_key=serpapi_api_key)
        return search.run(query)
    except Exception as e:
        return f"Search failed: {str(e)}"

planner = Agent(
    role="Planner",
    goal="Break down tasks and create a project plan for market research",
    backstory="An expert in project planning and strategic task delegation.",
    llm=llm,
    verbose=True,
)

researcher = Agent(
    role="Researcher",
    goal="Gather detailed information on LLM startups",
    backstory="A seasoned researcher focused on startup landscapes and AI trends.",
    tools=[serpapi_search],
    llm=llm,
    verbose=True,
)

writer = Agent(
    role="Writer",
    goal="Craft professional, clear, and insightful market reports",
    backstory="An experienced technical writer focused on AI and startup ecosystems.",
    llm=llm,
    verbose=True,
)

def run_crew():
    planning_task = Task(
        description=(
            "Break down the goal 'Write a market report on LLM startups' into clear subtasks. "
            "Specify what should be researched and how the report should be structured. "
            "Assign subtasks appropriately to the Researcher and Writer."
        ),
        expected_output="A set of subtasks assigned to the Researcher and Writer with clear objectives.",
        agent=planner
    )

    research_task = Task(
        description="Research the current LLM startup landscape including top players, funding rounds, products, and market trends.",
        expected_output="Detailed notes about top LLM startups, their differentiators, and the latest funding news.",
        agent=researcher
    )

    writing_task = Task(
        description="Write a professional market report on LLM startups using the research data provided.",
        expected_output="A cohesive and insightful market report tailored for investors or tech strategists.",
        agent=writer,
        context=[research_task]
    )

    crew = Crew(
        agents=[planner, researcher, writer],
        tasks=[planning_task, research_task, writing_task],
        verbose=True
    )

    try:
        output = crew.kickoff()
        return output
    except Exception as e:
        return f"Error running crew: {e}"

st.title("LLM Startup Report Generator")
if st.button("Generate Market Report"):
    with st.spinner("Running agents..."):
        result = run_crew()
    st.success("Done!")
    st.write(result)
