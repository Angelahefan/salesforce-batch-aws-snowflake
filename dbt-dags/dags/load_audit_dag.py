import os,subprocess,tempfile
from datetime import datetime,timedelta
from airflow.decorators import dag,task
from airflow.hooks.base import BaseHook
DBT_PROJECT_DIR='/usr/local/airflow/dags/dbt';DBT_EXECUTABLE=f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt";LOAD_AUDIT_SELECT='tag:load_audit source:SALESFORCE.LOAD_AUDIT'
def env(s):
 c=BaseHook.get_connection('snowflake_default');return {**os.environ,'DBT_LOG_PATH':f'{s}/logs','DBT_TARGET_PATH':f'{s}/target','SNOWFLAKE_ACCOUNT':c.extra_dejson['account'],'SNOWFLAKE_USER':c.login,'SNOWFLAKE_PASSWORD':c.password,'SNOWFLAKE_ROLE':c.extra_dejson.get('role','SALESFORCE_TRANSFORMER'),'SNOWFLAKE_SCHEMA':c.schema or 'SOURCE'}
def run(args):
 s=tempfile.mkdtemp(prefix='dbt_load_audit_');e=env(s);subprocess.run([DBT_EXECUTABLE,'deps','--project-dir',DBT_PROJECT_DIR,'--profiles-dir',DBT_PROJECT_DIR,'--packages-install-path',f'{s}/dbt_packages'],env=e,check=True);subprocess.run([DBT_EXECUTABLE,*args,'--project-dir',DBT_PROJECT_DIR,'--profiles-dir',DBT_PROJECT_DIR,'--packages-install-path',f'{s}/dbt_packages','--target','prod'],env=e,check=True)
@dag(dag_id='salesforce_load_audit',schedule='0 14 * * *',start_date=datetime(2025,8,1),catchup=False,tags=['dbt','salesforce','load_audit','data_quality','prod'],default_args={'retries':2,'retry_delay':timedelta(minutes=5)})
def salesforce_load_audit():
 @task
 def source_freshness():run(['source','freshness','--select','source:SALESFORCE.LOAD_AUDIT'])
 @task
 def test_load_audit():run(['test','--select',LOAD_AUDIT_SELECT])
 source_freshness() >> test_load_audit()
salesforce_load_audit()
