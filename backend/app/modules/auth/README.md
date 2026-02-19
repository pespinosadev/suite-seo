# Módulo: auth

## Descripción
Autenticación JWT, usuarios y roles. Todos los módulos futuros usan `core/deps.py`
(que importa los modelos de aquí) para verificar identidad y permisos.

## Endpoints

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | /api/auth/login | No | email+password → access_token |
| GET | /api/auth/me | Bearer | Usuario autenticado + rol |

**POST /api/auth/login**
```json
// body
{"email": "admin@example.com", "password": "secret"}
// response 200
{"access_token": "eyJ...", "token_type": "bearer"}
```

**GET /api/auth/me** — Header: `Authorization: Bearer <token>`
```json
{
  "id": 1,
  "email": "admin@example.com",
  "is_active": true,
  "role": {"id": 1, "name": "admin"},
  "created_at": "2024-01-01T00:00:00Z"
}
```

## Modelos de datos

### roles
| Campo | Tipo | Notas |
|-------|------|-------|
| id | integer PK | |
| name | varchar(50) UNIQUE | admin \| responsable \| usuario |

### users
| Campo | Tipo | Notas |
|-------|------|-------|
| id | integer PK | |
| email | varchar(255) UNIQUE | |
| hashed_password | varchar(255) | bcrypt |
| is_active | boolean | false = no puede hacer login |
| role_id | FK → roles.id | |
| created_at | timestamptz | |

## Variables de entorno

| Variable | Requerida | Descripción |
|----------|-----------|-------------|
| SECRET_KEY | ✅ | Clave JWT (mín. 32 chars aleatorios) |
| ALGORITHM | No (HS256) | Algoritmo JWT |
| ACCESS_TOKEN_EXPIRE_MINUTES | No (60) | Minutos hasta expiración |

## Dependencias

- Usa `core/security.py`: hash_password, verify_password, create_access_token, decode_token
- Usa `core/deps.py`: get_db
- `core/deps.py` importa los modelos de aquí para get_current_user

## CLI — Crear usuario

```bash
docker compose exec seo_api python -m app.core.create_user \
  --email admin@example.com \
  --password "tu-password" \
  --role admin
```
