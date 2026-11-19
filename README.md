# Salesforce Analytics Pipeline

Production-style portfolio pipeline adapted from the original transformation project while preserving its dbt, CI/CD, Terraform, Snowflake, Astronomer/Cosmos and Elementary architecture.

## Flow
Local Salesforce simulator -> CDC INSERT/UPDATE/DELETE -> replay checkpoints -> S3 Parquet Hive partitions -> Snowflake RAW -> dbt staging -> intermediate current state -> Kimball marts -> dbt docs/Elementary.

### Local CDC smoke test
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q tests
python -c "from salesforce_simulator.generator import init,mutate; init(); mutate()"
python -m ingestion.cdc_extract
```
Default `STORAGE_BACKEND=local` writes the exact S3 key layout under `local_s3/`. Set `STORAGE_BACKEND=s3`, `S3_RAW_BUCKET`, AWS credentials and region to use real S3.

The S3 layout is `raw/salesforce/object=<object>/event_date=YYYY-MM-DD/part-<uuid>.parquet`; checkpoints live under `raw/salesforce/_checkpoints/`.
