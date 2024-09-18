from client import ClickupClient
from automator import FormAutomator

class TaskManager:
    def __init__(self, clickup_client : ClickupClient, form_automator : FormAutomator):
        self.clickup_client = clickup_client
        self.form_automator = form_automator
    
    def extract_and_submit_tasks(self, workspace_id):
        tasks = self.clickup_client.get_tasks_from_workspace(workspace_id)
        for task in tasks:
            task_data = self.process_task(task)
            self.form_automator.fill_form(task_data)
            self.form_automator.submit_form()
    
    def process_task(self, task):
        # Logic to format the task data into the form input structure
