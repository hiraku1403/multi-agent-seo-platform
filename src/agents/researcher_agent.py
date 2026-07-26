from crewai import Agent
from langchain_openai import ChatOpenAI
from src.tools.search_tools import TavilySearchTool, SerperSearchTool
import os

class ResearcherAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
    def create_agent(self):
        return Agent(
            role='Pesquisador de Tendências',
            goal='Identificar tendências emergentes e oportunidades de mercado no setor',
            backstory="""Você é um pesquisador especializado em análise de mercado digital.
            Possui experiência em identificar padrões de comportamento do consumidor,
            tendências tecnológicas e oportunidades de conteúdo inexploradas.""",
            tools=[
                TavilySearchTool(),
                SerperSearchTool()
            ],
            llm=self.llm,
            verbose=True,
            allow_delegation=True,
            max_iter=5
        )