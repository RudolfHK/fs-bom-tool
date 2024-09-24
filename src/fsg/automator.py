from logger.fslogger import global_fs_logger as logger
from fsg.part_dataformat import PartFormData
from fsg.cost_dataformat import CostFormData

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException
import time


class WebFormAutomator:
    """WebFormAutomator is a class designed to automate interactions with a web form on the FSG website.
    It uses Selenium WebDriver to perform tasks such as logging in, navigating to specific pages,
    and filling out forms with provided data.
        driver (webdriver.Chrome): The Chrome WebDriver instance used for browser automation.

    Attributes:
        driver (webdriver.Chrome): The Chrome WebDriver instance.
        login_url (str): The URL for the login page.
        username (str): The username for login.
        password (str): The password for login.
        account_url (str): The URL for the account page.
        fsg_team_name (str): The name of the FSG team.

    Methods:
        __init__(login_url: str, username: str, password: str, account_url: str, fsg_team_name: str):
            Initializes the WebFormAutomator with the necessary credentials and URLs.
        login_fsg_website():
            Logs into the FSG website using the provided credentials.
        navigate_to_form():
            Navigates to the form page on the FSG website.
        create_new_part_entry(entry_data: PartFormData) -> None:
            Completes the workflow for checking if a new entry is already present and then creates a new entry in the form.
        check_ids(table_id: int, id_to_check: int) -> bool:
            Checks if the ID is already present in the table.
        fill_and_submit_part_form(entry_data: PartFormData) -> None:
            Fills the form with the provided data and submits it.
        edit_existing_entry(entry_data: PartFormData) -> None:
            Edits an existing entry in the form. (Not yet implemented)"""

    def __init__(
        self,
        login_url: str,
        username: str,
        password: str,
        account_url: str,
        fsg_team_name: str,
    ):
        self.driver = webdriver.Chrome()
        self.login_url = login_url
        self.username = username
        self.password = password
        self.account_url = account_url
        self.fsg_team_name = fsg_team_name
        self.existing_ids = []

    # Init methods
    def login_fsg_website(self):
        """
        Logs into the FSG website using the provided credentials.
        This method navigates to the login URL, waits for the username and password fields to be present,
        enters the provided credentials, and submits the login form. If the login is successful, a success
        message is logged. If an error occurs during the login process, an error message is logged and the
        browser is closed.
        """
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
        """
        Navigates to the form page on the FSG website.
        This method performs the following steps:
        1. Waits for the team link to be clickable and clicks on it.
        2. Waits for the CBOM link to be clickable and clicks on it.
        3. Logs a success message upon successful navigation.
        If any step fails, it logs an error message and quits the driver.
        """
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

    def get_existing_ids(self) -> list[str]:
        """Get the existing IDs from the BOM table on the FSG website.

        Returns:
            list[str]: A list of existing IDs from the BOM table.
        """
        table = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "bom-table"))
        )

        assembly_rows = table.find_elements(
            By.XPATH, ".//tr[contains(@class, 'grp-assembly')]"
        )
        part_rows = table.find_elements(By.XPATH, ".//tr[starts-with(@id, 'bompart')]")

        assembly_id_list = [
            row.find_elements(By.TAG_NAME, "td")[7] for row in assembly_rows
        ]
        part_id_list = [
            row.find_element(By.CLASS_NAME, "dt-head-center.edit.inline").text
            for row in part_rows
        ]
        return assembly_id_list + part_id_list

    # Main methods
    def create_new_part_entry(self, entry_data: PartFormData) -> None:
        """Complete workflow for checking if the new entry is already present and then creating a new entry in the form.
        This method first checks if an entry with the given custom ID already exists in the BOM table. If it does, it logs
        a message and edits the existing entry. If the entry does not exist, it clicks the button to create a new entry
        and fills out the form with the provided data.

        Args:
            entry_data (PartFormData): The data for the part entry to be created or edited.
        """
        # Check IDs sometimes throws Error during table check: Message: stale element reference:
        if entry_data.custom_id in self.existing_ids:
            logger.info(
                f"Entry with ID {entry_data.custom_id} already exists. Editing..."
            )
            # self.edit_existing_entry(entry_data)
            return
        else:
            new_button = self.driver.find_element(
                By.CSS_SELECTOR, ".dt-button.buttons-create"
            )
            new_button.click()

            logger.info(f"Creating new Entry for ID {entry_data.custom_id}.")
            self.fill_and_submit_part_form(entry_data)
            self.existing_ids.append(entry_data.custom_id)

    # Form filling methods
    def fill_and_submit_part_form(self, entry_data: PartFormData) -> None:
        """Fills the form with the provided data.

        Args:
            entry_data (PartFormData): The data to be entered into the form.
        """
        # Fill 'system' select dropdown
        system_select = self.staleElementRefExHandling("DTE_Field_system")
        system_select.select_by_value(entry_data.system)

        # Fill 'assembly' select dropdown
        assembly_select = self.staleElementRefExHandling("DTE_Field_assembly")
        assembly_options = assembly_select.options.copy()
        logger.info(f"Assembly options: {[option.text for option in assembly_options]}")

        # Check if the entry_data.assembly is in the assembly_select options
        if entry_data.assembly in [option.text for option in assembly_options]:
            assembly_select.select_by_value(entry_data.assembly)
        else:
            logger.warning(
                f"Assembly '{entry_data.assembly}' not found in options. Creating new Assembly"
            )
            assembly_select.select_by_value("_CUSTOMNEW")

            # Fill optional 'assembly_name' if it exists
            if entry_data.assembly_name != "" and entry_data.assembly_name != None:
                self.set_text_input("DTE_Field_assembly_name", entry_data.assembly_name)
            else:
                self.set_user_input_on_missing_value(
                    "Assembly Name", entry_data.part, "DTE_Field_assembly_name"
                )

            # Fill optional 'assembly_comment' if it exists
            if entry_data.assembly_comment != "":
                self.set_text_input(
                    "DTE_Field_assembly_comment", entry_data.assembly_comment
                )
            else:
                self.set_user_input_on_missing_value(
                    "Assembly Comment",
                    entry_data.part,
                    "DTE_Field_assembly_comment",
                )

        # Fill 'sub_assembly' select dropdown, "- none -" is default
        if entry_data.sub_assembly != "- none -" and entry_data.sub_assembly != "":
            sub_assembly_select = self.staleElementRefExHandling(
                "DTE_Field_sub_assembly"
            )
            if entry_data.sub_assembly in [
                option.text for option in sub_assembly_select.options
            ]:
                sub_assembly_select.select_by_value(entry_data.sub_assembly)
            else:
                logger.warning(
                    f"Sub-Assembly '{entry_data.sub_assembly}' not found in options. Creating new Sub-Assembly"
                )
                sub_assembly_select.select_by_value("_CUSTOMNEW")

                # Fill optional 'sub_assembly_name' if it exists
                if entry_data.sub_assembly_name != "":
                    self.set_text_input(
                        "DTE_Field_sub_assembly_name", entry_data.sub_assembly_name
                    )
                else:
                    self.set_user_input_on_missing_value(
                        "Sub Assembly Name",
                        entry_data.part,
                        "DTE_Field_sub_assembly_name",
                    )

        # Fill 'part' text input
        self.set_text_input("DTE_Field_part", entry_data.part)

        # Fill 'makebuy' radio buttons
        makebuy_value = entry_data.makebuy
        if makebuy_value == "m":
            self.driver.find_element(By.ID, "DTE_Field_makebuy_0").click()
        elif makebuy_value == "b":
            self.driver.find_element(By.ID, "DTE_Field_makebuy_1").click()

        # Fill 'comments' text input
        self.set_text_input("DTE_Field_comments", entry_data.comments)

        # Fill 'quantity' text input
        self.set_text_input("DTE_Field_quantity", str(entry_data.quantity))

        # Fill 'custom_id' text input
        self.set_text_input("DTE_Field_part_no", entry_data.custom_id)

        # Find and click the 'Create' button
        create_button = self.driver.find_element(By.CSS_SELECTOR, ".btn.btn")
        create_button.click()

        # Wait until the form is completely submitted and the new entry is visible in the table
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//td[text()='{entry_data.part}']")
                )
            )
            logger.success(
                f"Entry for ID: {entry_data.custom_id} submitted successfully."
            )
        except Exception as e:
            logger.error(f"Error waiting for form submission: {e}")

    def edit_existing_entry(self, entry_data: PartFormData) -> None:
        """Edit an existing entry in the form.

        Args:
            entry_data (PartFormData): The data to be entered into the form.
        """
        raise NotImplementedError

    def fill_and_submit_cost_form(self, cost_data: CostFormData):
        """Fills the cost form with the provided data.

        Args:
            cost_data (CostFormData): _description_
        """
        raise NotImplementedError

    # Helper methods
    def staleElementRefExHandling(self, element_id: str, by: By = By.ID) -> Select:
        """Handle StaleElementReferenceException by retrying to fetch the select element.
        This method attempts to fetch a select element from the web page, retrying up to a
        specified number of times if a StaleElementReferenceException is encountered. If the
        element cannot be fetched after the maximum number of retries, the program will exit.


        Args:
            element_id (str): The ID of the element to fetch.
            by (By, optional): Find element option . Defaults to By.ID.

        Raises:
            SystemExit: If the select element cannot be fetched after multiple attempts.

        Returns:
            Select: The select element fetched successfully.
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((by, element_id))
                )
                select_try = Select(self.driver.find_element(by, element_id))
                return select_try
            except StaleElementReferenceException:
                if attempt < max_retries - 1:
                    logger.warning(
                        "StaleElementReferenceException encountered. Retrying..."
                    )
                    time.sleep(1)
                else:
                    logger.error(
                        "Failed to fetch the select element after multiple attempts."
                    )
                    raise SystemExit(1)

    def set_text_input(self, element_id: str, text: str, by: By = By.ID) -> None:
        """
        Sets the text of an input field identified by its element ID.
        This method waits until the input field is present in the DOM, clears any existing text,
        and then sends the specified text to the input field.
        Args:
            element_id (str): The ID of the input field element.
            text (str): The text to be entered into the input field.
            by (By, optional): The method to locate the element (default is By.ID).
        Returns:
            None
        """
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((by, element_id))
        )
        text_input = self.driver.find_element(by, element_id)
        text_input.clear()
        text_input.send_keys(text)

    def set_user_input_on_missing_value(
        self, field_name: str, part_name: str, element_id: str
    ):
        """
        Prompts the user to input a value for a missing field and sets the input value.

        This method logs an error indicating that a required field value is missing for a specific part.
        It then prompts the user to enter the missing value and sets this value in the corresponding element.

        Args:
            field_name (str): The name of the field that is missing a value.
            part_name (str): The name of the part associated with the missing field.
            element_id (str): The identifier of the element where the input value should be set.

        Returns:
            None
        """
        logger.error(f"{field_name} for part: '{part_name}' not provided.")
        new_input = input(
            f"Please enter the {field_name} and press Enter to continue..."
        )
        self.set_text_input(element_id, new_input)
