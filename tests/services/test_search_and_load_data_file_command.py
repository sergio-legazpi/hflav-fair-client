import pytest
from unittest.mock import Mock, patch, MagicMock
from hflav_fair_client.services.search_and_load_data_file_command import (
    SearchAndLoadDataFile,
)
from hflav_fair_client.filters.base_query import BaseQuery
from hflav_fair_client.services.service_interface import ServiceInterface
from hflav_fair_client.models.models import Record, File


class TestSearchAndLoadDataFileCommand:
    """Test suite for SearchAndLoadDataFile command."""

    def test_command_initialization(self):
        """Test that SearchAndLoadDataFile initializes correctly."""
        mock_query = Mock(spec=BaseQuery)
        mock_service = Mock(spec=ServiceInterface)

        command = SearchAndLoadDataFile(query=mock_query, service=mock_service)

        assert command._query == mock_query
        assert command._service == mock_service

    def test_execute_user_selects_zero_exits_immediately(self):
        """Test execute when user selects 0 to exit."""
        mock_query = Mock(spec=BaseQuery)
        mock_service = Mock(spec=ServiceInterface)
        mock_records = [Mock(spec=Record)]
        mock_service.search_records_by_name.return_value = mock_records

        command = SearchAndLoadDataFile(query=mock_query, service=mock_service)

        with patch("builtins.input", return_value="0"):
            result = command.execute()

        assert result is None
        mock_service.search_records_by_name.assert_called_once_with(query=mock_query)

    def test_execute_invalid_record_selection_input(self):
        """Test execute when user provides invalid record selection input."""
        mock_query = Mock(spec=BaseQuery)
        mock_service = Mock(spec=ServiceInterface)
        mock_records = [Mock(spec=Record)]
        mock_service.search_records_by_name.return_value = mock_records

        command = SearchAndLoadDataFile(query=mock_query, service=mock_service)

        # First input is invalid (not a number), second is 0 to exit
        with patch("builtins.input", side_effect=["invalid", "0"]):
            with patch(
                "hflav_fair_client.services.search_and_load_data_file_command.logger"
            ):
                result = command.execute()

        assert result is None

    def test_execute_valid_record_invalid_file_selection(self):
        """Test execute with valid record selection but invalid file selection."""
        mock_query = Mock(spec=BaseQuery)
        mock_service = Mock(spec=ServiceInterface)

        # Create mock record with children
        mock_record = Mock(spec=Record)
        mock_record.id = 1
        mock_record.title = "Test Record"
        mock_file = Mock(spec=File)
        mock_file.name = "test.txt"
        mock_record.children = [mock_file]

        mock_service.search_records_by_name.return_value = [mock_record]

        command = SearchAndLoadDataFile(query=mock_query, service=mock_service)

        # First input is record selection (1), second is invalid file selection, third is 0 to exit
        with patch("builtins.input", side_effect=["1", "invalid", "0"]):
            with patch(
                "hflav_fair_client.services.search_and_load_data_file_command.logger"
            ):
                result = command.execute()

        assert result is None

    def test_execute_valid_record_and_file_selection(self):
        """Test execute with valid record and file selection."""
        mock_query = Mock(spec=BaseQuery)
        mock_service = Mock(spec=ServiceInterface)

        # Create mock record with children
        mock_record = Mock(spec=Record)
        mock_record.id = 1
        mock_record.title = "Test Record"
        mock_file = Mock(spec=File)
        mock_file.name = "test.txt"
        mock_record.children = [mock_file]

        mock_service.search_records_by_name.return_value = [mock_record]
        mock_service.load_data_file.return_value = {"data": "loaded"}

        command = SearchAndLoadDataFile(query=mock_query, service=mock_service)

        # Input: select record 1, select file 1
        with patch("builtins.input", side_effect=["1", "1"]):
            with patch(
                "hflav_fair_client.services.search_and_load_data_file_command.logger"
            ):
                result = command.execute()

        mock_service.load_data_file.assert_called_once_with(
            record_id=1, filename="test.txt"
        )
        assert result == {"data": "loaded"}

    def test_undo_operation(self):
        """Test undo operation logs appropriate message."""
        mock_query = Mock(spec=BaseQuery)
        mock_service = Mock(spec=ServiceInterface)

        command = SearchAndLoadDataFile(query=mock_query, service=mock_service)

        with patch(
            "hflav_fair_client.services.search_and_load_data_file_command.logger"
        ) as mock_logger:
            command.undo()

        mock_logger.info.assert_called_once_with(
            "Undo operation is not supported for loading data files."
        )

    def test_execute_multiple_records_selection(self):
        """Test execute with multiple records and selecting the second one."""
        mock_query = Mock(spec=BaseQuery)
        mock_service = Mock(spec=ServiceInterface)

        # Create mock records
        mock_record1 = Mock(spec=Record)
        mock_record1.id = 1
        mock_record1.title = "First Record"

        mock_record2 = Mock(spec=Record)
        mock_record2.id = 2
        mock_record2.title = "Second Record"

        mock_file = Mock(spec=File)
        mock_file.name = "data.json"
        mock_record2.children = [mock_file]

        mock_service.search_records_by_name.return_value = [mock_record1, mock_record2]
        mock_service.load_data_file.return_value = {"loaded": True}

        command = SearchAndLoadDataFile(query=mock_query, service=mock_service)

        # Select second record (index 1) and first file
        with patch("builtins.input", side_effect=["2", "1"]):
            with patch(
                "hflav_fair_client.services.search_and_load_data_file_command.logger"
            ):
                result = command.execute()

        mock_service.load_data_file.assert_called_once_with(
            record_id=2, filename="data.json"
        )

    def test_execute_search_called_at_start(self):
        """Test that search_records_by_name is called at the start of execute."""
        mock_query = Mock(spec=BaseQuery)
        mock_service = Mock(spec=ServiceInterface)
        mock_service.search_records_by_name.return_value = []

        command = SearchAndLoadDataFile(query=mock_query, service=mock_service)

        with patch("builtins.input", return_value="0"):
            command.execute()

        mock_service.search_records_by_name.assert_called_once_with(query=mock_query)
