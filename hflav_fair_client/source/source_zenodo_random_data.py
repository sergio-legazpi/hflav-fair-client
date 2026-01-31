from datetime import datetime
import json
from typing import List, Optional

from hypothesis import given, settings, Phase, HealthCheck
import hypothesis
from hypothesis_jsonschema import from_schema

from hflav_fair_client.filters.base_query import BaseQuery
from hflav_fair_client.models.models import File, Record, Template
from hflav_fair_client.source.source_interface import SourceInterface


class SourceZenodoRandomData(SourceInterface):

    def __init__(self):
        super().__init__()
        with open(
            "hflav_fair_client/resources/random_data_schema.schema",
            "r",
            encoding="utf-8",
        ) as file:
            schema_dict = json.load(file)
        self._schema = schema_dict

    _random_generated_data_name = "random_generated_data.json"

    _schema_name = "hflav_fair_client_schema.schema"

    # Cache the strategy to avoid recreating it on every call
    _cached_strategy = None

    def get_records_by_name(self, query: BaseQuery) -> List[Record]:
        record_data = {
            "id": 1,
            "doi": "10.1234/random.doi",
            "metadata": {
                "title": "Random Generated Record",
            },
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),
            "links": {},
            "files": [
                {
                    "key": self._random_generated_data_name,
                    "links": {"self": self._random_generated_data_name},
                },
            ],
        }
        return [
            Record(
                **record_data,
            )
        ]

    def get_correct_template_by_date(self, date: Optional[datetime] = None) -> Template:
        template_data = {
            "id": 123456,
            "metadata": {
                "title": "Random Generated Template",
                "version": "1.0.0",
            },
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),
            "files": [
                {
                    "key": self._random_generated_data_name,
                    "links": {"self": self._random_generated_data_name},
                },
                {
                    "key": self._schema_name,
                    "links": {"self": self._schema_name},
                },
            ],
        }
        return Template(
            **template_data,
        )

    def get_record(self, recid: int) -> Record:
        record_data = {
            "id": 1,
            "doi": "10.1234/random.doi",
            "metadata": {
                "title": "Random Generated Record",
            },
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),
            "links": {},
            "files": [
                {
                    "key": self._random_generated_data_name,
                    "links": {"self": self._random_generated_data_name},
                },
                {
                    "key": self._schema_name,
                    "links": {"self": self._schema_name},
                },
            ],
        }
        return Record(
            **record_data,
        )

    def _generate_random_data(self):
        if self._cached_strategy is None:
            self._cached_strategy = from_schema(self._schema)

        settings_obj = settings(
            max_examples=1,
            phases=[Phase.generate],
            database=None,
            suppress_health_check=[
                HealthCheck.too_slow,
                HealthCheck.data_too_large,
                HealthCheck.filter_too_much,
            ],
            deadline=None,
            derandomize=True,
        )

        data = hypothesis.find(
            self._cached_strategy,
            lambda x: True,
            settings=settings_obj,
        )

        return data

    def download_file_by_id_and_filename(
        self,
        id: int,
        filename: str,
        dest_path: Optional[str] = None,
    ) -> str:
        if filename == self._random_generated_data_name:
            data = self._generate_random_data()

        if filename == self._schema_name:
            data = self._schema

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return filename
