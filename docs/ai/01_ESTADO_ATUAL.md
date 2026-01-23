# Pulso — Estado Atual do Projeto (Fonte Operacional)

Este arquivo descreve o ponto exato do projeto no repositório atual.
A estrutura deste documento é fixa; o conteúdo deve ser atualizado após cada sessão de desenvolvimento.

---

## 1) Resumo do ponto atual
- Backend em FastAPI está funcional e validado em Swagger.
- Contratos de API congelados (ver seção 3).
- Endpoint canônico de health implementado.
- Observabilidade mínima implementada (request_id + logs).
- Segurança mínima implementada (API Key no endpoint de mensagens).
- Sessões/mensagens ainda estão em memória (sem persistência real).

---

## 2) O que já está pronto (baseline estável)
- `GET /api/health` (canônico) retorna `status`, `service`, `version`.
- `GET /` é landing informativa (não-health).
- `POST /api/message` com contrato congelado:
  - Request: `message`, `session_id?`, `metadata?`
  - Response: `reply`, `session_id`, `handoff_required`
- Middleware adiciona `X-Request-Id` em todas as respostas e loga method/path/status/latency.
- API Key:
  - Com `PULSO_API_KEY` configurada: sem header → 401, com header correto → 200.
- Estrutura modular inicial:
  - `src/schemas/` (contratos)
  - `src/services/` (lógica)
  - `src/core/settings.py` e `src/core/security.py` (config e segurança)

---

## 3) Contratos congelados (NÃO QUEBRAR SEM VERSIONAMENTO)
### 3.1 `GET /api/health`
Response:
- `status: str`
- `service: str`
- `version: str`

### 3.2 `POST /api/message`
Request (MessageIn):
- `message: str` (min 1)
- `session_id: Optional[str]`
- `metadata: Optional[dict]`

Response (MessageOut):
- `reply: str`
- `session_id: str`
- `handoff_required: bool`

Observação:
- Mesmo que a implementação migre memória → Postgres → IA, o contrato externo deve permanecer estável.

---

## 4) Segurança e observabilidade (estado atual)
### 4.1 API Key
- Variável: `PULSO_API_KEY`
- Header exigido quando configurada: `X-API-Key: <valor>`
- Comportamento esperado:
  - sem header ou incorreto → 401
  - correto → 200

### 4.2 Request ID e logs
- Middleware:
  - usa `X-Request-Id` do request se existir, senão gera UUID
  - inclui `X-Request-Id` no response
  - loga: request_id, method, path, status, latency_ms

---

## 5) Estrutura do repositório (estado atual esperado)
A árvore abaixo representa a estrutura funcional após a evolução já validada:

- `Dockerfile`
- `docker-compose.yml`
- `requirements.txt`
- `.env.example`
- `.gitignore` (recomendado)
- `src/`
  - `main.py` (landing + middleware + include_router prefix `/api`)
  - `api/routes.py` (rotas finas: health + message)
  - `schemas/message.py` (MessageIn/MessageOut)
  - `services/messages.py` (handle_message)
  - `core/config.py` (SESSIONS em memória; temporário)
  - `core/settings.py` (SERVICE_NAME, APP_VERSION, API_KEY)
  - `core/security.py` (require_api_key)
  - `models/base.py` (placeholder)

---

## 6) Como rodar e validar (mínimo)
### 6.1 Docker (recomendado)
1) `cp .env.example .env`
2) Ajustar `PULSO_API_KEY` no `.env`
3) `docker compose up --build`
4) Validar:
- `http://localhost:8000/docs`
- `http://localhost:8000/api/health`
- `POST /api/message`:
  - sem key → 401
  - com key → 200
  - verificar `X-Request-Id` no response

### 6.2 Local (uvicorn)
- PowerShell: set env `PULSO_API_KEY` e rodar `uvicorn src.main:app --reload`

---

## 7) Ponto de parada (último marco)
- Contratos congelados + health canônico + landing padronizado.
- Schemas extraídos para `src/schemas`.
- Service layer introduzida.
- Middleware `X-Request-Id` + logs mínimos.
- API Key validada via Swagger (401/200).
- Commit consolidado realizado.

---

## 8) Maior lacuna técnica (prioridade máxima)
Persistência real:
- Sessões e mensagens ainda são em memória.
- Próximo salto: Postgres + SQLAlchemy + Alembic + models `sessions/messages`, migrando a lógica do service para DB sem quebrar contratos.
# Pulso — Estado Atual do Projeto (Fonte Operacional)

