from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint, request
from flask_admin import BaseView, expose

import sys

sys.path.append('/Users/naveed/Mira/hackathon/airflow/dags')  # l-o-l

import test_naveed

class TestView(BaseView):
        @expose('/')
        def test(self):
                return self.render("test_plugin/test.html")

        @expose('/breakpoint', methods=['POST'])
        def test_add(self):
            dag_id = request.form['dag_id']
            task_id = request.form['task_id']

            src_code = open('/Users/naveed/Mira/hackathon/airflow/dags/test_naveed.py', 'a')
            src_code.write("\ngenerate_breakpoints_from_ids('{task_id}', '{dag_id}')".format(task_id=task_id, dag_id=dag_id))

            #test_naveed.generate_breakpoints_from_ids(task_id, dag_id)
            print 'haha'
            return self.render("test_plugin/test.html")


admin_view_ = TestView(category="Debugger", name="breakpoints")

blue_print_ = Blueprint("debugger",
                        __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/static/test_plugin')


class AirflowTestPlugin(AirflowPlugin):
    name = "Debug Breakpoints"
    admin_views = [admin_view_]
    flask_blueprints = [blue_print_]
