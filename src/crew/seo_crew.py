from crewai import Crew, Process
from src.agents.researcher_agent import ResearcherAgent
from src.agents.seo_analyst_agent import SEOAnalystAgent
from src.agents.writer_agent import WriterAgent
from src.agents.editor_agent import EditorAgent
from src.tasks.tasks import SEOTasks
import asyncio
from typing import Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SEOCrew:
    def __init__(self):
        self.researcher = ResearcherAgent().create_agent()
        self.seo_analyst = SEOAnalystAgent().create_agent()
        self.writer = WriterAgent().create_agent()
        self.editor = EditorAgent().create_agent()
        
    async def run_seo_workflow(self, topic: str) -> Dict[str, Any]:
        """
        Executa o fluxo completo de otimização SEO
        """
        try:
            logger.info(f"Iniciando análise SEO para: {topic}")
            
            # 1. Pesquisa
            research_task = SEOTasks.research_task(self.researcher, topic)
            research_crew = Crew(
                agents=[self.researcher],
                tasks=[research_task],
                process=Process.sequential,
                verbose=True
            )
            research_result = research_crew.kickoff()
            logger.info("✅ Pesquisa concluída")
            
            # 2. Análise SEO
            seo_task = SEOTasks.seo_analysis_task(self.seo_analyst, research_result)
            seo_crew = Crew(
                agents=[self.seo_analyst],
                tasks=[seo_task],
                process=Process.sequential,
                verbose=True
            )
            seo_analysis = seo_crew.kickoff()
            logger.info("✅ Análise SEO concluída")
            
            # 3. Escrita
            writing_task = SEOTasks.writing_task(self.writer, seo_analysis)
            writing_crew = Crew(
                agents=[self.writer],
                tasks=[writing_task],
                process=Process.sequential,
                verbose=True
            )
            article = writing_crew.kickoff()
            logger.info("✅ Artigo escrito")
            
            # 4. Edição
            editing_task = SEOTasks.editing_task(self.editor, article)
            editing_crew = Crew(
                agents=[self.editor],
                tasks=[editing_task],
                process=Process.sequential,
                verbose=True
            )
            final_article = editing_crew.kickoff()
            logger.info("✅ Artigo revisado")
            
            return {
                "success": True,
                "topic": topic,
                "research": research_result,
                "seo_analysis": seo_analysis,
                "article": article,
                "final_article": final_article
            }
            
        except Exception as e:
            logger.error(f"❌ Erro no workflow: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }