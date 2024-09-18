from logger.fslogger import global_fs_logger as logger
from clickup.client import ClickUpClient
from fsg.automator import WebFormAutomator


class TaskManager:
    def __init__(self, clickup_client: ClickUpClient, form_automator: WebFormAutomator):
        self.clickup_client = clickup_client
        self.form_automator = form_automator

    def extract_and_submit_tasks(self, workspace_id):
        tasks = self.clickup_client.get_tasks_from_workspace(workspace_id)
        for task in tasks:
            task_data = self.process_task(task)
            self.form_automator.fill_form(task_data)
            self.form_automator.submit_form()

    def process_task(self, task):
        pass
        # A format for the fsg website should include the following:
        # FSG-ID    |  EXAMPLE:                                     |   CLICKUP response
        # -----------------------------------------------------------------------------------------
        # system    | 'BR;EN; ...',                                 |   'name': 'SP.12.00.00_ScrewCover'
        # Assembly  | 'Brake Fluid',                                |
        #           | If not in FSG Assembly List:                  |
        #           |-> OTHER create with name + description        |
        # Sub-Assembly if given                                     |
        #           | If Sub-Assembly not in FSG Sub Assembly Lists |
        #           |-> NEW create with name                        |
        # Part Name | 'Fluid xyz',                                  |   'name': 'SP.12.00.00_ScrewCover'
        # Make/Buy  | 'Make' or 'Buy', radio button                 |
        # Quantity  | 1,                                            |
        # Custom ID | '1234',                                       |
        #           | Check if ID already exists                    |
