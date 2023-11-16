import api as api
from services import db_service
import uuid
from datetime import datetime


class Logger:

    def __init__(self, db: db_service.Database):
        self.db = db

    def push_run_log(self, log: api.RunLog) -> str:
        """Write a run log."""
        return self.db.insert_run_log(log)

    def push_run_model_logs(self, logs: [api.RunModelLog]) -> [str]:
        """Write a list of run model logs."""
        return self.db.insert_run_model_logs(logs)

    def info(self, phase: str, run_id: str, log: str):
        self.push_run_log({
            "id": str(uuid.uuid4()),
            "run_id": run_id,
            "phase": phase,
            "severity": "info",
            "log": log,
            "created_on": datetime.now()
        })

    def warn(self, phase: str, run_id: str, log: str):
        self.push_run_log({
            "id": str(uuid.uuid4()),
            "run_id": run_id,
            "phase": phase,
            "severity": "warn",
            "log": log,
            "created_on": datetime.now()
        })

    def error(self, phase: str, run_id: str, log: str):
        self.push_run_log({
            "id": str(uuid.uuid4()),
            "run_id": run_id,
            "phase": phase,
            "severity": "error",
            "log": log,
            "created_on": datetime.now()
        })