Este arquivo descreve o ponto exato do projeto no repositório atual.
A estrutura deste documento é fixa; o conteúdo deve ser atualizado após cada sessão de desenvolvimento.

---

## 1) Resumo do ponto atual
- Backend em FastAPI está funcional e validado em Swagger.
- Contratos de API congelados (ver seção 3).
- Endpoint canônico de health implementado.
- Observabilidade mínima implementada (request_id + logs).
- Segurança mínima implementada (API Key no endpoint de mensagens).
- Sessões/mensagens ainda estão em memória (sem persistência real).

---

## 2) O que já está pronto (baseline estável)
- `GET /api/health` (canônico) retorna `status`, `service`, `version`.
- `GET /` é landing informativa (não-health).
- `POST /api/message` com contrato congelado:
  - Request: `message`, `session_id?`, `metadata?`
  - Response: `reply`, `session_id`, `handoff_required`
- Middleware adiciona `X-Request-Id` em todas as respostas e loga method/path/status/latency.
- API Key:
  - Com `PULSO_API_KEY` configurada: sem header → 401, com header correto → 200.
- Estrutura modular inicial:
  - `src/schemas/` (contratos)
  - `src/services/` (lógica)
  - `src/core/settings.py` e `src/core/security.py` (config e segurança)

---

## 3) Contratos congelados (NÃO QUEBRAR SEM VERSIONAMENTO)
### 3.1 `GET /api/health`
Response:
- `status: str`
- `service: str`
- `version: str`

### 3.2 `POST /api/message`
Request (MessageIn):
- `message: str` (min 1)
- `session_id: Optional[str]`
- `metadata: Optional[dict]`

Response (MessageOut):
- `reply: str`
- `session_id: str`
- `handoff_required: bool`

Observação:
- Mesmo que a implementação migre memória → Postgres → IA, o contrato externo deve permanecer estável.

---

## 4) Segurança e observabilidade (estado atual)
### 4.1 API Key
- Variável: `PULSO_API_KEY`
- Header exigido quando configurada: `X-API-Key: <valor>`
- Comportamento esperado:
  - sem header ou incorreto → 401
  - correto → 200

### 4.2 Request ID e logs
- Middleware:
  - usa `X-Request-Id` do request se existir, senão gera UUID
  - inclui `X-Request-Id` no response
  - loga: request_id, method, path, status, latency_ms

---

## 5) Estrutura do repositório (estado atual esperado)
A árvore abaixo representa a estrutura funcional após a evolução já validada:

- `Dockerfile`
- `docker-compose.yml`
- `requirements.txt`
- `.env.example`
- `.gitignore` (recomendado)
- `src/`
  - `main.py` (landing + middleware + include_router prefix `/api`)
  - `api/routes.py` (rotas finas: health + message)
  - `schemas/message.py` (MessageIn/MessageOut)
  - `services/messages.py` (handle_message)
  - `core/config.py` (SESSIONS em memória; temporário)
  - `core/settings.py` (SERVICE_NAME, APP_VERSION, API_KEY)
  - `core/security.py` (require_api_key)
  - `models/base.py` (placeholder)

---

## 6) Como rodar e validar (mínimo)
### 6.1 Docker (recomendado)
1) `cp .env.example .env`
2) Ajustar `PULSO_API_KEY` no `.env`
3) `docker compose up --build`
4) Validar:
- `http://localhost:8000/docs`
- `http://localhost:8000/api/health`
- `POST /api/message`:
  - sem key → 401
  - com key → 200
  - verificar `X-Request-Id` no response

### 6.2 Local (uvicorn)
- PowerShell: set env `PULSO_API_KEY` e rodar `uvicorn src.main:app --reload`

---

## 7) Ponto de parada (último marco)
- Contratos congelados + health canônico + landing padronizado.
- Schemas extraídos para `src/schemas`.
- Service layer introduzida.
- Middleware `X-Request-Id` + logs mínimos.
- API Key validada via Swagger (401/200).
- Commit consolidado realizado.

---

## 8) Maior lacuna técnica (prioridade máxima)
Persistência real:
- Sessões e mensagens ainda são em memória.
- Próximo salto: Postgres + SQLAlchemy + Alembic + models `sessions/messages`, migrando a lógica do service para DB sem quebrar contratos.
