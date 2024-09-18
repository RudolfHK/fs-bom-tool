from logger.fslogger import global_fs_logger as logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class WebFormAutomator:
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
        self.fsg_team_name = fsg_team_name  # Not implemented yet

    def login_fsg_website(self):
        self.driver.get(self.login_url)

        try:
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "user"))
            )
            password_field = self.driver.find_element(By.ID, "pass")

            username_field.send_keys(self.username)
            password_field.send_keys(self.password)
            password_field.send_keys(Keys.RETURN)

            WebDriverWait(self.driver, 10).until(EC.url_changes(self.account_url))
            logger.success("Successfully logged in.")

        except Exception as e:
            logger.error(f"Error during login: {e}")
            self.driver.quit()

    def navigate_to_form(self):
        try:
            team_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, self.fsg_team_name))
            )
            team_link.click()

            cbom_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "CBOM"))
            )
            cbom_link.click()

            logger.info(f"Current URL: {self.driver.current_url}")
            logger.success("Successfully navigated to form.")

        except Exception as e:
            logger.error(f"Error navigating to form: {e}")
            self.driver.quit()

    def fill_form(self, task_data):
        pass

    def submit_form(self):
        pass
        # Logic to submit the form
