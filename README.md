# Suite SEO

Dashboard SEO interno para Prensa Ibérica.

## Stack
FastAPI · PostgreSQL · Alembic · Docker · Caddy

## Estructura
- [backend/](backend/) — API FastAPI

## VPS — Primera vez

```bash
git clone https://github.com/TU_USUARIO/suite-seo.git /opt/suite-seo
cd /opt/suite-seo

# Crear .env con valores reales (ver .env.example)
cp .env.example .env
nano .env
# Generar SECRET_KEY: python3 -c "import secrets; print(secrets.token_hex(32))"

# Arrancar BD y aplicar migraciones
docker compose up -d seo_db
sleep 5
docker compose run --rm seo_api alembic upgrade head

# Arrancar API
docker compose up -d seo_api

# Crear primer usuario admin
docker compose exec seo_api python -m app.core.create_user \
  --email admin@tudominio.com \
  --password "password-seguro" \
  --role admin

# Añadir bloque /api/* al Caddyfile (ver Caddyfile.snippet) y recargar
caddy reload
```

## Deploys sucesivos

```bash
cd /opt/suite-seo
bash deploy.sh
```

## Verificación

```bash
curl https://tu-dominio.com/api/health

curl -X POST https://tu-dominio.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@tudominio.com","password":"password-seguro"}'

# Con el token del paso anterior:
curl https://tu-dominio.com/api/auth/me \
  -H "Authorization: Bearer <token>"
```
