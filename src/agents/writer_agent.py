from crewai import Agent

class WriterAgent:
    def create_agent(self) -> Agent:
        return Agent(
            role='Redator de Conteúdo',
            goal='Criar artigos otimizados e envolventes para SEO',
            backstory="""Você é um redator criativo com expertise em copywriting.
            Escreve artigos que combinam otimização para SEO com storytelling envolvente.
            Sabe adaptar o tom de voz para diferentes nichos e audiências.""",
            verbose=True,
            allow_delegation=True
        )
