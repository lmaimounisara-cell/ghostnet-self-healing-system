# TP4 — Docker Compose

`docker compose up -d` starts the coordinator, the workers, and both PostgreSQL databases. Each app waits for its own database to become healthy.

## Database outage test

We stopped `db-coordinator` with `docker compose stop db-coordinator`.

- The coordinator’s `GET /jobs` returned `503 Service Unavailable`.
- The worker’s `GET /health` still returned `200 OK`.

We restarted the database with `docker compose start db-coordinator`.