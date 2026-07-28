from crewai import Crew, Process
from src.agents.researcher_agent import ResearcherAgent
from src.agents.writer_agent import WriterAgent
from src.tasks.tasks import SEOTasks
import asyncio
from typing import Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SEOCrew:
    def __init__(self):
        # Usamos apenas 2 agentes agora para economizar tokens
        self.researcher = ResearcherAgent().create_agent()
        self.writer = WriterAgent().create_agent()
        
    async def run_seo_workflow(self, topic: str) -> Dict[str, Any]:
        try:
            logger.info(f"Iniciando análise SEO para: {topic}")
            
            # 1. Pesquisa e Análise de Palavras-Chave Unidas
            research_task = SEOTasks.research_task(self.researcher, topic)
            research_crew = Crew(agents=[self.researcher], tasks=[research_task], verbose=True)
            research_output = await research_crew.kickoff_async()
            research_result = research_output.raw
            logger.info("✅ Pesquisa e Análise SEO concluídas")
            
            # DELAY EXPANDIDO PARA LIMPAR O LIMITE DE MINUTOS DO GROQ
            await asyncio.sleep(5)
            
            # 2. Redação e Edição Final Unidas
            writing_task = SEOTasks.writing_task(self.writer, research_result)
            writing_crew = Crew(agents=[self.writer], tasks=[writing_task], verbose=True)
            writing_output = await writing_crew.kickoff_async()
            final_article = writing_output.raw
            logger.info("✅ Artigo finalizado e editado")
            
            return {
                "success": True,
                "topic": topic,
                "research": research_result,
                "seo_analysis": "Integrada na etapa de pesquisa",
                "article": final_article,
                "final_article": final_article
            }
            
        except Exception as e:
            logger.error(f"❌ Erro no workflow: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
