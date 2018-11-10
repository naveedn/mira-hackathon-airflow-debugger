import airflow
from builtins import range
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.decorators import apply_defaults
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.models import Variable
from airflow.models import DAG
from airflow.models import TaskInstance
from airflow.exceptions import AirflowException
from datetime import timedelta
from datetime import datetime

import pdb
import json
from uuid import uuid4


def remap_upstream_deps(debug_task, debug_checkpoint):

  # map parents
  upstream_deps = debug_task.upstream_list

  debug_task._upstream_task_ids = set() # @HACK clear the upstream task list

  debug_checkpoint.set_downstream(debug_task)
  debug_checkpoint.set_upstream(upstream_deps)

def generate_breakpoint(debug_task, dag):
  debug_task_id = debug_task.task_id

  debug_checkpoint = BreakPointSensor(
      task_id='breakpoint_sensor_' + debug_task_id,
      debug_task_id=debug_task_id,
      poke_interval=5,
      dag=dag)

  #pdb.set_trace()
  remap_upstream_deps(debug_task, debug_checkpoint)

def generate_breakpoints_from_ids(debug_task_id, dag_id):
  dag_obj = dag_map[dag_id]
  debug_task = dag_obj.get_task(debug_task_id)

  generate_breakpoint(debug_task,  dag_obj)


class BreakPointSensor(BaseSensorOperator):

  @apply_defaults
  def __init__(self,
               debug_task_id,
               *args, **kwargs):

    super(BreakPointSensor, self).__init__(*args, **kwargs)
    self.debug_task_id = debug_task_id
    self.set_breakpoint = False

  def poke(self, context):
    try:
      status = Variable.get('breakpoint.{dag}.{task}'.format(dag=self.dag.dag_id, task=self.debug_task_id))
    except KeyError:
      status = None

    if status == 'skip':
      return True

    if not self.set_breakpoint:
      Variable.set('breakpoint.{dag}.{task}'.format(dag=self.dag.dag_id, task=self.debug_task_id), 'on')
      status = 'on'

      self.set_breakpoint = True

    if not status or status == 'done' or status == 'off':
      return True


## Define Dag / Tasks
args = {
    'owner': 'naveed',
    'start_date': airflow.utils.dates.days_ago(2),
    'debug': True
    #'wait_on_downstream': True,
}

dag = DAG(
    dag_id='naveed_test',
    default_args=args,
    schedule_interval='10 * * * *',
    max_active_runs=1,
    catchup=False,
    start_date=datetime(2018, 11, 9)
)

dag_map = {'naveed_test': dag}

sleep = BashOperator(
        task_id='sleep',
        bash_command='sleep 2 && echo "done!"',
        dag=dag)


run_this_first = DummyOperator(task_id='run_this_first', dag=dag)
run_this_first_parallel = DummyOperator(task_id='run_this_first_parallel', dag=dag)
run_this_last = DummyOperator(task_id='run_this_last', dag=dag)
run_this_last_parallel = DummyOperator(task_id='run_this_last_parallel', dag=dag)

## DAG order
run_this_first >> sleep >> run_this_last
run_this_first_parallel >> sleep >> run_this_last_parallel
## insert breakpoint

# if __name__ == "__main__":
#   dag.tree_view()
# generate_breakpoints_from_ids('sleep', 'naveed_test')