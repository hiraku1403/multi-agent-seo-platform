from crewai import Agent

import os



class WriterAgent:
    def create_agent(self) -> Agent:
        return Agent(
            role="Escritor de Conteúdo",
            goal="Escrever artigos engajadores e otimizados para SEO baseado na análise",
            backstory="Você é um redator profissional focado em criar conteúdo rico, informativo e fluído.",
            verbose=True
        )
        
    def create_agent(self):
        return Agent(
            role='Redator de Conteúdo',
            goal='Criar artigos otimizados e envolventes para SEO',
            backstory="""Você é um redator criativo com expertise em copywriting.
            Escreve artigos que combinam otimização para SEO com storytelling envolvente.
            Sabe adaptar o tom de voz para diferentes nichos e audiências.""",
            llm=LLM(model="gemini/gemini-2.5-flash"),
            verbose=True,
            allow_delegation=True
        )