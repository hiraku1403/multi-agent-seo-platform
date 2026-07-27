import os
# CONFIGURAÇÃO DE PASTAS DE CACHE E DIRETÓRIO HOME PERMITIDO NA VERCEL
os.environ["CREWAI_STORAGE_DIR"] = "/tmp/crewai"
os.environ["XDG_DATA_HOME"] = "/tmp/.local/share"
os.environ["XDG_CACHE_HOME"] = "/tmp/.cache"
os.environ["XDG_CONFIG_HOME"] = "/tmp/.config"
os.environ["HOME"] = "/tmp"  # Resolve definitivamente o erro Read-only file system
os.environ["NUMEXPR_MAX_THREADS"] = "1"

# REMOVIDO: A linha os.environ["OPENAI_API_BASE"] foi excluída para o LiteLLM usar o padrão correto nativo.



from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from src.crew.seo_crew import SEOCrew
import asyncio
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

# DESCUBRA O CAMINHO DA PASTA STATIC E ADICIONE O MOUNT (CORREÇÃO DO 404)
current_dir = os.path.dirname(os.path.abspath(__file__)) # src/api
project_root = os.path.dirname(current_dir) # src
static_dir = os.path.join(project_root, "static")

if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Banco de dados temporário em memória para salvar os resultados
jobs = {}

class SEORequest(BaseModel):
    topic: str

class SEOResponse(BaseModel):
    success: bool
    status: str
    topic: str
    research: str = None
    seo_analysis: str = None
    article: str = None
    final_article: str = None
    error: str = None

async def run_crew_in_background(job_id: str, topic: str):
    try:
        crew = SEOCrew()
        result = await crew.run_seo_workflow(topic)
        jobs[job_id] = result
    except Exception as e:
        jobs[job_id] = {"success": False, "error": str(e), "topic": topic}

@app.get("/", response_class=HTMLResponse)
async def root():
    html_path = os.path.join(static_dir, "index.html")
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        return HTMLResponse(content=f"<h1>Erro ao carregar a interface</h1><p>O arquivo nao foi localizado em: {html_path}</p>")

@app.post("/api/generate-content")
async def generate_content(request: SEORequest, background_tasks: BackgroundTasks):
    job_id = "".join(e for e in request.topic if e.isalnum()).lower()
    jobs[job_id] = {"success": False, "status": "processing", "topic": request.topic}
    background_tasks.add_task(run_crew_in_background, job_id, request.topic)
    return {"job_id": job_id, "status": "processing"}

@app.get("/api/job/{job_id}")
async def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Trabalho não encontrado")
    
    job_data = jobs[job_id]
    if job_data.get("status") == "processing":
        return {"success": False, "status": "processing", "topic": job_data["topic"]}
        
    # Retorna o dicionário de dados bruto direto para o frontend, convertendo tudo para string por segurança
    return {
        "success": bool(job_data.get("success", False)),
        "status": "completed",
        "topic": str(job_data.get("topic", "")),
        "research": str(job_data.get("research", "")),
        "seo_analysis": str(job_data.get("seo_analysis", "")),
        "article": str(job_data.get("article", "")),
        "final_article": str(job_data.get("final_article", "")),
        "error": str(job_data.get("error", "")) if job_data.get("error") else None
    }


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}
