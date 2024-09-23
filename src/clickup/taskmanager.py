from logger.fslogger import global_fs_logger as logger
from clickup.client import ClickUpClient
from fsg.automator import WebFormAutomator
from fsg.dataformat import FormData


class TaskManager:
    def __init__(
        self, clickup_client: ClickUpClient, web_form_automator: WebFormAutomator
    ):
        """Initializes the TaskManager with the ClickUpClient and WebFormAutomator instances.
        The Taskmanager is the Main execution class that will extract tasks from ClickUp, convert the json output into the FormData Class and then submit them to the FSG website.

        Args:
            clickup_client (ClickUpClient): _description_
            form_automator (WebFormAutomator): _description_
        """
        self.clickup_client: ClickUpClient = clickup_client
        self.web_form_automator: WebFormAutomator = web_form_automator

    def import_entries(self) -> dict:
        """Starts the task import process by extracting tasks from ClickUp and submitting them to the FSG website."""
        # system_lists = self.clickup_client.filter_system_lists(
        #     self.clickup_client.build_get_request(f"team/{FSCONFIG.clickup_workspace_id}/list"),
        # )
        # for list_id in system_lists:
        #     tasks = self.clickup_client.build_get_request(f"list/{list_id.get("id")}/task")
        #     logger.info(tasks)

    def convert_data(self, json_output: dict) -> list[FormData]:
        pass

    def submit_to_fsg(self, form_data_list: list[FormData]):
        """Submits the provided form data to the FSG website.

        Args:
            form_data_list (list[FormData]): _description_
        """
        self.web_form_automator.login_fsg_website()
        self.web_form_automator.navigate_to_form()

        # Example of using the the Form Data Class
        # form_data = FormData(
        #     system="BR",
        #     assembly="Brake Lines",
        #     assembly_name="",
        #     assembly_comment="",
        #     sub_assembly="- none -",
        #     sub_assembly_name="",
        #     part="Testpart Tool",
        #     makebuy="b",
        #     comments="Replace worn parts",
        #     quantity=4,
        # )

        for form_data in form_data_list:
            self.web_form_automator.create_new_entry(form_data)
