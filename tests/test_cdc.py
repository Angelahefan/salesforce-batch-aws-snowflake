import json
from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture(autouse=True)
def isolated_runtime(
    tmp_path,
    monkeypatch,
):
    test_database = (
        tmp_path
        / "salesforce.db"
    )

    test_local_s3 = (
        tmp_path
        / "local_s3"
    )

    monkeypatch.setenv(
        "SALESFORCE_SIMULATOR_DB",
        str(test_database),
    )

    monkeypatch.setenv(
        "LOCAL_S3_ROOT",
        str(test_local_s3),
    )

    monkeypatch.setenv(
        "STORAGE_BACKEND",
        "local",
    )

    monkeypatch.setenv(
        "S3_RAW_BUCKET",
        "test-salesforce-raw",
    )

    monkeypatch.setenv(
        "S3_RAW_PREFIX",
        "raw/salesforce",
    )

    from salesforce_simulator import (
        generator,
    )

    generator.init()

    yield {
        "root": tmp_path,
        "database": test_database,
        "local_s3": test_local_s3,
        "bucket": "test-salesforce-raw",
    }


def test_cdc_hive_partition_and_checkpoint(
    isolated_runtime,
):
    from ingestion import cdc_extract

    result = cdc_extract.extract_object(
        "account",
        "2026-11-18",
    )

    assert result["rows"] == 25

    assert (
        "object=account/"
        "event_date=2026-11-18/"
        "event_hour="
        in result["key"]
    )

    parquet_filename = Path(
        result["key"]
    ).name

    assert parquet_filename.startswith(
        "part-202"
    )

    assert parquet_filename.endswith(
        ".parquet"
    )

    parquet_file = (
        isolated_runtime["local_s3"]
        / isolated_runtime["bucket"]
        / result["key"]
    )

    assert parquet_file.exists()

    parquet_data = pd.read_parquet(
        parquet_file,
        engine="pyarrow",
    )

    assert len(parquet_data) == 25

    assert {
        "account_id",
        "change_type",
        "replay_id",
        "event_time",
        "ingested_at",
    }.issubset(
        parquet_data.columns
    )

    checkpoint_file = (
        isolated_runtime["local_s3"]
        / isolated_runtime["bucket"]
        / "raw"
        / "salesforce"
        / "_checkpoints"
        / "account.json"
    )

    assert checkpoint_file.exists()

    checkpoint_data = json.loads(
        checkpoint_file.read_text(
            encoding="utf-8"
        )
    )

    assert checkpoint_data["object"] == (
        "account"
    )

    assert checkpoint_data["replay_id"] == (
        result["replay_id"]
    )

    assert checkpoint_data["s3_key"] == (
        result["key"]
    )

    second_result = (
        cdc_extract.extract_object(
            "account",
            "2026-11-18",
        )
    )

    assert second_result["rows"] == 0

    assert second_result["key"] is None


def test_update_insert_delete_events_exist(
    isolated_runtime,
):
    from ingestion import cdc_extract

    from salesforce_simulator import (
        generator,
    )

    from salesforce_simulator.database import (
        connect,
    )

    # Consume initial INSERT events.
    initial_results = cdc_extract.run(
        "2026-11-18"
    )

    assert sum(
        result["rows"]
        for result in initial_results
    ) > 0

    generator.mutate(
        updates=2,
        inserts=1,
        deletes=1,
    )

    incremental_results = (
        cdc_extract.run(
            "2026-11-19"
        )
    )

    incremental_rows = sum(
        result["rows"]
        for result in incremental_results
    )

    assert incremental_rows >= 4

    with connect() as connection:
        operations = {
            row["change_type"]
            for row in connection.execute(
                """
                select distinct
                    change_type
                from cdc_event
                where replay_id > 0
                """
            )
        }

    assert {
        "INSERT",
        "UPDATE",
        "DELETE",
    }.issubset(operations)

    # Running again without new mutations
    # must not create duplicate CDC output.
    rerun_results = cdc_extract.run(
        "2026-11-19"
    )

    assert sum(
        result["rows"]
        for result in rerun_results
    ) == 0