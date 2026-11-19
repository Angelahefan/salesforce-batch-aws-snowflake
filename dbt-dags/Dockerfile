FROM quay.io/astronomer/astro-runtime:12.7.1
RUN python -m venv /usr/local/airflow/dbt_venv && /usr/local/airflow/dbt_venv/bin/pip install --no-cache-dir dbt-snowflake==1.10.*
