from crewai import Agent, LLM
from langchain_openai import ChatOpenAI
from src.tools.seo_tools import KeywordAnalysisTool, CompetitorAnalysisTool
import os

class SEOAnalystAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            api_key=os.getenv("OPENAI_API_KEY")
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