import sys
from airflow.hooks.postgres_hook import PostgresHook

dag_input = sys.argv[1]
hook=PostgresHook( postgres_conn_id='airflow_db')

for t in ["xcom", "task_instance", "sla_miss", "log", "job", "dag_run", "dag", "dag_stats", "task_fail"]:
    sql="delete from {} where dag_id='{}'".format(t, dag_input)
    hook.run(sql, True)
