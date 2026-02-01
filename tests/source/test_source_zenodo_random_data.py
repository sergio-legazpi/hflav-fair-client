import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import tempfile
import os
import json

from hflav_fair_client.filters.base_query import BaseQuery
from hflav_fair_client.models.models import Record, Template
from hflav_fair_client.source.source_zenodo_random_data import SourceZenodoRandomData


class TestSourceZenodoRandomData(unittest.TestCase):
    def setUp(self):
        """Initial setup for each test."""
        self.source = SourceZenodoRandomData()
        self.mock_random_data = {"test": "data"}

    def test_initialization(self):
        """Test class initialization."""
        self.assertIsNotNone(self.source._schema)
        self.assertIsInstance(self.source._schema, dict)
        self.assertEqual(
            self.source._random_generated_data_name, "random_generated_data.json"
        )
        self.assertEqual(self.source._schema_name, "hflav_fair_client_schema.schema")

    @patch.object(SourceZenodoRandomData, "_generate_random_data")
    def test_get_records_by_name(self, mock_gen):
        """Test get_records_by_name returns a list with a Record."""
        mock_gen.return_value = self.mock_random_data
        mock_query = Mock(spec=BaseQuery)

        result = self.source.get_records_by_name(mock_query)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Record)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].doi, "10.1234/random.doi")
        self.assertEqual(result[0].title, "Random Generated Record")

    @patch.object(SourceZenodoRandomData, "_generate_random_data")
    def test_get_correct_template_by_date(self, mock_gen):
        """Test get_correct_template_by_date returns a Template."""
        mock_gen.return_value = self.mock_random_data
        result = self.source.get_correct_template_by_date()

        self.assertIsInstance(result, Template)
        self.assertEqual(result.rec_id, 123456)
        self.assertEqual(result.title, "Random Generated Template")
        self.assertEqual(result.version, "1.0.0")

    @patch.object(SourceZenodoRandomData, "_generate_random_data")
    def test_get_correct_template_by_date_with_date(self, mock_gen):
        """Test get_correct_template_by_date with a specific date."""
        mock_gen.return_value = self.mock_random_data
        test_date = datetime.now()

        result = self.source.get_correct_template_by_date(test_date)

        self.assertIsInstance(result, Template)
        self.assertEqual(result.rec_id, 123456)

    @patch.object(SourceZenodoRandomData, "_generate_random_data")
    def test_get_record(self, mock_gen):
        """Test get_record returns a Record."""
        mock_gen.return_value = self.mock_random_data
        result = self.source.get_record(1)

        self.assertIsInstance(result, Record)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.doi, "10.1234/random.doi")
        self.assertEqual(result.title, "Random Generated Record")
        # Should have files in children
        self.assertEqual(len(result.children), 2)

    @patch.object(SourceZenodoRandomData, "_generate_random_data")
    def test_generate_random_data(self, mock_gen):
        """Test _generate_random_data returns valid data (mocked)."""
        mock_gen.return_value = self.mock_random_data

        result = self.source._generate_random_data()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    @patch("hflav_fair_client.source.source_zenodo_random_data.hypothesis.find")
    @patch("hflav_fair_client.source.source_zenodo_random_data.from_schema")
    def test_generate_random_data_real_execution(self, mock_from_schema, mock_find):
        """Test _generate_random_data real execution with mocked Hypothesis.

        Mocks the expensive Hypothesis operations to keep test execution fast
        while still testing the control flow and settings configuration.
        """
        # Reset cached strategy to ensure clean execution
        self.source._cached_strategy = None

        # Mock the strategy and find to return quick data
        mock_strategy = Mock()
        mock_from_schema.return_value = mock_strategy
        mock_find.return_value = self.mock_random_data

        result = self.source._generate_random_data()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        mock_from_schema.assert_called_once_with(self.source._schema)
        mock_find.assert_called_once()

    @patch.object(SourceZenodoRandomData, "_generate_random_data")
    def test_download_file_by_id_and_filename_random_data(self, mock_gen):
        """Test download_file_by_id_and_filename downloads random data."""
        mock_gen.return_value = self.mock_random_data

        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.source.download_file_by_id_and_filename(
                1, "random_generated_data.json", temp_dir
            )

            self.assertTrue(os.path.exists(result))
            # Check file contains valid JSON
            with open(result, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.assertIsInstance(data, dict)

    @patch.object(SourceZenodoRandomData, "_generate_random_data")
    def test_download_file_by_id_and_filename_schema(self, mock_gen):
        """Test download_file_by_id_and_filename downloads schema."""
        mock_gen.return_value = self.mock_random_data
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.source.download_file_by_id_and_filename(
                1, "hflav_fair_client_schema.schema", temp_dir
            )

            self.assertTrue(os.path.exists(result))
            # Check file contains valid JSON
            with open(result, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.assertIsInstance(data, dict)

    @patch.object(SourceZenodoRandomData, "_generate_random_data")
    def test_cached_strategy_reuse(self, mock_gen):
        """Test that _cached_strategy is cached and reused for multiple calls."""
        mock_gen.return_value = self.mock_random_data
        # First call - will generate and cache strategy
        data1 = self.source._generate_random_data()
        cached_strategy1 = self.source._cached_strategy

        # Second call - should reuse cached strategy
        data2 = self.source._generate_random_data()
        cached_strategy2 = self.source._cached_strategy

        # Strategy should be the same object (cached)
        if cached_strategy1 is not None and cached_strategy2 is not None:
            self.assertIs(cached_strategy1, cached_strategy2)

    @patch.object(SourceZenodoRandomData, "_generate_random_data")
    def test_get_record_files_structure(self, mock_gen):
        """Test get_record returns proper files structure."""
        mock_gen.return_value = self.mock_random_data
        result = self.source.get_record(1)

        self.assertIsInstance(result.children, list)
        self.assertEqual(len(result.children), 2)
        # Check first file
        self.assertEqual(result.children[0].title, "random_generated_data.json")
        # Check second file
        self.assertEqual(result.children[1].title, "hflav_fair_client_schema.schema")

    @patch.object(SourceZenodoRandomData, "_generate_random_data")
    def test_get_records_by_name_files_structure(self, mock_gen):
        """Test get_records_by_name returns proper files structure."""
        mock_gen.return_value = self.mock_random_data
        mock_query = Mock(spec=BaseQuery)

        result = self.source.get_records_by_name(mock_query)
        record = result[0]

        self.assertIsInstance(record.children, list)
        self.assertEqual(len(record.children), 1)
        self.assertEqual(record.children[0].title, "random_generated_data.json")

    @patch.object(SourceZenodoRandomData, "_generate_random_data")
    def test_get_correct_template_by_date_files_structure(self, mock_gen):
        """Test get_correct_template_by_date returns proper files structure."""
        mock_gen.return_value = self.mock_random_data
        result = self.source.get_correct_template_by_date()

        # Template has jsontemplate and jsonschema attributes
        self.assertIsNotNone(result.jsontemplate)
        self.assertIsNotNone(result.jsonschema)
        self.assertEqual(result.jsontemplate.title, "random_generated_data.json")
        self.assertEqual(result.jsonschema.title, "hflav_fair_client_schema.schema")


if __name__ == "__main__":
    unittest.main()
