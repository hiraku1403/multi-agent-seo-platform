from crewai import Agent

from src.tools.search_tools import TavilySearchTool, SerperSearchTool
import os

class ResearcherAgent:
    def create_agent(self) -> Agent:
        return Agent(
            role="Pesquisador de SEO",
            goal="Buscar tendências e dados do mercado para o tópico fornecido",
            backstory="Você é um especialista em mineração de dados e análise de tendências de busca.",
            verbose=True
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
            llm=LLM(model="gemini/gemini-2.5-flash"),
            verbose=True,
            allow_delegation=True,
            max_iter=5
        )