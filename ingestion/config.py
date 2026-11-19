import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def get_storage_backend() -> str:
    return os.getenv(
        "STORAGE_BACKEND",
        "local",
    )


def get_bucket() -> str:
    return os.getenv(
        "S3_RAW_BUCKET",
        "salesforce-analytics-raw-local",
    )


def get_prefix() -> str:
    return os.getenv(
        "S3_RAW_PREFIX",
        "raw/salesforce",
    ).strip("/")


def get_local_s3_root() -> Path:
    return Path(
        os.getenv(
            "LOCAL_S3_ROOT",
            str(ROOT / "local_s3"),
        )
    )


def get_aws_region() -> str:
    return os.getenv(
        "AWS_REGION",
        "ap-southeast-2",
    )