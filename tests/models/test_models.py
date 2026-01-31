import pytest
from datetime import datetime
from typing import Dict, Any, ClassVar, List
from unittest.mock import Mock, patch

from hflav_fair_client.models.models import ZenodoElement, File, Record, Template


class TestZenodoElementInterface:
    """Test suite for ZenodoElement base class interface."""

    def test_zenodo_element_is_abstract(self):
        """Test that ZenodoElement cannot be instantiated directly."""
        # ZenodoElement has abstract methods, should raise TypeError
        with pytest.raises(TypeError):
            element = ZenodoElement()

    def test_zenodo_element_abstract_methods(self):
        """Test that ZenodoElement defines required abstract methods."""
        # Check abstract methods exist
        assert hasattr(ZenodoElement, "get_data")
        assert hasattr(ZenodoElement, "name")


class TestFileClass:
    """Test suite for File class public interface."""

    def test_file_implements_zenodo_element(self):
        """Test that File correctly implements ZenodoElement."""
        # Use model_validate to create File instance
        file_data = {
            "key": "test.txt",
            "links": {"self": "http://example.com/test.txt"},
        }
        file = File.model_validate(file_data)
        assert isinstance(file, ZenodoElement)

    def test_file_name_property(self):
        """Test that name property returns title."""
        file_data = {
            "key": "document.pdf",
            "links": {"self": "http://example.com/doc.pdf"},
        }
        file = File.model_validate(file_data)
        assert file.name == "document.pdf"

        # Test with different title
        file_data2 = {
            "key": "image.jpg",
            "links": {"self": "http://example.com/image.jpg"},
        }
        file2 = File.model_validate(file_data2)
        assert file2.name == "image.jpg"

    def test_file_get_data_method(self):
        """Test get_data returns correct dictionary."""
        file_data = {
            "key": "data.json",
            "links": {"self": "http://example.com/data.json"},
        }
        file = File.model_validate(file_data)

        data = file.get_data()

        assert isinstance(data, dict)
        assert data["name"] == "data.json"
        assert data["download_url"] == "http://example.com/data.json"
        assert len(data) == 2

    def test_file_is_leaf(self):
        """Test that File is a leaf node."""
        file_data = {
            "key": "test.txt",
            "links": {"self": "http://example.com/test.txt"},
        }
        file = File.model_validate(file_data)
        assert file.is_leaf == True

    def test_file_str_representation(self):
        """Test string representation of File."""
        file_data = {
            "key": "report.pdf",
            "links": {"self": "http://example.com/report.pdf"},
        }
        file = File.model_validate(file_data)

        str_repr = str(file)
        assert "File(name='report.pdf'" in str_repr
        assert "download_url='http://example.com/report.pdf')" in str_repr

    def test_file_model_validator_transform(self):
        """Test the model_validator transforms JSON data correctly."""
        # Test with minimal valid JSON data
        json_data = {
            "key": "filename.txt",
            "links": {"self": "https://zenodo.org/api/files/filename.txt"},
        }

        file = File.model_validate(json_data)

        assert file.title == "filename.txt"
        assert file.download_url == "https://zenodo.org/api/files/filename.txt"

    def test_file_model_validator_empty_data(self):
        """Test model_validator with empty or incomplete data."""
        # Test with empty dict
        json_data = {}
        file = File.model_validate(json_data)

        assert file.title == ""
        assert file.download_url == ""


