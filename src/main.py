from fastapi import FastAPI
from src.api.routes import router as api_router

app = FastAPI(title="Pulso - Assistente de IA")

app.include_router(api_router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "Pulso online"}
