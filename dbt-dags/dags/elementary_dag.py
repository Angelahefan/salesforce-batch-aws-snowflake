import os
from datetime import datetime
from cosmos import DbtDag,ProjectConfig,ProfileConfig,ExecutionConfig,RenderConfig
from cosmos.profiles import SnowflakeUserPasswordProfileMapping
def _notify_failure(context):
 ti=context.get('task_instance') or context.get('ti');print(f"[salesforce_dbt_transformation] FAILED {getattr(ti,'dag_id','unknown')}.{getattr(ti,'task_id','unknown')}: {context.get('exception')!r}")
default_args={'depends_on_past':False,'retries':2,'on_failure_callback':_notify_failure}
profile_config=ProfileConfig(profile_name='salesforce_transformation',target_name='prod',profile_mapping=SnowflakeUserPasswordProfileMapping(conn_id='snowflake_default',profile_args={'database':'SALESFORCE_ANALYTICS_DB','schema':'SOURCE','warehouse':'SALESFORCE_COMPUTE_MEDIUM','role':'SALESFORCE_TRANSFORMER'}))
elementary_dag=DbtDag(project_config=ProjectConfig('/usr/local/airflow/dags/dbt'),operator_args={'install_deps':True},profile_config=profile_config,execution_config=ExecutionConfig(dbt_executable_path=f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt"),render_config=RenderConfig(select=['package:elementary']),default_args=default_args,schedule='0 20 * * *',start_date=datetime(2025,8,1),catchup=False,dag_id='salesforce_elementary',description='Elementary observability models only',tags=['dbt','elementary','observability','prod'])
