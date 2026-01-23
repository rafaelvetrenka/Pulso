# Pulso — Roadmap de Próximos Passos (Execução em Ordem)

Este arquivo define o roadmap operacional (ordem de execução) para evoluir o Pulso.
A estrutura é fixa; o conteúdo deve ser atualizado a cada sessão.

Regra: **Controle > Inteligência**.

---

## 1) Próximo passo imediato (1 item)
### [IMEDIATO] Validar onboarding em máquina limpa (PC de casa)
Objetivo:
- Garantir que qualquer dev consegue rodar o projeto do zero.

Ações:
- Instalar Git + Docker Desktop
- `git clone`
- `cp .env.example .env` + ajustar `PULSO_API_KEY`
- `docker compose up --build`
- Validar /docs, /api/health, /api/message (401/200) e X-Request-Id

Critério de aceite:
- Projeto sobe em < 10 minutos e passa no checklist Swagger sem ajustes manuais fora do README.

---

## 2) Próximos passos (ordem obrigatória)
### 2.1 Adicionar Postgres no docker-compose (sem alterar endpoints)
- Criar serviço `db` com volume persistente
- Introduzir `DATABASE_URL` em `.env.example`
Aceite:
- `docker compose up` sobe api + db; db persiste após restart.

### 2.2 Configurar SQLAlchemy (sync) + Alembic (migrations)
- Criar `src/core/db.py`
- Inicializar `migrations/`
- Documentar comandos de migration
Aceite:
- `alembic upgrade head` funciona e cria tabela(s) iniciais.

### 2.3 Implementar models: `sessions` e `messages`
- Tabelas mínimas com UUID e timestamps
Aceite:
- Inserção e leitura no DB confirmadas.

### 2.4 Migrar service layer de memória para DB (sem quebrar contrato)
- `handle_message` passa a gravar e ler histórico do DB
- Remover dependência de `SESSIONS` após validação
Aceite:
- reiniciar containers não perde histórico; mesmo session_id continua.

### 2.5 Testes mínimos + CI
- pytest smoke tests (health, auth 401/200, message schema)
- GitHub Actions
Aceite:
- PR não passa sem testes; regressões detectadas.

---

## 3) Fases posteriores (somente após persistência + testes)
### 3.1 IA controlada (Fase 3)
- `src/ia/client.py` único
- timeout, logs tokens, prompt fixo, policy anti-alucinação
- `handoff_required` acionado quando necessário

### 3.2 RAG (Fase 4)
- ingestão → chunking → embeddings → top-k → resposta com fontes
- decisão: pgvector vs externo

### 3.3 Handoff humano (Fase 5)
- payload padronizado (intenção, resumo, dados coletados, canal)

### 3.4 Widget (Fase 6)
- iframe isolado + segurança por domínio/tenant

### 3.5 Produção
- Nginx + HTTPS + rate limit + backups + observabilidade

---

## 4) Concluído (mover itens para cá ao finalizar)
- Contratos congelados (MessageIn/MessageOut).
- Health canônico em `/api/health`.
- Landing padronizada em `/`.
- Middleware `X-Request-Id` + logs mínimos.
- API Key validada (401/200).
- Schemas/services/core modularizados.
