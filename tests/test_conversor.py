import json
import tempfile
import os
import pytest
from typing import List, Type, Dict, Union, get_origin, get_args
from pydantic import BaseModel

from hflav_zenodo.conversors.dynamic_conversor import DynamicConversor

# Importa tu clase DynamicConversor
# from your_module import DynamicConversor


class TestDynamicConversor:
    """Test suite for DynamicConversor class"""

    @pytest.fixture
    def template_data(self):
        """Fixture with the example template data"""
        return {
            "title": "sin(2β) ≡ sin(2φ1)",
            "measurements": [
                {
                    "name": "J/ψKS (ηCP=-1)",
                    "inputs": [
                        {
                            "name": "BaBar",
                            "value": {
                                "central": 0.657,
                                "statistical": 0.036,
                                "systematic": 0.012,
                                "unit": "rad",
                            },
                            "comment": "N(BB)=465M",
                            "References": [
                                {
                                    "arxiv": "0902.1708",
                                    "publication": "PRD 79 (2009) 072009",
                                    "doi": "10.1103/PhysRevD.79.072009",
                                }
                            ],
                        }
                    ],
                    "average": {
                        "value": {
                            "central": 0.695,
                            "uncertainty": 0.019,
                            "unit": "rad",
                        },
                        "comment": "0.018 stat-only",
                    },
                }
            ],
            "averages_correlation": [[0.99, 0.01], [0.01, 0.99]],
        }

    @pytest.fixture
    def real_data(self):
        """Fixture with the real data example"""
        return {
            "title": "HFLAV Tau averages, lifetime",
            "measurements": [
                {
                    "name": "tau lifetime [fs]",
                    "vname": "tau_life",
                    "inputs": [
                        {
                            "name": "ALEPH",
                            "vname": "tau_life_ALEPH_pub_BARATE_1997R",
                            "value": {
                                "central": 290.1,
                                "statistical": 1.5,
                                "systematic": 1.1,
                            },
                            "References": [
                                {
                                    "bibtex": "ALEPH:1997roz",
                                    "publication": "Phys. Lett. B 414 (1997) 362--372",
                                    "doi": "10.1016/S0370-2693(97)01116-7",
                                    "arxiv": "hep-ex/9710026",
                                }
                            ],
                        }
                    ],
                    "average": {
                        "value": {
                            "central": 290.290848172575,
                            "uncertainty": 0.525213667384673,
                        }
                    },
                }
            ],
            "averages_correlation": [[1]],
        }

    def test_create_instance_with_dict(self, template_data, real_data):
        """Test creating model instance with dictionary data"""
        # Create model from template
        models = DynamicConversor.from_json(template_data)
        model_class = models["main"]

        # Create instance with real data as dict
        instance = DynamicConversor.create_instance(model_class, real_data)

        assert isinstance(instance, BaseModel)
        assert instance.title == "HFLAV Tau averages, lifetime"
        assert len(instance.measurements) == 1
        assert instance.measurements[0].name == "tau lifetime [fs]"

    def test_create_instance_with_json_string(self, template_data, real_data):
        """Test creating model instance with JSON string"""
        # Create model from template
        models = DynamicConversor.from_json(template_data)
        model_class = models["main"]

        # Convert real data to JSON string
        json_string = json.dumps(real_data)

        # Create instance with JSON string
        instance = DynamicConversor.create_instance(model_class, json_string)

        assert isinstance(instance, BaseModel)
        assert instance.title == "HFLAV Tau averages, lifetime"

    def test_create_instance_from_file(self, template_data, real_data):
        """Test creating model instance from file with real data"""
        # Create temporary file with real data
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(real_data, f)
            real_data_file = f.name

        try:
            # Create model from template
            models = DynamicConversor.from_json(template_data)
            model_class = models["main"]

            # Create instance from file
            instance = DynamicConversor.create_instance(model_class, real_data_file)

            assert isinstance(instance, BaseModel)
            assert instance.title == "HFLAV Tau averages, lifetime"
        finally:
            os.unlink(real_data_file)

    def test_from_json_with_dict(self, template_data):
        """Test creating models from dictionary template"""
        models = DynamicConversor.from_json(template_data)

        assert "main" in models
        assert issubclass(models["main"], BaseModel)

        # Check that model has expected fields (Pydantic v2 way)
        model_fields = models["main"].model_fields
        assert "title" in model_fields
        assert "measurements" in model_fields
        assert "averages_correlation" in model_fields

    def test_from_json_with_json_string(self, template_data):
        """Test creating models from JSON string"""
        json_string = json.dumps(template_data)
        models = DynamicConversor.from_json(json_string)

        assert "main" in models
        assert issubclass(models["main"], BaseModel)

    def test_from_json_with_file_path(self, template_data):
        """Test creating models from file path"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(template_data, f)
            temp_file = f.name

        try:
            models = DynamicConversor.from_json(temp_file)
            assert "main" in models
            assert issubclass(models["main"], BaseModel)
        finally:
            os.unlink(temp_file)

    def test_nested_structure_creation(self, template_data):
        """Test that nested structures are properly created"""
        models = DynamicConversor.from_json(template_data)
        model_class = models["main"]

        # Check measurements structure (Pydantic v2 way)
        measurements_field = model_class.model_fields["measurements"]
        field_type = measurements_field.annotation

        # In Pydantic v2, optional fields are Union[Type, None]
        # So we need to check the origin and then the args
        origin = get_origin(field_type)

        if origin is Union:
            # For Optional fields, it's Union[ActualType, NoneType]
            # We need to get the first type argument (the actual type)
            type_args = get_args(field_type)
            # The first argument is the actual type, the second is NoneType
            actual_type = type_args[0]
            origin = get_origin(actual_type)

        # Check if it's a List type
        assert origin is list or origin is List, f"Expected List, got {origin}"

        # Check that we can create an instance with partial data
        partial_data = {
            "title": "Test Title",
            "measurements": [],
            "averages_correlation": [],
        }
        instance = model_class(**partial_data)
        assert instance.title == "Test Title"
        assert instance.measurements == []

    def test_optional_fields(self, template_data):
        """Test that all fields are optional as intended"""
        models = DynamicConversor.from_json(template_data)
        model_class = models["main"]

        # Should be able to create instance with minimal data
        minimal_data = {}
        instance = model_class(**minimal_data)

        # All fields should be None when not provided
        assert instance.title is None
        assert instance.measurements is None
        assert instance.averages_correlation is None

    def test_complex_nested_data(self, template_data):
        """Test with complex nested data structures"""
        complex_data = {
            "title": "Complex Test",
            "measurements": [
                {
                    "name": "Test Measurement",
                    "inputs": [
                        {
                            "name": "Test Input",
                            "value": {
                                "central": 1.0,
                                "statistical": 0.1,
                                "systematic": 0.05,
                            },
                            "comment": "Test comment",
                            "References": [
                                {"arxiv": "1234.5678", "publication": "Test Journal"}
                            ],
                        }
                    ],
                    "average": {
                        "value": {"central": 1.0, "uncertainty": 0.1},
                        "comment": "Average comment",
                    },
                }
            ],
            "averages_correlation": [[1.0]],
        }

        models = DynamicConversor.from_json(template_data)
        model_class = models["main"]
        instance = model_class(**complex_data)

        assert instance.title == "Complex Test"
        assert instance.measurements[0].name == "Test Measurement"
        assert instance.measurements[0].inputs[0].name == "Test Input"

    def test_data_validation(self, template_data):
        """Test that data validation works correctly"""
        models = DynamicConversor.from_json(template_data)
        model_class = models["main"]

        # Test with valid data types that match the expected structure
        # Pydantic v2 is strict about types, even for optional fields
        valid_data = {
            "title": "Test Title",  # Must be string
            "measurements": [],  # Must be list (even if empty)
            "averages_correlation": [],  # Must be list (even if empty)
        }

        # Should create instance without errors
        instance = model_class(**valid_data)
        assert instance is not None
        assert instance.title == "Test Title"
        assert instance.measurements == []
        assert instance.averages_correlation == []

        # Test with partial data - only some fields
        partial_data = {
            "title": "Partial Data"
            # measurements and averages_correlation will be None
        }
        instance_partial = model_class(**partial_data)
        assert instance_partial is not None
        assert instance_partial.title == "Partial Data"
        assert instance_partial.measurements is None
        assert instance_partial.averages_correlation is None

        # Test with completely empty data
        empty_data = {}
        instance_empty = model_class(**empty_data)
        assert instance_empty is not None
        assert instance_empty.title is None
        assert instance_empty.measurements is None
        assert instance_empty.averages_correlation is None

    def test_empty_lists_handling(self, template_data):
        """Test handling of empty lists"""
        empty_list_data = {
            "title": "Empty Lists Test",
            "measurements": [],
            "averages_correlation": [],
        }

        models = DynamicConversor.from_json(template_data)
        model_class = models["main"]
        instance = model_class(**empty_list_data)

        assert instance.measurements == []
        assert instance.averages_correlation == []

    def test_missing_nested_fields(self, template_data):
        """Test with missing nested fields in real data"""
        incomplete_data = {
            "title": "Incomplete Data",
            "measurements": [
                {
                    "name": "Test",
                    # Missing 'inputs' and 'average' fields
                }
            ],
        }

        models = DynamicConversor.from_json(template_data)
        model_class = models["main"]

        # Should handle missing optional fields gracefully
        instance = model_class(**incomplete_data)
        assert instance.measurements[0].name == "Test"
        assert instance.measurements[0].inputs is None
        assert instance.measurements[0].average is None

    def test_model_reusability(self, template_data, real_data):
        """Test that created models can be reused multiple times"""
        models = DynamicConversor.from_json(template_data)
        model_class = models["main"]

        # Create multiple instances
        instance1 = DynamicConversor.create_instance(model_class, real_data)
        instance2 = DynamicConversor.create_instance(model_class, real_data)

        assert instance1.title == instance2.title
        assert len(instance1.measurements) == len(instance2.measurements)

    def test_field_optionality(self, template_data):
        """Test that all fields are properly marked as optional"""
        models = DynamicConversor.from_json(template_data)
        model_class = models["main"]

        # Check that fields are optional (Pydantic v2 way)
        for field_name, field_info in model_class.model_fields.items():
            # In Pydantic v2, we check if the field is not required
            assert (
                not field_info.is_required()
            ), f"Field {field_name} should be optional"


# Tests adicionales para casos edge
class TestDynamicConversorEdgeCases:
    """Test edge cases and error conditions"""

    @pytest.fixture
    def template_data(self):
        """Fixture with the example template data"""
        return {
            "title": "sin(2β) ≡ sin(2φ1)",
            "measurements": [
                {
                    "name": "J/ψKS (ηCP=-1)",
                    "inputs": [
                        {
                            "name": "BaBar",
                            "value": {
                                "central": 0.657,
                                "statistical": 0.036,
                                "systematic": 0.012,
                                "unit": "rad",
                            },
                            "comment": "N(BB)=465M",
                            "References": [
                                {
                                    "arxiv": "0902.1708",
                                    "publication": "PRD 79 (2009) 072009",
                                    "doi": "10.1103/PhysRevD.79.072009",
                                }
                            ],
                        }
                    ],
                    "average": {
                        "value": {
                            "central": 0.695,
                            "uncertainty": 0.019,
                            "unit": "rad",
                        },
                        "comment": "0.018 stat-only",
                    },
                }
            ],
            "averages_correlation": [[0.99, 0.01], [0.01, 0.99]],
        }

    @pytest.fixture
    def real_data(self):
        """Fixture with the real data example"""
        return {
            "title": "HFLAV Tau averages, lifetime",
            "measurements": [
                {
                    "name": "tau lifetime [fs]",
                    "vname": "tau_life",
                    "inputs": [
                        {
                            "name": "ALEPH",
                            "vname": "tau_life_ALEPH_pub_BARATE_1997R",
                            "value": {
                                "central": 290.1,
                                "statistical": 1.5,
                                "systematic": 1.1,
                            },
                            "References": [
                                {
                                    "bibtex": "ALEPH:1997roz",
                                    "publication": "Phys. Lett. B 414 (1997) 362--372",
                                    "doi": "10.1016/S0370-2693(97)01116-7",
                                    "arxiv": "hep-ex/9710026",
                                }
                            ],
                        }
                    ],
                    "average": {
                        "value": {
                            "central": 290.290848172575,
                            "uncertainty": 0.525213667384673,
                        }
                    },
                }
            ],
            "averages_correlation": [[1]],
        }

    def test_invalid_json_string(self):
        """Test with invalid JSON string"""
        invalid_json = "this is not json"

        with pytest.raises(Exception):
            DynamicConversor.from_json(invalid_json)

    def test_nonexistent_file(self):
        """Test with non-existent file path"""
        with pytest.raises(Exception):
            DynamicConversor.from_json("/nonexistent/path/file.json")

    def test_none_data(self):
        """Test with None data"""
        with pytest.raises(Exception):
            DynamicConversor.from_json(None)

    def test_empty_dict(self):
        """Test with empty dictionary"""
        models = DynamicConversor.from_json({})
        assert "main" in models
        model_class = models["main"]
        instance = model_class()
        assert isinstance(instance, BaseModel)

    def test_very_deep_nesting(self):
        """Test with very deeply nested data"""
        deep_data = {"level1": {"level2": {"level3": {"level4": {"value": "deep"}}}}}

        models = DynamicConversor.from_json(deep_data)
        model_class = models["main"]
        instance = DynamicConversor.create_instance(model_class, deep_data)

        assert instance.level1.level2.level3.level4.value == "deep"

    def test_create_instance_with_invalid_file(self, template_data):
        """Test create_instance with non-existent file"""
        models = DynamicConversor.from_json(template_data)
        model_class = models["main"]

        with pytest.raises(Exception):
            DynamicConversor.create_instance(model_class, "/nonexistent/file.json")

    def test_simple_types_creation(self):
        """Test with simple data types"""
        simple_data = {
            "string_field": "test",
            "int_field": 123,
            "float_field": 45.67,
            "bool_field": True,
            "list_field": [1, 2, 3],
            "none_field": None,
        }

        models = DynamicConversor.from_json(simple_data)
        model_class = models["main"]
        instance = model_class(**simple_data)

        assert instance.string_field == "test"
        assert instance.int_field == 123
        assert instance.float_field == 45.67
        assert instance.bool_field is True
        assert instance.list_field == [1, 2, 3]
