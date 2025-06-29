import logging
import os
from datetime import datetime
from pathlib import Path

# Global variables
_module_name = None
_logger = None
_current_log_file = None


def init(module_name):
    """Initialize the logger with a module name"""
    global _module_name, _logger, _current_log_file

    _module_name = module_name

    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Create daily log file name
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = log_dir / f"{today}.log"

    _current_log_file = log_file

    # Create custom logger
    _logger = logging.getLogger(module_name)
    _logger.setLevel(logging.DEBUG)

    # Clear any existing handlers
    _logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s [%(name)s] %(message)s", datefmt="%H:%M:%S"
    )

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    _logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    _logger.addHandler(console_handler)

    # Prevent duplicate logs
    _logger.propagate = False


def _check_date_change():
    """Check if date has changed and create new log file if needed"""
    global _current_log_file, _logger

    if not _logger or not _module_name:
        return

    today = datetime.now().strftime("%Y-%m-%d")
    expected_log_file = Path("logs") / f"{today}.log"

    if _current_log_file != expected_log_file:
        # Date has changed, reinitialize logger
        init(_module_name)


def info(message):
    """Log an info message"""
    if not _logger:
        raise RuntimeError("Logger not initialized. Call logger.init() first.")

    _check_date_change()
    _logger.info(message)


def error(message):
    """Log an error message"""
    if not _logger:
        raise RuntimeError("Logger not initialized. Call logger.init() first.")

    _check_date_change()
    _logger.error(message)


def warning(message):
    """Log a warning message"""
    if not _logger:
        raise RuntimeError("Logger not initialized. Call logger.init() first.")

    _check_date_change()
    _logger.warning(message)


def debug(message):
    """Log a debug message"""
    if not _logger:
        raise RuntimeError("Logger not initialized. Call logger.init() first.")

    _check_date_change()
    _logger.debug(message)


def critical(message):
    """Log a critical message"""
    if not _logger:
        raise RuntimeError("Logger not initialized. Call logger.init() first.")

    _check_date_change()
    _logger.critical(message)
