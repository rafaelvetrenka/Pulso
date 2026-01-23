# Pulso — Referências Operacionais (Comandos, Checklists e Rituais)

Este arquivo contém referências práticas para execução, validação e manutenção do Context Pack.
A estrutura é fixa; o conteúdo pode ser atualizado conforme o projeto evolui.

---

## 1) Checklists de validação (manual)

### 1.1 Checklist Swagger (regressão mínima)
1) `GET /api/health` → 200 e campos `status/service/version`
2) `POST /api/message` sem `X-API-Key` (com API_KEY setada) → 401
3) `POST /api/message` com `X-API-Key` correta → 200 e retorna `reply/session_id/handoff_required`
4) Confirmar header `X-Request-Id` na resposta do `/api/message`

### 1.2 Checklist Docker (máquina limpa)
- `docker compose up --build` sobe sem erro
- `/docs` abre
- endpoints passam no checklist Swagger

---

## 2) Comandos úteis

### 2.1 Docker
- Subir: `docker compose up --build`
- Parar: `docker compose down`
- Rebuild sem cache (só quando necessário): `docker compose build --no-cache`

### 2.2 Curl (exemplo message)
```bash
curl -i -X POST http://localhost:8000/api/message \
  -H "Content-Type: application/json" \
  -H "X-API-Key: <PULSO_API_KEY>" \
  -d '{"message":"teste"}'
