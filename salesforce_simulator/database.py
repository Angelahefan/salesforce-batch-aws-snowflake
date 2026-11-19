import os
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def get_db_path() -> Path:
    return Path(
        os.getenv(
            "SALESFORCE_SIMULATOR_DB",
            str(ROOT / "data" / "salesforce.db"),
        )
    )


def connect() -> sqlite3.Connection:
    db_path = get_db_path()
    db_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(
        db_path,
        timeout=30,
    )

    connection.row_factory = sqlite3.Row

    return connection