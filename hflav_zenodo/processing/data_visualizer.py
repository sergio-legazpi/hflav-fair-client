import json
from typing import Any, Type

from pydantic import BaseModel
from rich.table import Table
from rich import print as rprint, print_json


class DataVisualizer:
    """Class to visualize Pydantic models in a simplified and visual way"""

    @staticmethod
    def print_schema(schema: dict):
        print_json(json.dumps(schema))

    @staticmethod
    def print_json_data(data: Type[BaseModel]):
        print_json(data.model_dump_json(indent=4))
