from logger.fslogger import global_fs_logger as logger
import requests


class ClickUpClient:
    def __init__(self, api_token: str, api_server: str, workspace_id: str):
        self.api_token = api_token
        self.api_server = api_server
        self.workspace_id = workspace_id

    def build_get_request(self, endpoint: str, params: dict = None) -> dict:
        """Builds a GET request to the ClickUp API.

        Args:
            endpoint (str): adress that gets appended to the api_server address.
            params (dict, optional): Not Implemented yet. Defaults to None.

        Returns:
            dict: json response from the API.
        """
        url = f"{self.api_server}/{endpoint}"
        logger.info(f"GET request to {url}")
        headers = {"Authorization": self.api_token, "Content-Type": "application/json"}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            response_json: dict = response.json()
            return response_json
        else:
            logger.error(
                f"Failed to get data: {response.status_code} - {response.text}"
            )
            response.raise_for_status()

    def filter_system_lists(self, list_response: dict, trim: bool = True) -> list[dict]:
        """Filters out FSG BOM Tool system lists from the workspace lists. This also ignore archived lists.

        Args:
            list_response (dict): jsno response from the ClickUp API.
            trim (bool, optional): trims data to essentials (id,name,task_count,folder{id,name},space{id,name}) . Defaults to False.

        Returns:
            list: list of system lists.
            without trim: {'id': '1', 'name': 'SU.24_Suspension', 'orderindex': 6, 'content': '', 'status': None, 'priority': None, 'assignee': None, 'due_date': None, 'start_date': None, 'folder': {'id': '3', 'name': 'Baugruppen', 'hidden': False, 'access': True}, 'space': {'id': '5', 'name': 'Fahrwerk', 'access': True}, 'archived': False, 'override_statuses': True, 'permission_level': 'create'},
            with trim: {'id': '1', 'name': 'SU.24_Suspension'}
        """
        systems = [
            "BR",
            "EL",
            "EN",
            "FR",
            "MS",
            "ST",
            "SU",
            "WT",
        ]
        lists = list_response.get("lists", [])
        filtered_list = [
            l for l in lists if l.get("name")[:2] in systems and not l.get("archived")
        ]
        if trim:
            trimmed_response = []
            for item in filtered_list:
                trimmed_item = {
                    k: item[k]
                    for k in [
                        "id",
                        "name",
                    ]
                    if k in item
                }
                trimmed_response.append(trimmed_item)
            return trimmed_response
        return filtered_list

    def filter_system_tasks(self, list_response: dict, trim: bool = True) -> list[dict]:
        pass
        # Logic to fetch task details using task_id
