import pytest
from types import SimpleNamespace

from hflav_fair_client.utils.namespace_utils import dict_to_namespace, namespace_to_dict


class TestNamespaceUtils:
    """Test suite for namespace utility functions."""

    def test_dict_to_namespace_simple_dict(self):
        """Test conversion of simple dictionary to namespace."""
        data = {"key1": "value1", "key2": "value2"}
        result = dict_to_namespace(data)

        assert isinstance(result, SimpleNamespace)
        assert result.key1 == "value1"
        assert result.key2 == "value2"

    def test_dict_to_namespace_nested_dict(self):
        """Test conversion of nested dictionary to namespace."""
        data = {"level1": {"level2": {"key": "value"}}}
        result = dict_to_namespace(data)

        assert isinstance(result, SimpleNamespace)
        assert isinstance(result.level1, SimpleNamespace)
        assert isinstance(result.level1.level2, SimpleNamespace)
        assert result.level1.level2.key == "value"

    def test_dict_to_namespace_with_list(self):
        """Test conversion of dictionary with list to namespace."""
        data = {"items": [{"id": 1, "name": "item1"}, {"id": 2, "name": "item2"}]}
        result = dict_to_namespace(data)

        assert isinstance(result, SimpleNamespace)
        assert isinstance(result.items, list)
        assert len(result.items) == 2
        assert isinstance(result.items[0], SimpleNamespace)
        assert result.items[0].id == 1
        assert result.items[0].name == "item1"

    def test_dict_to_namespace_with_primitive_value(self):
        """Test that primitive values are returned as-is."""
        assert dict_to_namespace("string") == "string"
        assert dict_to_namespace(42) == 42
        assert dict_to_namespace(3.14) == 3.14
        assert dict_to_namespace(True) is True
        assert dict_to_namespace(None) is None

    def test_namespace_to_dict_simple_namespace(self):
        """Test conversion of simple namespace to dictionary."""
        ns = SimpleNamespace(key1="value1", key2="value2")
        result = namespace_to_dict(ns)

        assert isinstance(result, dict)
        assert result == {"key1": "value1", "key2": "value2"}

    def test_namespace_to_dict_nested_namespace(self):
        """Test conversion of nested namespace to dictionary."""
        ns = SimpleNamespace(
            level1=SimpleNamespace(level2=SimpleNamespace(key="value"))
        )
        result = namespace_to_dict(ns)

        assert isinstance(result, dict)
        assert result == {"level1": {"level2": {"key": "value"}}}

    def test_namespace_to_dict_with_list(self):
        """Test conversion of namespace with list to dictionary."""
        ns = SimpleNamespace(
            items=[
                SimpleNamespace(id=1, name="item1"),
                SimpleNamespace(id=2, name="item2"),
            ]
        )
        result = namespace_to_dict(ns)

        assert isinstance(result, dict)
        assert result == {
            "items": [{"id": 1, "name": "item1"}, {"id": 2, "name": "item2"}]
        }

    def test_namespace_to_dict_with_primitive_value(self):
        """Test that primitive values are returned as-is."""
        assert namespace_to_dict("string") == "string"
        assert namespace_to_dict(42) == 42
        assert namespace_to_dict(3.14) == 3.14
        assert namespace_to_dict(True) is True
        assert namespace_to_dict(None) is None

    def test_round_trip_conversion(self):
        """Test that conversion to namespace and back to dict works."""
        original = {"name": "test", "nested": {"value": 123, "items": [1, 2, 3]}}
        ns = dict_to_namespace(original)
        result = namespace_to_dict(ns)

        assert result == original
