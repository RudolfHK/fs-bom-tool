from __future__ import annotations
from loguru import logger
from pathlib import Path
import sys
from datetime import datetime
from collections import Counter


# init empty loguru logger as global_fs_logger
global_fs_logger = logger
global_fs_logger.remove()

# config logging paths and files
global_logpath: Path = Path.cwd() / ".logs"
global_logpath.mkdir(exist_ok=True)

instance_logpath = global_logpath / datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
instance_logpath.mkdir(exist_ok=True)

global_logfile = instance_logpath / "global.log"


# log message configs
time_format = "<y>{time:YYYY-MM-DD HH:mm:ss.SSS}</y>"
level_format = "<level>{level: <8}</level>"
log_message_format = (
    "<cyan>{module}</cyan>:<cyan>{function}</cyan>:<y>{line}</y> - <w>{message}</w>"
)

# custom log levels
global_fs_logger.level("SUCCESS", color="<g>")
global_fs_logger.level("WARNING", color="<y>")
global_fs_logger.level("ERROR", color="<r>")

# logging sinks
global_fs_logger.add(
    sys.stdout,
    format=f"{time_format} | {level_format} | {log_message_format}",
    level=20,
)
global_fs_logger.add(
    str(global_logfile),
    format=f"{time_format} | {level_format} | {log_message_format}",
    level=1,
)

# Initialize a Counter object and errorlist
log_counter = Counter()
error_messages = []


# Define a custom sink function for log counter
def count_sink(message):
    record = message.record
    level = record["level"].name
    log_counter[level] += 1
    if level == "ERROR":
        error_messages.append(message)


# Configure the logger to use the custom sink function
global_fs_logger.add(
    count_sink,
    level=1,
)


# Init complete Start Message
logger.info("--------------Starting the FSG BOM Automation --------------")
