import pytest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from hflav_fair_client.models.hflav_data_searching import (
    HflavDataSearching,
    SearchOperators,
)


class TestHflavDataSearching:
    """Test suite for HflavDataSearching class."""

    @pytest.fixture
    def mock_visualizer(self):
        """Create a mock visualizer."""
        visualizer = Mock()
        visualizer.print_json_data = Mock()
        return visualizer

    @pytest.fixture
    def sample_hflav_data(self):
        """Create sample HFLAV data for testing."""
        return SimpleNamespace(
            measurements=[
                SimpleNamespace(name="measurement1", value=10.5, type="typeA"),
                SimpleNamespace(name="measurement2", value=20.3, type="typeB"),
                SimpleNamespace(name="measurement3", value=15.7, type="typeA"),
            ],
            experiments=SimpleNamespace(
                exp1=SimpleNamespace(
                    measurements=[
                        SimpleNamespace(name="exp1_m1", value=5.0, type="typeA"),
                        SimpleNamespace(name="exp1_m2", value=25.0, type="typeC"),
                    ]
                )
            ),
        )

    @pytest.fixture
    def hflav_searching(self, sample_hflav_data, mock_visualizer):
        """Create HflavDataSearching instance with sample data."""
        return HflavDataSearching(sample_hflav_data, visualizer=mock_visualizer)

    def test_initialization(self, hflav_searching, sample_hflav_data, mock_visualizer):
        """Test HflavDataSearching initialization."""
        assert hflav_searching._hflav_data == sample_hflav_data
        assert hflav_searching._visualizer == mock_visualizer

    def test_get_data_object_from_key_and_value_equals(
        self, hflav_searching, mock_visualizer
    ):
        """Test searching with EQUALS operator."""
        results = hflav_searching.get_data_object_from_key_and_value(
            object_name="measurements",
            key_name="type",
            operator=SearchOperators.EQUALS,
            value="typeA",
        )

        # Should find all typeA measurements (including nested ones)
        assert len(results) >= 2
        assert any(r.name == "measurement1" for r in results)
        assert any(r.name == "measurement3" for r in results)
        assert mock_visualizer.print_json_data.call_count == len(results)

    def test_get_data_object_from_key_and_value_greater_than(
        self, hflav_searching, mock_visualizer
    ):
        """Test searching with GREATER_THAN operator."""
        results = hflav_searching.get_data_object_from_key_and_value(
            object_name="measurements",
            key_name="value",
            operator=SearchOperators.GREATER_THAN,
            value=15.0,
        )

        assert len(results) >= 2
        for result in results:
            assert result.value > 15.0
        assert mock_visualizer.print_json_data.call_count == len(results)

    def test_get_data_object_from_key_and_value_less_than(
        self, hflav_searching, mock_visualizer
    ):
        """Test searching with LESS_THAN operator."""
        results = hflav_searching.get_data_object_from_key_and_value(
            object_name="measurements",
            key_name="value",
            operator=SearchOperators.LESS_THAN,
            value=20.0,
        )

        assert len(results) >= 2
        for result in results:
            assert result.value < 20.0

    def test_get_data_object_from_key_and_value_no_results(
        self, hflav_searching, mock_visualizer
    ):
        """Test searching with no matching results."""
        results = hflav_searching.get_data_object_from_key_and_value(
            object_name="measurements",
            key_name="type",
            operator=SearchOperators.EQUALS,
            value="nonexistent_type",
        )

        assert len(results) == 0
        mock_visualizer.print_json_data.assert_not_called()

    def test_get_data_object_from_key_and_value_numeric_value(
        self, hflav_searching, mock_visualizer
    ):
        """Test searching with numeric value."""
        results = hflav_searching.get_data_object_from_key_and_value(
            object_name="measurements",
            key_name="value",
            operator=SearchOperators.EQUALS,
            value=10.5,
        )

        assert len(results) == 1
        assert results[0].value == 10.5

    def test_search_operators_enum_values(self):
        """Test SearchOperators enum values."""
        assert SearchOperators.EQUALS.value == "=="
        assert SearchOperators.NOT_EQUALS.value == "!="
        assert SearchOperators.GREATER_THAN.value == ">"
        assert SearchOperators.LESS_THAN.value == "<"
        assert SearchOperators.GREATER_THAN_OR_EQUALS.value == ">="
        assert SearchOperators.LESS_THAN_OR_EQUALS.value == "<="
        assert SearchOperators.CONTAINS.value == "=~"
        assert SearchOperators.REGEX.value == "=~"

    def test_get_data_object_with_nested_search(self, hflav_searching, mock_visualizer):
        """Test searching in nested structures."""
        results = hflav_searching.get_data_object_from_key_and_value(
            object_name="measurements",
            key_name="name",
            operator=SearchOperators.EQUALS,
            value="exp1_m1",
        )

        assert len(results) >= 1
        found = any(r.name == "exp1_m1" for r in results)
        assert found
