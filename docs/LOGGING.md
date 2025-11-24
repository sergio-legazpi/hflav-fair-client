# Logging Configuration

The `hflav_zenodo` package uses Python's built-in logging module for all output messages.

## Usage

The logger is centrally configured in `hflav_zenodo/logger.py`. All modules import and use this logger:

```python
from hflav_zenodo.logger import get_logger

logger = get_logger(__name__)

# Use different log levels as appropriate
logger.debug("Detailed debug information")
logger.info("General information about program execution")
logger.warning("Warning messages")
logger.error("Error messages")
logger.critical("Critical error messages")
```

## Log Levels

The default log level is `INFO`. You can change the log level using the `set_log_level` function:

```python
import logging
from hflav_zenodo.logger import get_logger, set_log_level

logger = get_logger(__name__)
set_log_level(logger, logging.DEBUG)  # Show all messages including debug
```

## Log Format

Logs are formatted as:
```
YYYY-MM-DD HH:MM:SS - module_name - LEVEL - message
```

Example:
```
2025-11-24 10:30:45 - hflav_zenodo.services.services - INFO - Getting record with id 12345...
```

## Data Visualization

Note: The `DataVisualizer` class uses `rich.print_json` for formatted data display. This is intentional for presenting structured data to end users and is separate from the logging system.
