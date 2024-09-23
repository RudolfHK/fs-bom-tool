from logger.fslogger import global_fs_logger as logger
from clickup.client import ClickUpClient
from fsg.automator import WebFormAutomator
from fsg.dataformat import FormData


class TaskManager:
    """Manages tasks by importing them from ClickUp and submitting them to the FSG website.

    Attributes:
        clickup_client (ClickUpClient): The client used to interact with the ClickUp API.
        web_form_automator (WebFormAutomator): The automator used to interact with the FSG website.

    Methods:
        import_entries() -> dict:
            Starts the task import process by extracting tasks from ClickUp and submitting them to the FSG website.
        convert_data(json_output: dict) -> list[FormData]:
            Converts the JSON output from ClickUp into a list of FormData objects.
        submit_to_fsg(form_data_list: list[FormData]):
            Submits the provided form data to the FSG website.
                form_data_list (list[FormData]): A list of FormData objects to be submitted.
    """

    def __init__(
        self, clickup_client: ClickUpClient, web_form_automator: WebFormAutomator
    ):
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
