# GhostNet — Self-Healing Distributed System

## Project Overview

GhostNet is a Python-based microservices project that simulates a distributed system capable of detecting worker failures and automatically redistributing unfinished tasks.

## Main Objective

Build a system that continues operating even when some of its worker nodes fail.

## Architecture

GhostNet consists of two microservices:

- **Coordinator Service:** Manages tasks, assignments and recovery decisions.
- **Workers Service:** Manages simulated workers, heartbeats and task execution.

Each service owns its own PostgreSQL database.

## Technologies

- Python
- FastAPI
- Pydantic
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker and Docker Compose
- HTTPX
- Tenacity
- PyBreaker

Additional event-driven technologies will be selected according to the course TP6 requirements.

## Development Environment

The project is developed locally using free tools on Windows 10.

## Project Goal

Demonstrate failure detection, task redistribution and automatic recovery in a distributed system.