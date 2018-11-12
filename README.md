# PROJECT

i wanted to create a debugger for the apache airflow project. IT works!! but its not a production-ready thing to use.

## How to install / build this repo (you probs won't be able to tbh)
- get a postgres database up
- create a role for the airflow user
- configure your airflow.cfg file to point to your airflow instance
- `airflow initdb`
- try to load in the naveed_test.py file for the scheduler

## How does it work
* there is a debugger view (added via plugin)
* you add breakpoints by specifying the dag_id and the task_id
* you should go to the dag and observe that new breakpoint tasks get automatically created right before the task you want to inspect
* when the pipeline runs, the dag will pause at the BreakpointSensor task
* you go to Admin > Variable, and you should see the breakpoint variable created
* You can delete it, mark it as "done" or "off" and it will mark the sensor as done and keep going through the dag
** If you mark it as "skip", the next time the dag runs, the sensor will automatically be marked as successful

## Video / Screenshots
 video (no sound) lives here: https://vimeo.com/300390033




## TODO:
* productionize the damn thing!
* Looking for help so we can crank it out in a weekend warrior project
