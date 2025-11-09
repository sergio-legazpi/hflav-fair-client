import json
from pathlib import Path
from typing import Union
from pydantic import BaseModel
from pydantic_core import ValidationError
from zenodo_client import Zenodo

from hflav_zenodo.hflav_schema import hflav_schema_from_dict, hflav_schema_to_dict


class HFLAVApp:
    @classmethod
    def get_json(cls, client: Zenodo, record_id: int, name: str) -> str:
        """Download JSON file from Zenodo using the client and return the local path."""
        return client.download(record_id=record_id, name=name)

    @classmethod
    def from_json(self, json_path_or_str: str) -> BaseModel:
        """Instantiate an average from a JSON file path (is_path=True) or a raw JSON string.

        Example:
            inst = MyAverage.from_json("/tmp/avg.json", client=my_client)
            inst = MyAverage.from_json(json_string, is_path=False)
        """
        try:
            inst = hflav_schema_from_dict(
                json.loads(Path(json_path_or_str).read_text())
            )
        except ValidationError:
            raise
        return inst

    @classmethod
    def from_zenodo(self, client: Zenodo, record_id: int, name: str) -> BaseModel:
        """Download JSON from Zenodo and parse into an instance."""
        path = self.get_json(client=client, record_id=record_id, name=name)
        return self.from_json(path, client=client)

    @classmethod
    def to_json(self, path: Union[str, None] = None) -> str:
        """Serialize the average to JSON. If path is given, write to that file and return the path;
        otherwise return the JSON string. The `client` attribute is excluded from the output.
        """
        j = hflav_schema_to_dict()
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(j)
            return path
        return j
