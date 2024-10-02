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

    part_form_data_list = [
        # Item 1
        PartFormData(
            system="BR",
            assembly="Brake Lines",
            assembly_name="",
            assembly_comment="",
            sub_assembly="- none -",
            sub_assembly_name="",
            part="Hydraulic Brake Line",
            makebuy="b",
            comments="TEST",
            quantity=2,
            custom_id="123",
        ),
        # Item 2
        PartFormData(
            system="EL",
            assembly="TEST assembly",
            assembly_name="This is a new assembly",
            assembly_comment="Harness for engine components",
            sub_assembly="- none -",
            sub_assembly_name="",
            part="Wiring Loom",
            makebuy="m",
            comments="TEST",
            quantity=1,
            custom_id="456",
        ),
        # Item 3
        PartFormData(
            system="SU",
            assembly="Suspension Arms",
            assembly_name="TEST",
            assembly_comment="Front suspension arms replacement",
            sub_assembly="new",
            sub_assembly_name="WOW a subassembly",
            part="Carbon Suspension Arm",
            makebuy="b",
            comments="TEST",
            quantity=2,
            custom_id="789",
        ),
    ]

    logger.info("Initializing TaskManager")
    task_manager = TaskManager(clickup_client, web_form_automator)
    # json_response = task_manager.import_entries()
    # form_data_list = task_manager.convert_data(json_response)
    task_manager.submit_to_fsg(part_form_data_list)
    logger.success("Automation successfull")


if __name__ == "__main__":
    main()
