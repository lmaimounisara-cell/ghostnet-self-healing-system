# GhostNet — Microservices Architecture

## 1. Project Overview

GhostNet is a self-healing distributed system that simulates a network of worker nodes executing tasks.

Its main objective is to detect worker failures and automatically redistribute unfinished tasks to healthy workers.

## 2. System Architecture

GhostNet consists of two microservices:

### 2.1 Coordinator Service

Responsibilities:
- Create and manage tasks.
- Assign tasks to available workers.
- Track task status and execution attempts.
- Detect unfinished tasks following worker failures.
- Redistribute unfinished tasks to healthy workers.

Database: PostgreSQL — Coordinator Database.

### 2.2 Workers Service

Responsibilities:
- Register and manage simulated workers.
- Track worker availability and status.
- Maintain heartbeat information.
- Simulate task execution.
- Detect worker failures.
- Report execution results.

Database: PostgreSQL — Workers Database.

## 3. Database Ownership

Each microservice owns its database.

- Coordinator Service owns the Coordinator Database.
- Workers Service owns the Workers Database.

No microservice is allowed to access another microservice's database directly.

## 4. Communication

### Synchronous Communication — TP5

The Coordinator Service communicates with the Workers Service through HTTP requests.

The communication uses HTTPX, timeout handling, retries with Tenacity and a circuit breaker with PyBreaker.

### Asynchronous Communication — TP6

The services exchange events to communicate important changes, such as worker failures and task completion.

The event technology will be selected according to the teacher's TP6 requirements.

## 5. Failure and Recovery Scenario

1. The Coordinator assigns a task to a worker.
2. The worker begins executing the task.
3. The worker crashes or stops sending heartbeats.
4. The Workers Service detects the failure.
5. A failure notification is communicated to the Coordinator.
6. The Coordinator identifies unfinished tasks.
7. The Coordinator redistributes those tasks to healthy workers.
8. The system continues operating.

## 6. Architectural Constraints

- Maximum of two microservices for this project.
- One database per microservice.
- No direct database sharing.
- Communication through defined service interfaces.
- Worker nodes are simulated inside the Workers Service.
- All development and testing are performed locally using free tools.

## 7. Main Objective

Demonstrate how a distributed system can detect failures, redistribute unfinished work and continue operating without requiring manual intervention.

## 8. Architecture Diagram

```mermaid
flowchart TB
    C[Coordinator Service]
    W[Workers Service]

    DB1[(Coordinator PostgreSQL)]
    DB2[(Workers PostgreSQL)]

    C -->|Read and write| DB1
    W -->|Read and write| DB2

    C -->|HTTP requests| W
    W -->|Events| C