class TestRecordClass:
    """Test suite for Record class public interface."""

    def test_record_implements_zenodo_element(self):
        """Test that Record correctly implements ZenodoElement."""
        record_data = {
            "id": 123,
            "doi": "10.1234/zenodo.123",
            "created": "2023-01-01T12:00:00",
            "updated": "2023-01-02T12:00:00",
            "links": {"self": "http://example.com/123"},
            "metadata": {"title": "Test Record"},
            "files": [],
        }
        record = Record.model_validate(record_data)
        assert isinstance(record, ZenodoElement)

    def test_record_name_property(self):
        """Test that name property returns title."""
        record_data = {
            "id": 456,
            "doi": "10.1234/zenodo.456",
            "created": "2023-01-01T12:00:00",
            "updated": "2023-01-02T12:00:00",
            "links": {},
            "metadata": {"title": "Research Data"},
            "files": [],
        }
        record = Record.model_validate(record_data)
        assert record.name == "Research Data"

    def test_record_is_not_leaf(self):
        """Test that Record is not a leaf node (has children)."""
        record_data = {
            "id": 123,
            "doi": "10.1234/zenodo.123",
            "created": "2023-01-01T12:00:00",
            "updated": "2023-01-02T12:00:00",
            "links": {},
            "metadata": {"title": "Test"},
            "files": [],
        }
        record = Record.model_validate(record_data)
        assert record.is_leaf == False

    def test_record_get_data_method(self):
        """Test get_data returns complete record information."""
        record_data = {
            "id": 789,
            "doi": "10.1234/zenodo.789",
            "created": "2023-01-01T12:00:00",
            "updated": "2023-01-02T12:00:00",
            "links": {"download": "http://example.com/download"},
            "metadata": {"title": "Test Dataset"},
            "files": [],
        }

        record = Record.model_validate(record_data)
        data = record.get_data()

        assert isinstance(data, dict)
        assert data["id"] == 789
        assert data["doi"] == "10.1234/zenodo.789"
        assert data["title"] == "Test Dataset"
        assert isinstance(data["created"], datetime)
        assert isinstance(data["updated"], datetime)
        assert data["links"] == {"download": "http://example.com/download"}
        assert data["children"] == []

    def test_record_get_data_with_children(self):
        """Test get_data includes children data."""
        record_data = {
            "id": 100,
            "doi": "10.1234/zenodo.100",
            "created": "2023-01-01T12:00:00",
            "updated": "2023-01-02T12:00:00",
            "links": {},
            "metadata": {"title": "Parent Record"},
            "files": [
                {"key": "file1.txt", "links": {"self": "http://example.com/file1.txt"}},
                {"key": "file2.txt", "links": {"self": "http://example.com/file2.txt"}},
            ],
        }

        record = Record.model_validate(record_data)
        data = record.get_data()

        assert len(data["children"]) == 2
        assert data["children"][0]["name"] == "file1.txt"
        assert data["children"][1]["name"] == "file2.txt"

    def test_record_add_child_method(self):
        """Test add_child adds a child to the record."""
        record_data = {
            "id": 200,
            "doi": "10.1234/zenodo.200",
            "created": "2023-01-01T12:00:00",
            "updated": "2023-01-02T12:00:00",
            "links": {},
            "metadata": {"title": "Empty Record"},
            "files": [],
        }
        record = Record.model_validate(record_data)

        # Create a File using model_validate
        file_data = {
            "key": "new_file.txt",
            "links": {"self": "http://example.com/new.txt"},
        }
        file = File.model_validate(file_data)

        record.add_child(file)

        assert len(record.children) == 1
        assert record.children[0].name == "new_file.txt"

    def test_record_remove_child_method(self):
        """Test remove_child removes child by name."""
        record_data = {
            "id": 400,
            "doi": "10.1234/zenodo.400",
            "created": "2023-01-01T12:00:00",
            "updated": "2023-01-02T12:00:00",
            "links": {},
            "metadata": {"title": "Record with Multiple Children"},
            "files": [
                {"key": "file1.txt", "links": {"self": "http://example.com/file1.txt"}},
                {"key": "file2.txt", "links": {"self": "http://example.com/file2.txt"}},
                {"key": "file3.txt", "links": {"self": "http://example.com/file3.txt"}},
            ],
        }
        record = Record.model_validate(record_data)

        record.remove_child("file2.txt")

        assert len(record.children) == 2
        assert record.children[0].name == "file1.txt"
        assert record.children[1].name == "file3.txt"

    def test_record_get_child_method(self):
        """Test get_child retrieves child by name."""
        record_data = {
            "id": 600,
            "doi": "10.1234/zenodo.600",
            "created": "2023-01-01T12:00:00",
            "updated": "2023-01-02T12:00:00",
            "links": {},
            "metadata": {"title": "Record"},
            "files": [
                {"key": "file1.txt", "links": {"self": "http://example.com/file1.txt"}},
                {"key": "file2.txt", "links": {"self": "http://example.com/file2.txt"}},
            ],
        }
        record = Record.model_validate(record_data)

        child = record.get_child("file2.txt")
        assert child.name == "file2.txt"
        assert child.download_url == "http://example.com/file2.txt"

    def test_record_str_representation(self):
        """Test string representation of Record."""
        record_data = {
            "id": 999,
            "doi": "10.1234/zenodo.999",
            "created": "2023-01-01T12:00:00",
            "updated": "2023-01-02T12:00:00",
            "links": {},
            "metadata": {"title": "Test Dataset"},
            "files": [
                {"key": "data.csv", "links": {"self": "http://example.com/data.csv"}},
                {
                    "key": "readme.txt",
                    "links": {"self": "http://example.com/readme.txt"},
                },
            ],
        }

        record = Record.model_validate(record_data)
        str_repr = str(record)

        assert "Record(" in str_repr
        assert "id=999" in str_repr
        assert "title='Test Dataset'" in str_repr
        assert "doi='10.1234/zenodo.999'" in str_repr
        assert "File(name='data.csv'" in str_repr
        assert "File(name='readme.txt'" in str_repr

    def test_record_model_validator_transform(self):
        """Test the model_validator transforms JSON data correctly."""
        json_data = {
            "id": 12345,
            "doi": "10.5281/zenodo.12345",
            "created": "2023-01-01T12:00:00",
            "updated": "2023-01-02T12:00:00",
            "links": {
                "self": "https://zenodo.org/api/records/12345",
                "html": "https://zenodo.org/record/12345",
            },
            "metadata": {"title": "Test Record Title"},
            "files": [
                {
                    "key": "file1.pdf",
                    "links": {"self": "https://zenodo.org/api/files/file1.pdf"},
                },
                {
                    "key": "file2.csv",
                    "links": {"self": "https://zenodo.org/api/files/file2.csv"},
                },
            ],
        }

        record = Record.model_validate(json_data)

        assert record.id == 12345
        assert record.doi == "10.5281/zenodo.12345"
        assert record.title == "Test Record Title"
        assert isinstance(record.created, datetime)
        assert isinstance(record.updated, datetime)
        assert record.links == {
            "self": "https://zenodo.org/api/records/12345",
            "html": "https://zenodo.org/record/12345",
        }
        assert len(record.children) == 2
        assert record.children[0].name == "file1.pdf"
        assert record.children[1].name == "file2.csv"


