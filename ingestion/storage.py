from pathlib import Path

from .config import (
    get_aws_region,
    get_bucket,
    get_local_s3_root,
    get_storage_backend,
)


def get_local_object_path(
    key: str,
) -> Path:
    return (
        get_local_s3_root()
        / get_bucket()
        / key
    )


def put_file(
    key: str,
    source_path: Path,
) -> None:
    if get_storage_backend() == "s3":
        import boto3

        client = boto3.client(
            "s3",
            region_name=get_aws_region(),
        )

        client.upload_file(
            str(source_path),
            get_bucket(),
            key,
            ExtraArgs={
                "ServerSideEncryption": "AES256",
            },
        )

        return

    destination = get_local_object_path(
        key
    )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination.write_bytes(
        Path(source_path).read_bytes()
    )


def get_text(
    key: str,
) -> str | None:
    if get_storage_backend() == "s3":
        import boto3
        from botocore.exceptions import ClientError

        client = boto3.client(
            "s3",
            region_name=get_aws_region(),
        )

        try:
            response = client.get_object(
                Bucket=get_bucket(),
                Key=key,
            )
        except ClientError as error:
            error_code = (
                error.response
                .get("Error", {})
                .get("Code")
            )

            if error_code in {
                "NoSuchKey",
                "404",
            }:
                return None

            raise

        return (
            response["Body"]
            .read()
            .decode("utf-8")
        )

    object_path = get_local_object_path(
        key
    )

    if not object_path.exists():
        return None

    return object_path.read_text(
        encoding="utf-8"
    )


def put_text(
    key: str,
    text: str,
) -> None:
    if get_storage_backend() == "s3":
        import boto3

        client = boto3.client(
            "s3",
            region_name=get_aws_region(),
        )

        client.put_object(
            Bucket=get_bucket(),
            Key=key,
            Body=text.encode("utf-8"),
            ContentType="application/json",
            ServerSideEncryption="AES256",
        )

        return

    destination = get_local_object_path(
        key
    )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination.write_text(
        text,
        encoding="utf-8",
    )