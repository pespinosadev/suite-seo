#!/usr/bin/env bash
set -euo pipefail

echo "[1/5] Pull..."
git pull origin main

echo "[2/5] Build..."
docker compose build

echo "[3/5] Up..."
docker compose up -d

echo "[4/5] Migrations..."
sleep 5
docker compose exec seo_api alembic upgrade head

echo "[5/5] Health check..."
for i in 1 2 3 4 5; do
  if curl -sf http://localhost:8000/api/health > /dev/null; then
    echo "Deploy OK."
    exit 0
  fi
  echo "Waiting... ($i/5)"
  sleep 3
done

echo "FAILED. Logs:"
docker compose logs --tail=50 seo_api
exit 1
