|Scenario                                      |→ Script / Command             |
|--------------------------------------------  |------------------------------ |
|First-time setup / new machine                |→ Deploy (10.1)                |
|Normal dev after small code changes           |→ Rebuild (10.2)               |
|Service seems stuck; want clean restart       |→ Refresh (10.4)               |
|DB schema or data is badly out of sync        |→ Destroy (10.3) then Deploy   |
|Inspect logs for troubleshooting              |→ docker compose logs -f ...   |
|Inspect container internals (shell)           |→ docker compose exec ...      |
|Run tests in a clean, ephemeral web container |→ docker compose run --rm ...  |
