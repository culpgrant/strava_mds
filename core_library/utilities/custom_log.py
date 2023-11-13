"""
Custom Logging Config
"""
import logging


def setup_console_logger(logger_name=__name__, level=logging.DEBUG):
    """Create the custom logger (temp function for now)"""
    # Create a logger
    logger = logging.getLogger(logger_name)

    # Set the logging level
    logger.setLevel(level)

    # Create a console handler and set its level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Create a formatter and attach it to the handler
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(console_handler)

    return logger
