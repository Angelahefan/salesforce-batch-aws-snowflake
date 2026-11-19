import os,subprocess
from datetime import datetime,timedelta
from airflow.decorators import dag,task
PROJECT='/usr/local/airflow/project'
@dag(dag_id='salesforce_cdc_ingestion',schedule='0 */1 * * *',start_date=datetime(2025,8,1),catchup=False,tags=['salesforce','cdc','s3','ingestion'],default_args={'retries':2,'retry_delay':timedelta(minutes=5)})
def salesforce_cdc_ingestion():
 @task
 def generate_changes(): subprocess.run(['python','-c','from salesforce_simulator.generator import init,mutate; init(); mutate()'],cwd=PROJECT,check=True)
 @task
 def extract_cdc(): subprocess.run(['python','-m','ingestion.cdc_extract'],cwd=PROJECT,check=True)
 generate_changes() >> extract_cdc()
salesforce_cdc_ingestion()
