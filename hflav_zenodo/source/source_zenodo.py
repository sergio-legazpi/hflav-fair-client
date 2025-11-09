"""Zenodo client utilities for HFLAV data.

This module provides a small wrapper around the Zenodo REST API to search
and download records related to HFLAV. It's intentionally small and
dependency-light (only `requests`).
"""

from typing import Optional, Dict, Any, List
import requests
import os
from datetime import datetime

from source.source_interface import SourceInterface


class ZenodoClient(SourceInterface):
    """Simple Zenodo API client.

    Basic contract
    - Inputs: query strings, community name, record id
    - Outputs: parsed JSON from Zenodo or downloaded file path
    - Error modes: raises requests.exceptions on network errors; ValueError
      on missing content.
    """

    DEFAULT_BASE = "https://zenodo.org/api"
    DEFAULT_COMMUNITY = "hflav"

    def __init__(self, session: Optional[requests.Session] = None):
        """Create a client fixed to Zenodo and the HFLAV community.

        The client always uses the public Zenodo API at `https://zenodo.org/api`
        and the `hflav` community. These values are not configurable to keep
        the client focused on HFLAV data.
        """
        self.base_url = self.DEFAULT_BASE
        self.community = self.DEFAULT_COMMUNITY
        self.session = session or requests.Session()

    def _records_url(self) -> str:
        return f"{self.base_url}/records"

    def get_files_by_name(
        self,
        query: Optional[str] = None,
        size: int = 10,
        page: int = 1,
    ) -> Dict[str, Any]:
        """Search records on Zenodo.

        Parameters
        - query: free text query (optional)
        - community: Zenodo community slug (optional)
        - size: number of records to fetch (max 100)
        - page: page number

        Returns JSON-decoded response from the Zenodo API.
        """
        params: Dict[str, Any] = {"size": size, "page": page, "sort": "mostrecent"}
        if query:
            params["q"] = query
        params["communities"] = self.community

        resp = self.session.get(self._records_url(), params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_record(self, recid: int) -> Dict[str, Any]:
        """Fetch a single record by id (record id as shown in Zenodo URL)."""
        url = f"{self._records_url()}/{recid}"
        resp = self.session.get(url, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_file_by_id(
        self,
        id: int,
        filename: Optional[str] = None,
        dest_path: Optional[str] = None,
    ) -> str:
        """Download a file from a record.

        - record_or_id: either the record JSON (dict) or the record id (int)
        - filename: if provided, choose that file from the record.files list
        - dest_path: directory or full filename to save; if None uses cwd

        Returns the path to the saved file.
        """
        if isinstance(id, int):
            record = self.get_record(id)
        else:
            raise ValueError("record_or_id must be an int or a record dict")

        files = record.get("files") or []
        if not files:
            raise ValueError("Record contains no files")

        chosen = None
        if filename:
            for f in files:
                if f.get("key") == filename or f.get("filename") == filename:
                    chosen = f
                    break
        if not chosen:
            chosen = files[0]

        # file links: try 'links'->'download' or 'links'->'self'
        links = chosen.get("links", {})
        url = links.get("download") or links.get("self") or chosen.get("url")
        if not url:
            raise ValueError("No download link found for file")

        r = self.session.get(url, stream=True, timeout=60)
        r.raise_for_status()

        dest_is_dir = dest_path and os.path.isdir(dest_path)
        if dest_path is None or dest_is_dir:
            filename_on_disk = (
                chosen.get("key")
                or chosen.get("filename")
                or f"record_{record.get('id')}_file"
            )
            out_path = os.path.join(dest_path or os.getcwd(), filename_on_disk)
        else:
            out_path = dest_path

        with open(out_path, "wb") as fh:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    fh.write(chunk)

        return out_path
