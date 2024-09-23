from logger.fslogger import global_fs_logger as logger
from fsg.dataformat import FormData

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class WebFormAutomator:
    def __init__(
        self,
        login_url: str,
        username: str,
        password: str,
        account_url: str,
        fsg_team_name: str,
    ):
        """
        Initializes the Automator class with the necessary credentials and URLs.
        Args:
            login_url (str): The URL for the login page.
            username (str): The username for login.
            password (str): The password for login.
            account_url (str): The URL for the account page.
            fsg_team_name (str): The name of the FSG team.
        Attributes:
            driver (webdriver.Chrome): The Chrome WebDriver instance.
            login_url (str): The URL for the login page.
            username (str): The username for login.
            password (str): The password for login.
            account_url (str): The URL for the account page.
            fsg_team_name (str): The name of the FSG team.
        """
        self.driver = webdriver.Chrome()
        self.login_url = login_url
        self.username = username
        self.password = password
        self.account_url = account_url
        self.fsg_team_name = fsg_team_name

    def login_fsg_website(self):
        """Logs into the FSG website using the provided credentials."""
        self.driver.get(self.login_url)

        try:
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "user"))
            )
            password_field = self.driver.find_element(By.ID, "pass")

            username_field.send_keys(self.username)
            password_field.send_keys(self.password)
            password_field.send_keys(Keys.RETURN)

            # WebDriverWait(self.driver, 10).until(EC.url_changes(self.account_url))
            logger.success("Successfully logged in.")

        except Exception as e:
            logger.error(f"Error during login: {e}")
            self.driver.quit()

    def navigate_to_form(self):
        """Navigates to the form page on the FSG website. From Profile Page to Team Page and then to CBOM Page"""
        try:
            team_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, self.fsg_team_name))
            )
            team_link.click()

            cbom_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "CBOM"))
            )
            cbom_link.click()
            logger.success("Successfully navigated to form.")

        except Exception as e:
            logger.error(f"Error navigating to form: {e}")
            self.driver.quit()

    def create_new_entry(self, entry_data: FormData) -> None:
        """Complete workflow for checking if the new entry is already present and then creating a new entry in the form.

        Args:
            entry_data (FormData): _description_
        """
        # Check IDs sometimes throws Error during table check: Message: stale element reference:
        # if self.check_ids("bom-table", entry_data.custom_id):
        #     logger.info(f"Entry with ID {entry_data.custom_id} already exists.")
        #     return
        # else:
        new_button = self.driver.find_element(
            By.CSS_SELECTOR, ".dt-button.buttons-create"
        )
        new_button.click()

        self.fill_and_submit_form(entry_data)
        logger.success("Form filled successfully!")

    def check_ids(self, table_id: int, id_to_check: int) -> bool:
        """Checks if the ID is already present in the table.


        Args:
            table_id (int): html id of the table. (usually "bom-table")
            id_to_check (str): ID of the new entry to check.

        Returns:
            bool: True if present, False if not present.
        """
        try:
            table = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, table_id))
            )
            rows = table.find_elements(By.XPATH, ".//tbody/tr")

            for row in rows:
                custom_id_column = row.find_elements(By.TAG_NAME, "td")[
                    7
                ]  # Column with the IDs
                id_value = custom_id_column.text.strip()

                if id_value == id_to_check:
                    logger.info(f"ID {id_to_check} is already present in the table.")
                    return True

            return False
        except Exception as e:
            logger.error(f"Error during table check: {e}")
            self.driver.quit()

    def fill_and_submit_form(self, entry_data: FormData) -> None:
        """Fills the form with the provided data.

        Args:
            entry_data (FormData): The data to be entered into the form.
        """
        # Fill 'system' select dropdown
        system_select = Select(self.driver.find_element(By.ID, "DTE_Field_system"))
        system_select.select_by_value(entry_data.system)

        # Fill 'assembly' select dropdown
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "DTE_Field_assembly"))
        )
        assembly_select = Select(self.driver.find_element(By.ID, "DTE_Field_assembly"))
        assembly_select.select_by_value(entry_data.assembly)

        # Fill optional 'assembly_name' if it exists
        if entry_data.assembly_name != "":
            assembly_name_input = self.driver.find_element(
                By.ID, "DTE_Field_assembly_name"
            )
            assembly_name_input.clear()
            assembly_name_input.send_keys(entry_data.assembly_name)

        # Fill optional 'assembly_comment' if it exists
        if entry_data.assembly_comment != "":
            assembly_comment_input = self.driver.find_element(
                By.ID, "DTE_Field_assembly_comment"
            )
            assembly_comment_input.clear()
            assembly_comment_input.send_keys(entry_data.assembly_comment)

        # Fill 'sub_assembly' select dropdown, "- none -" is default
        if entry_data.sub_assembly != "- none -" and entry_data.sub_assembly != "":
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "DTE_Field_sub_assembly"))
            )
            sub_assembly_select = Select(
                self.driver.find_element(By.ID, "DTE_Field_sub_assembly")
            )
            sub_assembly_select.select_by_value(entry_data.sub_assembly)

        # Fill optional 'sub_assembly_name' if it exists
        if entry_data.sub_assembly_name != "":
            sub_assembly_name_input = self.driver.find_element(
                By.ID, "DTE_Field_sub_assembly_name"
            )
            sub_assembly_name_input.clear()
            sub_assembly_name_input.send_keys(entry_data.sub_assembly_name)

        # Fill 'part' text input
        part_input = self.driver.find_element(By.ID, "DTE_Field_part")
        part_input.clear()
        part_input.send_keys(entry_data.part)

        # Fill 'makebuy' radio buttons
        makebuy_value = entry_data.makebuy
        if makebuy_value == "m":
            self.driver.find_element(By.ID, "DTE_Field_makebuy_0").click()
        elif makebuy_value == "b":
            self.driver.find_element(By.ID, "DTE_Field_makebuy_1").click()

        # Fill 'comments' text input
        comments_input = self.driver.find_element(By.ID, "DTE_Field_comments")
        comments_input.clear()
        comments_input.send_keys(entry_data.comments)

        # Fill 'quantity' text input
        quantity_input = self.driver.find_element(By.ID, "DTE_Field_quantity")
        quantity_input.clear()
        quantity_input.send_keys(entry_data.quantity)

        # Fill 'sub_costs' if needed (if not disabled)
        if not self.driver.find_element(By.ID, "DTE_Field_sub_costs").get_attribute(
            "disabled"
        ):
            sub_costs_input = self.driver.find_element(By.ID, "DTE_Field_sub_costs")
            sub_costs_input.clear()
            sub_costs_input.send_keys(entry_data.sub_costs)

        # Find and click the 'Create' button
        create_button = self.driver.find_element(By.CSS_SELECTOR, ".btn.btn")
        create_button.click()

    def edit_existing_entry(self, entry_data: FormData) -> None:
        """Edit an existing entry in the form.

        Args:
            entry_data (FormData): The data to be entered into the form.
        """
        raise NotImplementedError
