import os
import time
from fastapi import HTTPException
from consts import LOGS_DIR, ARTIFACTS_DIR

from dotenv import load_dotenv
load_dotenv()


LOGS_RETENTION_DAYS = int(os.environ.get("LOGS_RETENTION_DAYS"))
ARTIFACTS_RETENTION_DAYS = int(os.environ.get("ARTIFACTS_RETENTION_DAYS"))


def _delete_old_files(directory: str, retention_days: int, label: str = "log"):
    now = time.time()
    retention_seconds = retention_days * 86400  # 60 * 60 * 24

    if not os.path.exists(directory):
        raise HTTPException(status_code=404, detail=f"{label.title()} directory '{directory}' does not exist.")

    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            if os.path.isfile(file_path):
                file_age = now - os.path.getmtime(file_path)
                if file_age > retention_seconds:
                    os.remove(file_path)



def delete_old_files():
    _delete_old_files(LOGS_DIR, LOGS_RETENTION_DAYS, label="logs")
    _delete_old_files(ARTIFACTS_DIR, ARTIFACTS_RETENTION_DAYS, label="artifacts")
