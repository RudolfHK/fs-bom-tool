from config_loader.confighandler import ConfigHandler
from pathlib import Path
from logger.fslogger import global_fs_logger as logger
from dotenv import load_dotenv
import os
import requests


class FSConfigParser:
    def __init__(self) -> None:
        self.config: ConfigHandler = ConfigHandler(Path("configs/default.toml"))
        self.__parse_args()

    def __parse_args(self) -> None:
        """parse all arguments of the config file"""
        try:
            # [fsgurl]
            self.fsg_url: str = self.config.get_param("fsgurl", "url")
            self.fsg_login_url: str = self.__parse_fsg_credentials(
                self.config.get_param("fsgurl", "login_url")
            )

            # [debug]
            self.debug: bool = self.config.get_param("debug", "performance_logger")

            # [clickup]
            self.api_server: str = self.config.get_param("clickup", "api_server")
            self.clickup_token: str = self.__parse_clickup_api(self.api_server)

        except KeyError as error:
            logger.error(
                f"Config option[{error}] not found in config file[{self.config}], please add that. Check default.toml for reference."
            )
            raise SystemExit(1)

    def __parse_fsg_credentials(self, fsg_login_url: str) -> str:

        dotenv_path = Path(".env")
        if dotenv_path.exists():
            load_dotenv(dotenv_path)
        else:
            logger.error(".env file not found")
            raise SystemExit(1)

        fsg_user = os.environ.get("FSGUSER")
        fsg_passwd = os.environ.get("FSGPASSWD")

        if fsg_user == "" or fsg_user == None:
            logger.error("check environment variables, FSGUSER in .env not set")
            raise SystemExit(1)
        if fsg_passwd == "" or fsg_passwd == None:
            logger.error("check environment variables, FSGPASSWD in .env not set")
            raise SystemExit(1)
        if fsg_login_url != "" and fsg_login_url != None:
            response = requests.get(fsg_login_url, auth=(fsg_user, fsg_passwd))
            if response.status_code == 200:
                self.fsg_user = fsg_user
                self.fsg_passwd = fsg_passwd
                logger.success("Successfully authenticated with FSG.")
                return fsg_login_url
            else:
                logger.error(
                    f"Login failed with status code {response.status_code}. Please check your credentials."
                )
            raise SystemExit(1)
        else:
            logger.error("check environment variables, fsg_login_url not set")
            raise SystemExit(1)

    def __parse_clickup_api(self, api_server: str) -> str:
        load_dotenv()

        clickup_api_token = os.environ.get("CLICKUPAPIKEY")
        clickup_workspace_name = os.environ.get("CLICKUPWORKSPACENAME")
        logger.info(clickup_workspace_name)

        if clickup_api_token == "" or clickup_api_token == None:
            logger.error("check environment variables, clickup_api_key in .env not set")
            raise SystemExit(1)

        if clickup_workspace_name == "" or clickup_workspace_name == None:
            logger.error(
                "check environment variables, clickup_workspace_name in .env not set"
            )
            raise SystemExit(1)

        if api_server != "" and api_server != None:
            headers = {"Authorization": clickup_api_token}
            response = requests.get(api_server, headers=headers)

            if response.status_code == 200:
                logger.success("Successfully authenticated with ClickUp API.")
                teams = response.json().get("teams", [])
                if not teams:
                    logger.error("No workspaces found.")
                    raise SystemExit(1)
                else:
                    for team in teams:
                        if team.get("name") == clickup_workspace_name:
                            self.clickup_workspace_id = team.get("id")
                            self.clickup_workspace_name = clickup_workspace_name
                            logger.success(f"Found workspace: {clickup_workspace_name}")
                            break
                    else:
                        logger.error(
                            f"Workspace name '{clickup_workspace_name}' not found."
                        )
                        raise SystemExit(1)
                return clickup_api_token
            else:
                logger.error(
                    f"Failed to authenticate with ClickUp API: {response.status_code}, {response.text}"
                )
                raise SystemExit(1)
        else:
            logger.error("check config variables, api_server not set")
            raise SystemExit(1)


# https://www.merge.dev/blog/how-to-use-python-to-get-tasks-from-clickup

FSCONFIG = FSConfigParser()
