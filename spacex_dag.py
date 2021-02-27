from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2018, 1, 1),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG("spacex", default_args=default_args, schedule_interval="0 0 1 1 *")

rokets = ['falcon1', 'falcon9', 'falconheavy', 'all']
for roket in rokets:
    comand = "python3 /root/airflow/dags/spacex/load_launches.py -y {{ execution_date.year }} -o /var/data -r " + roket
    if roket == 'all':
        comand = "python3 /root/airflow/dags/spacex/load_launches.py -y {{ execution_date.year }} -o /var/data"
    
    t1 = BashOperator(
        task_id="get_data", 
        bash_command=comand, 
        dag=dag
    )

    t2 = BashOperator(
        task_id="print_data", 
        bash_command="cat /var/data/year={{ execution_date.year }}/rocket={{ params.rocket }}/data.csv", 
        params={"rocket": roket}, # falcon1/falcon9/falconheavy
        dag=dag
    )

    t1 >> t2
