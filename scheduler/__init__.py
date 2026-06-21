"""Scheduler worker package (Phase 7).

Run the daily ingestion worker:

    python -m scheduler
    python -m scheduler --once
"""

from scheduler.worker import create_scheduler, run_scheduled_ingestion

__all__ = ["create_scheduler", "run_scheduled_ingestion"]