class TestTemplateClass:
    """Test suite for Template class public interface."""

    def test_template_implements_zenodo_element(self):
        """Test that Template correctly implements ZenodoElement."""
        template_data = {
            "id": 1001,
            "created": "2023-01-01T12:00:00",
            "updated": "2023-01-02T12:00:00",
            "metadata": {"title": "Test Template", "version": "1.0.0"},
            "files": [],
        }
        template = Template.model_validate(template_data)
        assert isinstance(template, ZenodoElement)

    def test_template_name_property(self):
        """Test that name property returns title."""
        template_data = {
            "id": 1002,
            "created": "2023-01-01T12:00:00",
            "updated": "2023-01-02T12:00:00",
            "metadata": {"title": "Data Template", "version": "2.0.0"},
            "files": [],
        }
        template = Template.model_validate(template_data)
        assert template.name == "Data Template"

    def test_template_is_leaf(self):
        """Test that Template is a leaf node."""
        template_data = {
            "id": 1003,
            "created": "2023-01-01T12:00:00",
            "updated": "2023-01-02T12:00:00",
            "metadata": {"title": "Template", "version": "1.0.0"},
            "files": [],
        }
        template = Template.model_validate(template_data)
        # Template doesn't have children attribute, so it should be a leaf
        assert template.is_leaf == True

    def test_template_get_data_method(self):
        """Test get_data returns template information."""
        template_data = {
            "id": 1004,
            "created": "2023-01-01T12:00:00",
            "updated": "2023-01-02T12:00:00",
            "metadata": {"title": "JSON Template", "version": "1.0.0"},
            "files": [
                {
                    "key": "template.json",
                    "links": {"self": "http://example.com/template.json"},
                }
            ],
        }

        template = Template.model_validate(template_data)
        data = template.get_data()

        assert isinstance(data, dict)
        assert data["rec_id"] == 1004
        assert data["title"] == "JSON Template"
        assert isinstance(data["created"], datetime)
        assert isinstance(data["updated"], datetime)
        assert data["version"] == "1.0.0"

    def test_template_model_validator_transform_with_files(self):
        """Test model_validator finds JSON and schema files."""
        json_data = {
            "id": 2000,
            "created": "2023-01-01T12:00:00",
            "updated": "2023-01-02T12:00:00",
            "metadata": {"title": "Data Template", "version": "1.0.0"},
            "files": [
                {
                    "key": "data.json",
                    "links": {"self": "https://zenodo.org/api/files/data.json"},
                },
                {
                    "key": "schema.schema",
                    "links": {"self": "https://zenodo.org/api/files/schema.schema"},
                },
                {
                    "key": "readme.txt",
                    "links": {"self": "https://zenodo.org/api/files/readme.txt"},
                },
            ],
        }

        template = Template.model_validate(json_data)

        assert template.rec_id == 2000
        assert template.title == "Data Template"
        assert template.version == "1.0.0"
        assert isinstance(template.created, datetime)
        assert isinstance(template.updated, datetime)

        # Should have found the JSON file
        assert template.jsontemplate is not None
        assert template.jsontemplate.name == "data.json"

        # Should have found the schema file
        assert template.jsonschema is not None
        assert template.jsonschema.name == "schema.schema"

    def test_template_model_validator_transform_no_matching_files(self):
        """Test model_validator when no JSON or schema files exist."""
        json_data = {
            "id": 2001,
            "created": "2023-01-01T12:00:00",
            "updated": "2023-01-02T12:00:00",
            "metadata": {"title": "Template without JSON", "version": "1.0.0"},
            "files": [
                {
                    "key": "readme.txt",
                    "links": {"self": "https://zenodo.org/api/files/readme.txt"},
                },
                {
                    "key": "data.txt",
                    "links": {"self": "https://zenodo.org/api/files/data.txt"},
                },
            ],
        }

        template = Template.model_validate(json_data)

        assert template.rec_id == 2001
        assert template.title == "Template without JSON"

        # Should not find JSON or schema files
        assert template.jsontemplate is None
        assert template.jsonschema is None


