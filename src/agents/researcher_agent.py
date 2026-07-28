from crewai import Agent
from src.tools.search_tools import TavilySearchTool

class ResearcherAgent:
    def create_agent(self) -> Agent:
        return Agent(
            role='Pesquisador de Tendências',
            goal='Identificar tendências emergentes e oportunidades de mercado no setor',
            backstory="""Você é um pesquisador especializado em análise de mercado digital.
            Possui experiência em identificar padrões de comportamento do consumidor,
            tendências tecnológicas e oportunidades de conteúdo inexploradas.""",
            tools=[TavilySearchTool()],
            verbose=True,
            allow_delegation=True,
            max_iter=5
        )
