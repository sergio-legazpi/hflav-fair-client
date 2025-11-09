from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class SourceInterface(ABC):
    """Abstract interface for source clients used by HFLAV.

    This defines the public contract implemented by `ZenodoClient` in
    `source_zenodo.py`. Implementations must provide the methods below and
    follow the documented input/output shapes (they generally return JSON-like
    dicts or file paths).
    """

    @abstractmethod
    def get_files_by_name(
        self, query: Optional[str] = None, size: int = 10, page: int = 1
    ) -> Dict[str, Any]:
        """Search records and return the JSON-decoded response.

        Args:
                query: optional free-text query
                size: number of results to return
                page: page number

        Returns:
                A dict representing the JSON response from the backend.
        """

    @abstractmethod
    def get_file_by_id(
        self,
        id: int,
        filename: Optional[str] = None,
        dest_path: Optional[str] = None,
    ) -> str:
        """Download a file referenced by a record and return the saved path.

        Args:
                id: integer id of the record
                filename: optional filename/key to select a specific file in the record
                dest_path: optional destination directory or full path

        Returns:
                The filesystem path to the saved file.
        """
