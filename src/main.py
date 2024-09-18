from logger.fslogger import global_fs_logger as logger
from clickup.client import ClickUpClient
from fsg.automator import WebFormAutomator
from taskmanager import TaskManager
from config_loader.fsconfig import FSCONFIG


def main():
    logger.info("Starting the ClickUp to FSG automation tool.")

    # clickup_client = ClickUpClient(
    #     FSCONFIG.clickup_token, FSCONFIG.api_server, FSCONFIG.clickup_workspace_id
    # )
    # system_lists = clickup_client.filter_system_lists(
    #     clickup_client.build_get_request(f"team/{FSCONFIG.clickup_workspace_id}/list"),
    # )
    # for list_id in system_lists:
    #     tasks = clickup_client.build_get_request(f"list/{list_id.get("id")}/task")
    #     logger.info(tasks)

    # Initialize WebFormAutomator
    web_form_automator = WebFormAutomator(
        FSCONFIG.fsg_login_url,
        FSCONFIG.fsg_user,
        FSCONFIG.fsg_passwd,
        FSCONFIG.fsg_account_url,
        "greenBEAR",
        # FSCONFIG.fsg_team_name,
    )
    web_form_automator.login_fsg_website()
    web_form_automator.navigate_to_form()
    # Initialize TaskManager
    # task_manager = TaskManager(clickup_client, web_form_automator)
    # Extract and submit tasks

    logger.info("ClickUp to FSG automation completed successfully.")


if __name__ == "__main__":
    main()
# Plannend Workflow:

# Extract data from ClickUp using the ClickUp API.

# Transform the data into the format required by the FSG website.

# Automate the input on the FSG website using python Selenium.

# Error handling to ensure smooth data transfer and deal with any issues like missing fields or API errors.
