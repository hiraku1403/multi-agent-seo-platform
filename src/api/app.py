import os
# Redirecionamento de permissão do CrewAI
os.environ["CREWAI_STORAGE_DIR"] = "/tmp/crewai"
os.environ["XDG_DATA_HOME"] = "/tmp/.local/share"
os.environ["XDG_CACHE_HOME"] = "/tmp/.cache"

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from src.crew.seo_crew import SEOCrew
import asyncio
import uvicorn
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

# DESCUBRA O CAMINHO DA PASTA STATIC AUTOMATICAMENTE
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Sobe para /src
STATIC_DIR = os.path.join(BASE_DIR, "static")

# MONTA A PASTA DE ESTRUTURAS ESTÁTICAS (ISSO OBRIGA A VERCEL A INCLUÍ-LA NO BUILD)
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def root():
    html_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(html_file):
        return FileResponse(html_file)
    return {"message": "🚀 Multi-Agent SEO Platform API", "status": "online", "info": "index.html nao encontrado na pasta static"}

@app.post("/api/generate-content", response_model=SEOResponse)
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