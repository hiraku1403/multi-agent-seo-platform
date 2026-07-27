from crewai import Agent, LLM
from langchain_openai import ChatOpenAI
import os

class EditorAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
    def create_agent(self):
        return Agent(
            role='Editor de Conteúdo',
            goal='Revisar e melhorar artigos para máxima qualidade',
            backstory="""Você é um editor experiente com olhar crítico para qualidade.
            Especialista em avaliação de conteúdo, correção gramatical e melhoria de estilo.
            Aplica critérios rigorosos de qualidade em cada revisão.""",
           llm=LLM(model="gemini/gemini-2.5-flash"),
            verbose=True,
            allow_delegation=True
        )