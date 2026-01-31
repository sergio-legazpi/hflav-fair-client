import pytest
from types import SimpleNamespace

from hflav_fair_client.models.base_hflav_data_decorator import BaseHflavDataDecorator


class TestBaseHflavDataDecorator:
    """Test suite for BaseHflavDataDecorator class."""

    class ConcreteDecorator(BaseHflavDataDecorator):
        """Concrete implementation of BaseHflavDataDecorator for testing."""

        pass

    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        return SimpleNamespace(
            name="test",
            value=42,
            nested=SimpleNamespace(field1="value1", field2="value2"),
        )

    @pytest.fixture
    def decorator(self, sample_data):
        """Create a concrete decorator instance for testing."""
        return self.ConcreteDecorator(sample_data)

    def test_initialization(self, decorator, sample_data):
        """Test BaseHflavDataDecorator initialization."""
        assert decorator._hflav_data == sample_data

    def test_get_data_as_namespace(self, decorator, sample_data):
        """Test get_data_as_namespace returns the data."""
        result = decorator.get_data_as_namespace()
        assert result == sample_data
        assert isinstance(result, SimpleNamespace)

    def test_getattr_delegates_to_hflav_data(self, decorator):
        """Test __getattr__ delegates attribute access to _hflav_data."""
        # Access attributes through the decorator
        assert decorator.name == "test"
        assert decorator.value == 42
        assert decorator.nested.field1 == "value1"
        assert decorator.nested.field2 == "value2"

    def test_getattr_raises_attribute_error_for_nonexistent(self, decorator):
        """Test __getattr__ raises AttributeError for nonexistent attributes."""
        with pytest.raises(AttributeError):
            _ = decorator.nonexistent_attribute

    def test_base_class_is_abstract(self):
        """Test that BaseHflavDataDecorator is an abstract base class."""
        # Verify it's an ABC
        from abc import ABC

        assert issubclass(BaseHflavDataDecorator, ABC)
