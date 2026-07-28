from crewai import Agent
from src.tools.seo_tools import KeywordAnalysisTool, CompetitorAnalysisTool

class SEOAnalystAgent:
    def create_agent(self) -> Agent:
        return Agent(
            role="Analista de SEO",
            goal="Analisar dados de palavras-chave e estruturar a estratégia de SEO",
            backstory="Você é um analista sênior focado em otimização de mecanismos de busca e intenção do usuário.",
            tools=[KeywordAnalysisTool(), CompetitorAnalysisTool()],
            verbose=True
        )
