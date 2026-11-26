# TP6 - GhostNet Events

## Business events

| Event | Trigger | Payload | Consumer |
|---|---|---|---|
| job.created | Coordinator creates a job | message_id, job_id, email | Notifications (implemented) |
| job.completed | Worker completes a job | job_id | Coordinator (planned) |
| job.failed | Worker fails to complete a job | job_id, reason | Coordinator (planned) |

## Architecture

- Producer: Coordinator
- Message broker: RabbitMQ
- Exchange: events (Topic)
- Routing key: job.created
- Queue: notifications (Durable)
- Consumer: Notifications

## Validation tests

### 1. Event publication and email notification
PASSED: Job #16 generated a notification for admin@ghostnet.dev.

### 2. Temporal decoupling
PASSED: Jobs #17, #18 and #19 were created while Notifications was stopped.

### 3. Message recovery
PASSED: Notifications processed the three pending messages after restarting.

### 4. Message redelivery
PASSED: Job #20 was retrieved and requeued using the RabbitMQ management interface.

### 5. Idempotence
PASSED: Three deliveries of the same message ID generated one notification and two duplicate warnings.

### 6. Broker failure tolerance
PASSED: Job #21 was created with HTTP 201 while RabbitMQ was stopped. Coordinator logged a publication warning.

## Limitations

- Email sending is simulated through logs.
- Processed message IDs are stored in memory.
- Failed publications during a broker outage are not automatically retried.
