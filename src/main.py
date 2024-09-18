from logger.fslogger import global_fs_logger as logger
from clickup.client import ClickUpClient
from fsg.automator import WebFormAutomator
from taskmanager import TaskManager
from config_loader.fsconfig import FSCONFIG


def main():
    logger.info("Starting the ClickUp to FSG automation tool.")

    # Initialize ClickUp client
    # clickup_client = ClickUpClient()
    # Initialize WebFormAutomator
    # web_form_automator = WebFormAutomator()

    # Initialize TaskManager
    # task_manager = TaskManager(clickup_client, web_form_automator)
    # Extract and submit tasks
    # task_manager.extract_and_submit_tasks(workspace_id)
    logger.info("ClickUp to FSG automation completed successfully.")


if __name__ == "__main__":
    main()
# Plannend Workflow:

# Extract data from ClickUp using the ClickUp API.

# Transform the data into the format required by the FSG website.

# Automate the input on the FSG website using python Selenium.

# Error handling to ensure smooth data transfer and deal with any issues like missing fields or API errors.
