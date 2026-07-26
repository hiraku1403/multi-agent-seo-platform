from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from bs4 import BeautifulSoup
import requests
import re
from collections import Counter

class KeywordAnalysisTool(BaseTool):
    name: str = "Keyword Analysis"
    description: str = "Analisa palavras-chave e sua dificuldade"
    
    def _run(self, keyword: str) -> str:
        # Simulação de análise de palavras-chave
        # Em produção, conectaria com APIs como Ahrefs ou SEMrush
        analysis = {
            "keyword": keyword,
            "search_volume": 1000,
            "difficulty": 45,
            "cpc": 2.50,
            "suggestions": [
                f"{keyword} guide",
                f"best {keyword}",
                f"{keyword} tutorial"
            ]
        }
        return str(analysis)

class CompetitorAnalysisTool(BaseTool):
    name: str = "Competitor Analysis"
    description: str = "Analisa conteúdo dos concorrentes"
    
    def _run(self, website: str) -> str:
        try:
            response = requests.get(website, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extrai palavras do título e cabeçalhos
            content = " ".join([soup.title.string if soup.title else "", 
                               " ".join([h.get_text() for h in soup.find_all(['h1', 'h2', 'h3'])])])
            
            words = re.findall(r'\w+', content.lower())
            common_words = Counter(words).most_common(10)
            
            return f"Análise do site {website}: Palavras mais comuns: {common_words}"
        except:
            return "Erro ao analisar o site do concorrente"