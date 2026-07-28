from crewai import Agent

class EditorAgent:
    def create_agent(self) -> Agent:
        return Agent(
            role='Editor de Conteúdo',
            goal='Revisar e melhorar artigos para máxima qualidade',
            backstory="""Você é um editor experiente com olhar crítico para qualidade.
            Especialista em avaliação de conteúdo, correção gramatical e melhoria de estilo.
            Aplica critérios rigorosos de qualidade em cada revisão.""",
            verbose=True,
            allow_delegation=True
        )
