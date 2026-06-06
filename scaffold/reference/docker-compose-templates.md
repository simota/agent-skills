# Docker Compose Templates

Purpose: Use this file when the task is a local development stack, production-like local stack, or Compose verification plan.

Contents:
1. Full development stack
2. Production-like local stack
3. Minimal quick-start
4. Verification checklist

## Full Development Stack

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app_dev
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    command: pnpm dev
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: app_dev
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d app_dev"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  redis_data:
```

## Production-Like Local Stack

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    env_file:
      - .env.production.local
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 512M
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    depends_on:
      - app
    restart: unless-stopped
```

## Minimal Quick-Start

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
      POSTGRES_DB: app_dev
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

## Verification Checklist

- `docker compose up -d` completes successfully
- Every required service reaches healthy status
- App, database, and cache connectivity work
- Seed data and migrations are applied
- Volumes survive restart when persistence is expected
- Hot reload and logs are usable in development

Useful commands:

```bash
docker compose up -d
docker compose ps
docker compose exec app curl localhost:3000/health
docker compose exec db pg_isready -U postgres
docker compose exec redis redis-cli ping
docker compose logs -f app
docker compose down -v
```