class TestInteroperability:
    """Test interoperability between different ZenodoElement types."""

    def test_record_can_contain_files(self):
        """Test that Record can contain File instances as children."""
        record_data = {
            "id": 4000,
            "doi": "10.5281/zenodo.4000",
            "created": "2023-01-01T12:00:00",
            "updated": "2023-01-02T12:00:00",
            "links": {},
            "metadata": {"title": "Research Package"},
            "files": [
                {
                    "key": "document.pdf",
                    "links": {"self": "http://example.com/doc.pdf"},
                },
                {"key": "data.csv", "links": {"self": "http://example.com/data.csv"}},
            ],
        }
        record = Record.model_validate(record_data)

        assert len(record.children) == 2
        assert isinstance(record.children[0], File)
        assert isinstance(record.children[1], File)
        assert isinstance(record.children[0], ZenodoElement)

    def test_template_contains_files(self):
        """Test that Template can contain File instances."""
        template_data = {
            "id": 4001,
            "created": "2023-01-01T12:00:00",
            "updated": "2023-01-02T12:00:00",
            "metadata": {"title": "JSON Template", "version": "1.0.0"},
            "files": [
                {
                    "key": "template.json",
                    "links": {"self": "http://example.com/template.json"},
                }
            ],
        }
        template = Template.model_validate(template_data)

        assert isinstance(template.jsontemplate, File)
        assert isinstance(template.jsontemplate, ZenodoElement)

    def test_composite_structure_get_data(self):
        """Test get_data works through a composite structure."""
        # Create a nested structure
        record_data = {
            "id": 5000,
            "doi": "10.5281/zenodo.5000",
            "created": "2023-01-01T12:00:00",
            "updated": "2023-01-02T12:00:00",
            "links": {},
            "metadata": {"title": "Parent Record"},
            "files": [
                {
                    "key": "inner1.txt",
                    "links": {"self": "http://example.com/inner1.txt"},
                },
                {
                    "key": "inner2.txt",
                    "links": {"self": "http://example.com/inner2.txt"},
                },
            ],
        }

        record = Record.model_validate(record_data)

        # Get data from record (should include children data)
        record_data = record.get_data()

        assert record_data["id"] == 5000
        assert len(record_data["children"]) == 2
        assert record_data["children"][0]["name"] == "inner1.txt"
        assert record_data["children"][1]["name"] == "inner2.txt"


