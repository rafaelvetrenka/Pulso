#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

API_BASE="${PULSO_API_BASE:-http://localhost:8000}"
HEALTH_URL="${API_BASE}/api/health"
MESSAGE_URL="${API_BASE}/api/message"

# Lê PULSO_API_KEY do .env (se existir)
API_KEY=""
if [[ -f ".env" ]]; then
  API_KEY="$(grep -E '^PULSO_API_KEY=' .env | head -n1 | cut -d'=' -f2- | tr -d '\r' || true)"
fi

echo "[verify] Using API_BASE=${API_BASE}"
if [[ -n "${API_KEY}" ]]; then
  echo "[verify] PULSO_API_KEY is set (protected mode)"
else
  echo "[verify] PULSO_API_KEY is empty (dev mode)"
fi

echo "[verify] Starting docker compose (detached)..."
docker compose up -d --build

echo "[verify] Waiting for health: ${HEALTH_URL}"
for i in {1..40}; do
  if curl -fsS "${HEALTH_URL}" >/dev/null 2>&1; then
    echo "[verify] Health OK"
    break
  fi
  sleep 1
  if [[ $i -eq 40 ]]; then
    echo "[verify] ERROR: health did not become ready"
    exit 1
  fi
done

echo "[verify] Checking /api/health response shape..."
health_json="$(curl -fsS "${HEALTH_URL}")"
echo "[verify] health: ${health_json}"
echo "${health_json}" | grep -q '"status"' || { echo "[verify] ERROR: health missing status"; exit 1; }
echo "${health_json}" | grep -q '"service"' || { echo "[verify] ERROR: health missing service"; exit 1; }
echo "${health_json}" | grep -q '"version"' || { echo "[verify] ERROR: health missing version"; exit 1; }

echo "[verify] Checking X-Request-Id header on /api/message..."
hdr="$(curl -sS -i -X POST "${MESSAGE_URL}" \
  -H "Content-Type: application/json" \
  ${API_KEY:+-H "X-API-Key: ${API_KEY}"} \
  -d '{"message":"verify"}' | tr -d '\r')"

echo "${hdr}" | grep -qi '^x-request-id:' || { echo "[verify] ERROR: missing X-Request-Id header"; exit 1; }

if [[ -n "${API_KEY}" ]]; then
  echo "[verify] Expect 401 without key..."
  code_no_key="$(curl -sS -o /dev/null -w "%{http_code}" -X POST "${MESSAGE_URL}" \
    -H "Content-Type: application/json" \
    -d '{"message":"no-key"}')"
  [[ "${code_no_key}" == "401" ]] || { echo "[verify] ERROR: expected 401 without key, got ${code_no_key}"; exit 1; }

  echo "[verify] Expect 200 with key..."
  code_with_key="$(curl -sS -o /dev/null -w "%{http_code}" -X POST "${MESSAGE_URL}" \
    -H "Content-Type: application/json" \
    -H "X-API-Key: ${API_KEY}" \
    -d '{"message":"with-key"}')"
  [[ "${code_with_key}" == "200" ]] || { echo "[verify] ERROR: expected 200 with key, got ${code_with_key}"; exit 1; }
else
  echo "[verify] Dev mode: expect 200 without key..."
  code_dev="$(curl -sS -o /dev/null -w "%{http_code}" -X POST "${MESSAGE_URL}" \
    -H "Content-Type: application/json" \
    -d '{"message":"dev"}')"
  [[ "${code_dev}" == "200" ]] || { echo "[verify] ERROR: expected 200 in dev mode, got ${code_dev}"; exit 1; }
fi

echo "[verify] OK — smoke checks passed."
