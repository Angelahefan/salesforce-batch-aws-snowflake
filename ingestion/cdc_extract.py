import json
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from salesforce_simulator.database import connect

from .config import get_prefix
from .storage import (
    get_text,
    put_file,
    put_text,
)


OBJECTS = [
    "account",
    "contact",
    "opportunity",
    "opportunity_line_item",
]


def checkpoint_key(
    object_name: str,
) -> str:
    return (
        f"{get_prefix()}/"
        f"_checkpoints/"
        f"{object_name}.json"
    )


def get_checkpoint(
    object_name: str,
) -> int:
    raw_checkpoint = get_text(
        checkpoint_key(object_name)
    )

    if not raw_checkpoint:
        return 0

    checkpoint_data = json.loads(
        raw_checkpoint
    )

    return int(
        checkpoint_data["replay_id"]
    )


def build_parquet_key(
    object_name: str,
    run_date: str | None = None,
    now_utc: datetime | None = None,
) -> str:
    current_time = (
        now_utc
        or datetime.now(timezone.utc)
    )

    event_date = (
        run_date
        or current_time.date().isoformat()
    )

    event_hour = current_time.strftime(
        "%H"
    )

    ingestion_timestamp = (
        current_time.strftime(
            "%Y%m%dT%H%M%S%fZ"
        )
    )

    unique_suffix = uuid.uuid4().hex[:8]

    file_name = (
        f"part-{ingestion_timestamp}-"
        f"{unique_suffix}.parquet"
    )

    return (
        f"{get_prefix()}/"
        f"object={object_name}/"
        f"event_date={event_date}/"
        f"event_hour={event_hour}/"
        f"{file_name}"
    )


def extract_object(
    object_name: str,
    run_date: str | None = None,
) -> dict:
    last_replay_id = get_checkpoint(
        object_name
    )

    with connect() as connection:
        rows = [
            dict(row)
            for row in connection.execute(
                """
                select
                    replay_id,
                    object_name,
                    record_id,
                    change_type,
                    event_time,
                    system_modstamp,
                    payload
                from cdc_event
                where object_name = ?
                  and replay_id > ?
                order by replay_id
                """,
                (
                    object_name,
                    last_replay_id,
                ),
            )
        ]

    if not rows:
        return {
            "object": object_name,
            "rows": 0,
            "replay_id": last_replay_id,
            "key": None,
        }

    now_utc = datetime.now(
        timezone.utc
    )

    output_records = []

    for event in rows:
        event_data = dict(event)

        payload = json.loads(
            event_data.pop("payload")
        )

        payload.update(event_data)

        payload["ingested_at"] = (
            now_utc.isoformat()
        )

        output_records.append(
            payload
        )

    parquet_key = build_parquet_key(
        object_name=object_name,
        run_date=run_date,
        now_utc=now_utc,
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        parquet_file = (
            Path(temp_dir)
            / Path(parquet_key).name
        )

        dataframe = pd.DataFrame(
            output_records
        )

        dataframe.to_parquet(
            parquet_file,
            index=False,
            compression="snappy",
            engine="pyarrow",
        )

        # If this fails, the checkpoint is not updated.
        put_file(
            parquet_key,
            parquet_file,
        )

    latest_replay_id = int(
        rows[-1]["replay_id"]
    )

    checkpoint_document = {
        "object": object_name,
        "replay_id": latest_replay_id,
        "s3_key": parquet_key,
        "updated_at": now_utc.isoformat(),
    }

    # Critical ordering:
    # update checkpoint only after Parquet write succeeds.
    put_text(
        checkpoint_key(object_name),
        json.dumps(
            checkpoint_document,
            indent=2,
        ),
    )

    return {
        "object": object_name,
        "rows": len(output_records),
        "replay_id": latest_replay_id,
        "key": parquet_key,
    }


def run(
    run_date: str | None = None,
) -> list[dict]:
    return [
        extract_object(
            object_name,
            run_date,
        )
        for object_name in OBJECTS
    ]


if __name__ == "__main__":
    print(
        json.dumps(
            run(),
            indent=2,
        )
    )
