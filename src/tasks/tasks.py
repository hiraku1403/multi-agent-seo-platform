from crewai import Task
from typing import List

class SEOTasks:
    @staticmethod
    def research_task(agent, topic: str):
        return Task(
            description=f"""
            Pesquise profundamente sobre '{topic}':
            1. Identifique 5 tendências emergentes
            2. Liste 3 principais concorrentes
            3. Encontre 10 palavras-chave relacionadas
            4. Identifique gaps de conteúdo
            
            Use ferramentas de pesquisa para obter dados atualizados.
            """,
            agent=agent,
            expected_output="Relatório detalhado da pesquisa"
        )
    
    @staticmethod
    def seo_analysis_task(agent, research_result: str):
        return Task(
            description=f"""
            Com base na pesquisa: {research_result}
            1. Analise as palavras-chave encontradas
            2. Determine dificuldade e oportunidade de cada uma
            3. Identifique tópicos com alto potencial
            4. Sugira estrutura de conteúdo
            
            Foque em palavras-chave de baixa concorrência.
            """,
            agent=agent,
            expected_output="Análise SEO e recomendação de tópicos"
        )
    
    @staticmethod
    def writing_task(agent, seo_analysis: str):
        return Task(
            description=f"""
            Com base na análise SEO: {seo_analysis}
            Escreva um artigo completo em Markdown:
            1. Título otimizado
            2. Introdução envolvente
            3. Subtítulos com palavras-chave
            4. Conteúdo de 1500+ palavras
            5. Conclusão com call-to-action
            
            Mantenha tom profissional mas acessível.
            """,
            agent=agent,
            expected_output="Artigo completo em Markdown"
        )
    
    @staticmethod
    def editing_task(agent, article: str):
        return Task(
            description=f"""
            Revise e melhore este artigo: {article}
            1. Avalie qualidade (0-10)
            2. Corrija erros gramaticais
            3. Melhore a fluidez do texto
            4. Sugira melhorias de conteúdo
            5. Verifique otimização SEO
            
            Forneça feedback detalhado com nota.
            """,
            agent=agent,
            expected_output="Versão revisada do artigo com notas"
        )