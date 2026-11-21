# GhostNet — Self-Healing Distributed System

## Project Overview

GhostNet is a Python microservices project designed to detect worker failures and reassign unfinished jobs. The goal is to keep processing jobs when a worker stops.

## Architecture

- **Coordinator:** Receives job requests and stores them in PostgreSQL. It will later assign jobs and manage recovery.
- **Workers:** Starts as a separate service with a health endpoint. It will later run jobs and report their progress.

Docker Compose starts both services and their separate PostgreSQL databases. Each service waits for its database to be ready.

## Technologies

- **Used so far:** Python, FastAPI, Pydantic, PostgreSQL, SQLAlchemy, Alembic, Docker, and Docker Compose.
- **Planned:** HTTPX, Tenacity, and PyBreaker in TP5, then RabbitMQ in TP6.

## Development Environment

GhostNet runs locally on Windows using Docker Desktop and PowerShell.

## Démarrage rapide

Depuis un clone neuf, ouvrez PowerShell dans le dossier `GhostNet` avec Docker Desktop démarré :

```powershell
Copy-Item .\.env.example .\.env
docker compose up -d --build --wait
docker compose exec coordinator alembic upgrade head
```

Ouvrez [Swagger](http://127.0.0.1:8000/docs) et exécutez `GET /jobs`. Une base neuve doit renvoyer `200 OK` et `[]`.

Pour vérifier le service Workers, ouvrez [son endpoint `/health`](http://127.0.0.1:8001/health).