import time
import uuid
import logging
from fastapi import FastAPI, Request
from src.api.routes import router

# logger básico
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("pulso")

app = FastAPI(title="Pulso - Assistente de IA")

# Router da API
app.include_router(router, prefix="/api")


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    start = time.time()

    # Usa request id do cliente se vier, senão gera
    request_id = request.headers.get("X-Request-Id") or str(uuid.uuid4())
    request.state.request_id = request_id

    response = await call_next(request)

    elapsed_ms = int((time.time() - start) * 1000)

    # Header de resposta para debug/trace
    response.headers["X-Request-Id"] = request_id

    logger.info(
        "request_id=%s method=%s path=%s status=%s latency_ms=%s",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
    )
    return response


# Landing page (opcional) — não é health
@app.get("/", tags=["default"])
def landing():
    return {
        "service": "pulso",
        "message": "Pulso API online. Use /docs para Swagger e /api/health para health check."
    }
