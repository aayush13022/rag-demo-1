# Scheduler (Phase 7)

Daily corpus ingestion runs as a **separate worker process** from the API.

## Schedule

| Setting | Value |
|---------|-------|
| Time | **10:00 AM IST** daily |
| Cron | `0 10 * * *` |
| Timezone | `Asia/Kolkata` |
| Retries | 3 with exponential backoff (60s base) |
| Overlap | Skipped if another job is already running |

Configured in `config/corpus.yaml` under `scheduler:`.

## Run locally

```bash
# One-off ingestion (manual trigger / tests)
python -m scheduler --once

# Continuous worker (waits for 10:00 AM IST daily)
python -m scheduler
```

Alternative entry point:

```bash
python -m ingestion.scheduler --once
```

## Production cron

See `crontab.example`:

```cron
0 10 * * * cd /path/to/rag-demo-1 && .venv/bin/python -m scheduler --once >> logs/scheduler.log 2>&1
```

## GitHub Actions

Daily ingestion also runs via `.github/workflows/daily-ingestion.yml` at 10:00 AM IST (04:30 UTC).

Trigger manually: **Actions → Daily Ingestion → Run workflow**

## Observability

After each run, check:

```bash
curl http://localhost:8000/corpus/status
```

Logs include:
- `ingestion_job_contract=` — full job JSON (status, chunks, duration, URLs)
- `ingestion_run_duration_seconds=` — run time
- `Corpus may be stale` — warning if data is older than 48 hours

## Failure behavior

- **Partial failure** (some URLs fail): successful funds are indexed; status = `partial`
- **Full failure**: previous corpus version is kept; status = `failed`
- **Overlapping trigger**: second run is skipped
