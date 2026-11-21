# TP5 — Communication synchrone et résilience

Avant de créer un job, le coordinateur vérifie la capacité du service workers.
Il attend au maximum une seconde par tentative et réessaie une fois.
Après cinq vérifications échouées de suite, il suspend les appels pendant 30 secondes.

| Test | Résultat |
|---|---|
| Workers arrêté, avant protection | HTTP 500 en 4,05 s |
| Workers arrêté, circuit ouvert | HTTP 503 en 27 ms |
| Workers redémarré, après la pause | HTTP 201, job #7 créé |

Si le service workers est indisponible, le coordinateur renvoie 503 et ne crée pas le job.