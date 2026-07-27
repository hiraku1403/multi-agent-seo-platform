from crewai import Agent
from langchain_openai import ChatOpenAI
import os

class WriterAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.8,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
    def create_agent(self):
        return Agent(
            role='Redator de Conteúdo',
            goal='Criar artigos otimizados e envolventes para SEO',
            backstory="""Você é um redator criativo com expertise em copywriting.
            Escreve artigos que combinam otimização para SEO com storytelling envolvente.
            Sabe adaptar o tom de voz para diferentes nichos e audiências.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=True
        )