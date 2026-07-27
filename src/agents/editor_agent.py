from crewai import Agent

import os

class EditorAgent:
    def create_agent(self) -> Agent:
        return Agent(
            role="Editor de Conteúdo",
            goal="Revisar, corrigir e refinar o artigo final para máxima qualidade",
            backstory="Você é um editor rigoroso que garante perfeição gramatical, tom correto e legibilidade perfeita.",
            verbose=True
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