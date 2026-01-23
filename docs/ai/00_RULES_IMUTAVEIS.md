# Pulso — Regras Imutáveis de Desenvolvimento (AI Workflow)

Este arquivo define o protocolo de trabalho obrigatório para qualquer IA/agente que participe do desenvolvimento do Pulso.
NÃO ALTERAR este arquivo, exceto se o usuário instruir explicitamente.

---

## 1) Fonte de verdade
A IA deve usar como fonte de verdade:
1) O repositório atual (arquivos presentes no repo)
2) Os arquivos `docs/ai/*` (este pacote de contexto)

Se houver divergência entre o que a IA supõe e o repo, prevalece o repo.
Se houver divergência entre o repo e `docs/ai/*`, a IA deve:
- apontar a divergência de forma objetiva
- propor um passo de verificação (pedindo arquivo específico)
- e só então atualizar o pack (NUNCA alterar código fora de um passo aprovado).

---

## 2) Regra de ouro do projeto
**Controle > Inteligência**

Antes de IA avançada (LLM/RAG), garantir:
- contratos estáveis
- persistência
- observabilidade
- testes mínimos
- execução reproduzível

---

## 3) Protocolo obrigatório: Planejar → Agir → Revisar
A IA deve operar sempre neste ciclo disciplinado:

### 3.1 Planejar (spec antes do código)
- Confirmar requisitos e casos de borda
- Propor um mini-plano do passo (o que será alterado e como validar)
- Se faltar informação, pedir apenas o arquivo necessário (ex.: `docker-compose.yml`, `src/main.py`)

### 3.2 Agir (um passo por mensagem)
- Executar a menor mudança possível para avançar
- Evitar mudanças monolíticas
- Sempre entregar “arquivo inteiro” quando houver alteração de código

### 3.3 Revisar (validação objetiva)
- Exigir validação repetível (Swagger/curl/logs/teste)
- Não avançar sem validação do usuário

---

## 4) Formato obrigatório de cada resposta (UM PASSO por mensagem)
A IA só pode entregar **um passo por mensagem**, sempre no formato:

1) **PASSO X — Nome curto**
2) Objetivo do passo (1–2 linhas)
3) Contexto mínimo (por que este passo vem agora, alinhado ao roadmap)
4) Ações exatas (lista curta)
5) Código completo dos arquivos a criar/substituir (sempre arquivo inteiro; nunca trechos soltos)
6) Comandos exatos para rodar/testar
7) Critério de aceite (o que o usuário deve observar)
8) Encerramento pedindo resposta do usuário apenas com:
   - `PASSO X concluído`
   ou
   - erro/trace/print (para debugging)

**Regra de progressão:** a IA não pode avançar para o próximo passo até o usuário responder `PASSO X concluído`.

---

## 5) Regras de precisão (anti “vibe coding”)
- Não inventar arquivos, endpoints, contratos ou arquitetura.
- Não “assumir” que algo existe — pedir o arquivo quando necessário.
- Não quebrar contratos congelados sem versionamento explícito e justificativa.
- Toda mudança deve ter ao menos 1 gate de qualidade (Swagger/curl/log esperado/teste).
- Se houver risco alto, preferir passos menores e mais verificáveis.

---

## 6) Protocolo de commit
Quando o usuário pedir commit:
- propor mensagem de commit clara e pequena
- sugerir checklist pré-commit (build + validações mínimas)
- o usuário não deve commitar nada que não entenda e valide

---

## 7) Regra de escopo (quando solicitado)
Se a tarefa for “atualizar documentação do pack”, a IA só pode alterar `docs/ai/*` conforme definido em `docs/ai/03_REFERENCIAS.md` (ritual POST-SESSION UPDATE).
