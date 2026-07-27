import os
# FORÇA O CREWAI A USAR A PASTA TEMPORÁRIA COM PERMISSÃO DE ESCRITA DA VERCEL
os.environ["CREWAI_STORAGE_DIR"] = "/tmp/crewai"
os.environ["XDG_DATA_HOME"] = "/tmp/.local/share"
os.environ["XDG_CACHE_HOME"] = "/tmp/.cache"

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
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

    # Encontra a pasta static ao lado da pasta api
current_dir = os.path.dirname(os.path.abspath(__file__)) # src/api
project_root = os.path.dirname(os.path.dirname(current_dir)) # Raiz
static_dir = os.path.join(project_root, "src", "static")

if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    html_path = os.path.join(project_root, "src", "static", "index.html")
    
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

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

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
