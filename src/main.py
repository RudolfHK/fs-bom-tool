from logger.fslogger import global_fs_logger as logger
from clickup.client import ClickUpClient
from fsg.automator import WebFormAutomator
from clickup.taskmanager import TaskManager
from config_loader.fsconfig import FSCONFIG
from fsg.part_dataformat import PartFormData


def main():

    logger.info("Initializing ClickUp Client")
    clickup_client = ClickUpClient(
        FSCONFIG.clickup_token, FSCONFIG.api_server, FSCONFIG.clickup_workspace_id
    )

    logger.info("Initializing WebFormAutomator")
    web_form_automator = WebFormAutomator(
        FSCONFIG.fsg_login_url,
        FSCONFIG.fsg_user,
        FSCONFIG.fsg_passwd,
        FSCONFIG.fsg_account_url,
        FSCONFIG.fsg_team_name,
    )

    logger.info("Initializing TaskManager")
    task_manager = TaskManager(clickup_client, web_form_automator)
    # json_response = task_manager.import_entries()
    # form_data_list = task_manager.convert_data(json_response)
    # task_manager.submit_to_fsg(form_data_list)
    logger.success("Automation successfull")


if __name__ == "__main__":
    main()
