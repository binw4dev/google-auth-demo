import logging
import sys
import os
from datetime import datetime

# ANSI 颜色码定义
COLORS = {
    "DEBUG": "\033[37m",   # 灰
    "INFO": "\033[32m",    # 绿
    "WARNING": "\033[33m", # 黄
    "ERROR": "\033[31m",   # 红
    "CRITICAL": "\033[41m" # 红底
}
RESET = "\033[0m"

class ColorFormatter(logging.Formatter):
    """带颜色的日志格式器"""
    def format(self, record):
        log_color = COLORS.get(record.levelname, "")
        message = super().format(record)
        return f"{log_color}{message}{RESET}"

def setup_logging(log_dir="logs"):
    """集中配置日志"""
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(
        log_dir, f"app_{datetime.now().strftime('%Y%m%d')}.log"
    )

    # 日志格式
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    color_formatter = ColorFormatter(formatter._fmt, formatter.datefmt)

    # 控制台输出（带颜色）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(color_formatter)

    # 文件输出（不带颜色）
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # 初始化 root logger
    logging.basicConfig(
        level=logging.INFO,
        handlers=[console_handler, file_handler]
    )

    logger = logging.getLogger("app")
    logger.info(f"Logging initialized. Log file: {log_file_path}")
    return logger
