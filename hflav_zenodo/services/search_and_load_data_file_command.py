from hflav_zenodo.logger import get_logger
from hflav_zenodo.services.command import Command
from dependency_injector.wiring import inject, Provide

from hflav_zenodo.services.service_interface import ServiceInterface

logger = get_logger(__name__)


class SearchAndLoadDataFile(Command):
    @inject
    def __init__(
        self,
        service: ServiceInterface = Provide["service"],
        query: str = None,
        size: int = 10,
        page: int = 1,
    ):
        self._service = service
        self._query = query
        self._size = size
        self._page = page

    def execute(self):
        selected_record = 0
        selected_file = 0
        while selected_record == 0:
            records = self._service.search_records_by_name(
                query=self._query, size=self._size, page=self._page
            )
            logger.info("Select a record by number (or 0 to search again):")
            try:
                selected_record = int(input())
            except ValueError:
                logger.info("Invalid input. Please enter a number.")
                continue
            if selected_record == 0:
                logger.info("Please enter a new search query:")
                self._query = input()
            else:
                record = records[selected_record - 1]
                logger.info(f"Selected record: {record.title}")
                logger.info("Select a file by number:")
                try:
                    selected_file = int(input())
                except ValueError:
                    logger.info("Invalid input. Please enter a number.")
                    selected_record = 0
                    continue
                filename = record.children[selected_file - 1].name
                logger.info(f"Selected file: {filename}")
                return self._service.load_data_file(
                    record_id=record.id, filename=filename
                )

    def undo(self):
        logger.info("Undo operation is not supported for loading data files.")
