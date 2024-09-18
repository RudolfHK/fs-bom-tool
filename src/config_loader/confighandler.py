from pathlib import Path
import toml
from logger.fslogger import global_fs_logger as logger


class ConfigHandler:
    """This class is for handling arguments or configs to load specific conditions"""

    def __init__(self, config_file_path: Path) -> None:
        self.config_file_path = config_file_path
        if not self.config_file_path.is_file():
            logger.error(f"config file [{self.config_file_path}] not found !")
            SystemExit(1)
        self.config = {}

        with open(self.config_file_path, "r") as f:
            self.config = toml.load(f)

    def get_param(self, section, key):
        """Get a configuration parameter"""
        return self.config.get(section, {}).get(key)

    def get_section(self, section):
        """Get a configuration section"""
        return self.config.get(section)
