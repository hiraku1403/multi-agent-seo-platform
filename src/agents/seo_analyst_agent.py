from crewai import Agent

from src.tools.seo_tools import KeywordAnalysisTool, CompetitorAnalysisTool
import os

class SEOAnalystAgent:
    def create_agent(self) -> Agent:
        return Agent(
            role="Analista de SEO",
            goal="Analisar dados de palavras-chave e estruturar a estratégia de SEO",
            backstory="Você é um analista sênior focado em otimização de mecanismos de busca e intenção do usuário.",
            verbose=True
        )
        
    def create_agent(self):
        return Agent(
            role='Analista de SEO Senior',
            goal='Identificar palavras-chave de baixa concorrência e oportunidades de conteúdo',
            backstory="""Você é especialista em SEO com mais de 10 anos de experiência.
            Já otimizou mais de 500 sites e possui profundo conhecimento em
            estratégias de conteúdo e análise de concorrência.""",
            tools=[
                KeywordAnalysisTool(),
                CompetitorAnalysisTool()
            ],
           llm=LLM(model="gemini/gemini-2.5-flash"),
            verbose=True,
            allow_delegation=True
        )