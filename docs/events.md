# TP6 — GhostNet events

| Event | When it happens | Message data | Who reads it |
|---|---|---|---|
| `job.created` | The coordinator saves a new job. | `job_id` | Notifications (implemented) |
| `job.completed` | A worker finishes a job successfully. | `job_id` | Coordinator (planned) |
| `job.failed` | A worker reports that a job attempt failed. | `job_id`, `reason` | Coordinator (planned) |

## What we tested

- Notifications received the event for job #12.
- RabbitMQ held the event for job #13 while Notifications was offline.
  Notifications read it after restarting.
- Two copies with the same message ID produced one notification.
  Processed IDs are kept in memory until Notifications restarts.