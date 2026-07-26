from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
import os

class TavilySearchTool(BaseTool):
    name: str = "Tavily Search"
    description: str = "Busca informações atualizadas na web usando Tavily API"
    
    def _run(self, query: str) -> str:
        api_key = os.getenv("TAVILY_API_KEY")
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": api_key,
            "query": query,
            "search_depth": "advanced",
            "max_results": 10
        }
        response = requests.post(url, json=payload)
        return str(response.json())

class SerperSearchTool(BaseTool):
    name: str = "Serper Search"
    description: str = "Busca em tempo real usando Serper API (Google Search)"
    
    def _run(self, query: str) -> str:
        api_key = os.getenv("SERPER_API_KEY")
        url = "https://google.serper.dev/search"
        headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
        payload = {"q": query, "num": 10}
        response = requests.post(url, json=payload, headers=headers)
        return str(response.json())