class TestEdgeCases:
    """Test edge cases and less common scenarios."""

    def test_record_add_child_when_children_is_none(self):
        """Test add_child initializes children list if None."""
        record_data = {
            "id": 1,
            "doi": "10.1234/test",
            "created": "2023-01-01T12:00:00",
            "updated": "2023-01-02T12:00:00",
            "links": {},
            "metadata": {"title": "Test"},
            "files": [],
        }
        record = Record.model_validate(record_data)
        # Manually set children to None to test the condition
        record.children = None
        file_data = {
            "key": "test.txt",
            "links": {"self": "http://example.com/test.txt"},
        }
        file = File.model_validate(file_data)
        record.add_child(file)
        assert len(record.children) == 1

    def test_record_remove_child_with_empty_children(self):
        """Test remove_child does nothing when children is empty."""
        record_data = {
            "id": 1,
            "doi": "10.1234/test",
            "created": "2023-01-01T12:00:00",
            "updated": "2023-01-02T12:00:00",
            "links": {},
            "metadata": {"title": "Test"},
            "files": [],
        }
        record = Record.model_validate(record_data)
        # Should not raise error
        record.remove_child("nonexistent.txt")
        assert len(record.children) == 0

    def test_record_get_child_raises_error_when_no_children(self):
        """Test get_child raises ValueError when record has no children."""
        record_data = {
            "id": 1,
            "doi": "10.1234/test",
            "created": "2023-01-01T12:00:00",
            "updated": "2023-01-02T12:00:00",
            "links": {},
            "metadata": {"title": "Test"},
            "files": [],
        }
        record = Record.model_validate(record_data)
        with pytest.raises(ValueError, match="No children in record"):
            record.get_child("test.txt")

    def test_record_get_child_raises_error_when_child_not_found(self):
        """Test get_child raises ValueError when child not found."""
        record_data = {
            "id": 1,
            "doi": "10.1234/test",
            "created": "2023-01-01T12:00:00",
            "updated": "2023-01-02T12:00:00",
            "links": {},
            "metadata": {"title": "Test"},
            "files": [
                {"key": "file1.txt", "links": {"self": "http://example.com/file1.txt"}},
            ],
        }
        record = Record.model_validate(record_data)
        with pytest.raises(
            ValueError, match="Child with name nonexistent.txt not found"
        ):
            record.get_child("nonexistent.txt")

    def test_file_model_validator_non_dict_input(self):
        """Test File model_validator when input is not a dict."""
        # When passing a non-dict object, the validator should return it as-is
        non_dict_input = "not a dict"
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            file = File.model_validate(non_dict_input)

    def test_record_model_validator_non_dict_input(self):
        """Test Record model_validator when input is not a dict."""
        # When passing a non-dict object, the validator should return it as-is
        non_dict_input = "not a dict"
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            record = Record.model_validate(non_dict_input)

    def test_template_model_validator_non_dict_input(self):
        """Test Template model_validator when input is not a dict."""
        # When passing a non-dict object, the validator should return it as-is
        non_dict_input = "not a dict"
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            template = Template.model_validate(non_dict_input)
