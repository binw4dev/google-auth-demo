import logging
import sys
import os
from datetime import datetime

# ANSI color codes for different log levels
COLORS = {
    "DEBUG": "\033[37m",   # gray
    "INFO": "\033[32m",    # green
    "WARNING": "\033[33m", # yellow
    "ERROR": "\033[31m",   # red
    "CRITICAL": "\033[41m" # red background
}
RESET = "\033[0m"

class ColorFormatter(logging.Formatter):
    """logging formatter with colors"""
    def format(self, record):
        log_color = COLORS.get(record.levelname, "")
        message = super().format(record)
        return f"{log_color}{message}{RESET}"

def setup_logging(log_dir="logs"):
    """logging setup with console and file handlers"""
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(
        log_dir, f"app_{datetime.now().strftime('%Y%m%d')}.log"
    )

    # log formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    color_formatter = ColorFormatter(formatter._fmt, formatter.datefmt)

    # logging handlers - console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(color_formatter)

    # logging handlers - file
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Initialize root logger
    logging.basicConfig(
        level=logging.INFO,
        handlers=[console_handler, file_handler]
    )

    logger = logging.getLogger("app")
    logger.info(f"Logging initialized. Log file: {log_file_path}")
    return logger
