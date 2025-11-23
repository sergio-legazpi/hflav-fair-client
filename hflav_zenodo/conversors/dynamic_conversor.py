import json
import os
from typing import Dict, Type, Union, Optional

from genson import SchemaBuilder
from pydantic import BaseModel, ConfigDict, Field, create_model
from hflav_zenodo.processing.data_visualizer import DataVisualizer


class DynamicConversor(BaseModel):
    """Base class to create Pydantic models dynamically from JSON templates"""

    def _get_data_from_dict_file_or_string(
        self, input_data: Union[str, bytes, os.PathLike, Dict]
    ) -> Dict:
        """
        Load data from a dictionary, JSON string, or file path

        Args:
            input_data: JSON string, file path, or dict with example data
        Returns:
            Dictionary with loaded data
        """
        if isinstance(input_data, dict):
            # Already a dictionary
            return input_data
        elif isinstance(input_data, (str, bytes, os.PathLike)) and os.path.exists(
            input_data
        ):
            # Is a file path
            with open(input_data, "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            # Is a JSON string
            return json.loads(input_data)

    def _generate_json_schema(cls, file_path: str):
        builder = SchemaBuilder()

        data = cls._get_data_from_dict_file_or_string(cls, file_path)

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

        field_definitions = {}

        for prop_name, prop_schema in schema.get("properties", {}).items():
            field_type = prop_schema.get("type")
            required = prop_name in schema.get("required", [])

            type_mapping = {
                "string": str,
                "integer": int,
                "number": float,
                "boolean": bool,
                "array": list,
                "object": dict,
            }

            python_type = type_mapping.get(field_type, str)
            if not required:
                python_type = Optional[python_type]
                default = None
            else:
                default = ...
            field_definitions[prop_name] = (python_type, Field(default))

        TemplateModel = create_model(
            schema.get("title", "TemplateModel"),
            __config__=ConfigDict(strict=True),
            **field_definitions
        )
        data_dict = cls._get_data_from_dict_file_or_string(cls, data_path)
        instance = TemplateModel(**data_dict)

        return instance
