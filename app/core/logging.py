import logging
import sys
from app.core.config import settings

# --- Configuration for production-ready logger ---

# Create a logger object
logger = logging.getLogger("url_shortner_app")

# Set the logging level (e.g., INFO, DEBUG, WARNING)
logger.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create a handler to write logs to the console (stdout)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# Add the handler to the logger
if not logger.handlers: # Avoid adding handlers multiple times on reload
    logger.addHandler(console_handler)