from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.crew.seo_crew import SEOCrew
import asyncio
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Multi-Agent SEO Platform", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SEORequest(BaseModel):
    topic: str

class SEOResponse(BaseModel):
    success: bool
    topic: str
    research: str = None
    seo_analysis: str = None
    article: str = None
    final_article: str = None
    error: str = None

@app.get("/")
async def root():
    return {"message": "🚀 Multi-Agent SEO Platform API", "status": "online"}

@app.post("/generate-content", response_model=SEOResponse)
async def generate_content(request: SEORequest):
    """
    Gera conteúdo otimizado para SEO usando sistema multi-agente
    """
    try:
        crew = SEOCrew()
        result = await crew.run_seo_workflow(request.topic)
        
        if result["success"]:
            return SEOResponse(
                success=True,
                topic=result["topic"],
                research=result.get("research"),
                seo_analysis=result.get("seo_analysis"),
                article=result.get("article"),
                final_article=result.get("final_article")
            )
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Erro desconhecido"))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)