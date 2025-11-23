from dataclasses import fields
import json
import os
from types import SimpleNamespace
from typing import Dict, Type, Union, Optional

from genson import SchemaBuilder
import jsonschema
from pydantic import BaseModel, ConfigDict, Field, create_model
from hflav_zenodo.processing.data_visualizer import DataVisualizer


class DynamicConversor(BaseModel):
    """Base class to create Pydantic models dynamically from JSON templates"""

    def _generate_json_schema(cls, file_path: str):
        builder = SchemaBuilder()

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        builder.add_object(data)
        schema = builder.to_schema()

        schema["$schema"] = "http://json-schema.org/draft-07/schema#"

        return schema

    @classmethod
    def generate_instance_from_template_and_data(
        cls, template_path: str, data_path: str
    ) -> Type[BaseModel]:
        schema = cls._generate_json_schema(
            cls,
            template_path,
        )
        print("Template JSON Schema:")
        DataVisualizer.print_schema(schema)

        with open(data_path, "r", encoding="utf-8") as file:
            data_dict = json.load(file)
        jsonschema.validate(instance=data_dict, schema=schema)

        return SimpleNamespace(**data_dict)
