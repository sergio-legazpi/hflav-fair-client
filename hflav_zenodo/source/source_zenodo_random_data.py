from datetime import datetime
import json
from typing import List, Optional

from hypothesis import given, settings, Phase, HealthCheck
import hypothesis
from hypothesis_jsonschema import from_schema

from hflav_zenodo.filters.base_query import BaseQuery
from hflav_zenodo.models.models import File, Record, Template
from hflav_zenodo.source.source_interface import SourceInterface


class SourceZenodoRandomData(SourceInterface):

    _schema = {
        "$schema": "http://json-schema.org/draft-06/schema#",
        "$ref": "#/definitions/Hflav",
        "definitions": {
            "Hflav": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "metadata": {"$ref": "#/definitions/Metadata"},
                    "groups": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/Group"},
                        "minItems": 1,
                    },
                },
                "required": ["groups", "metadata"],
                "title": "Hflav",
            },
            "Group": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "name": {
                        "type": "string",
                        "minLength": 1,
                        "pattern": "^[\\x20-\\x7E]*$",
                    },
                    "fit": {"$ref": "#/definitions/Fit"},
                    "averages": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/AverageElement"},
                        "minItems": 1,
                    },
                    "averages_correlation": {
                        "type": "array",
                        "items": {"type": "array", "items": {"type": "number"}},
                    },
                    "inputs": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/Input"},
                        "minItems": 1,
                    },
                    "contours": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/Contour"},
                    },
                    "scans": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/Scan"},
                    },
                    "inputs_correlation": {
                        "type": "array",
                        "items": {"type": "array", "items": {"type": "number"}},
                    },
                },
                "required": [
                    "averages",
                    "averages_correlation",
                    "contours",
                    "fit",
                    "inputs",
                    "inputs_correlation",
                    "name",
                    "scans",
                ],
                "title": "Group",
            },
            "AverageElement": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "name": {
                        "type": "string",
                        "minLength": 1,
                        "pattern": "^[\\x20-\\x7E]*$",
                    },
                    "comment": {
                        "type": "string",
                        "minLength": 1,
                        "pattern": "^[\\x20-\\x7E]*$",
                    },
                    "PDGcode": {
                        "type": "string",
                        "pattern": "^\\d+$",
                    },
                    "average": {"$ref": "#/definitions/AverageAverage"},
                    "intervals": {
                        "type": "array",
                        "items": {"type": "array", "items": {"type": "number"}},
                    },
                },
                "required": ["average", "comment", "intervals", "name", "PDGcode"],
                "title": "AverageElement",
            },
            "AverageAverage": {
                "type": "object",
                "additionalProperties": False,
                "properties": {"value": {"$ref": "#/definitions/AverageValue"}},
                "required": ["value"],
                "title": "AverageAverage",
            },
            "AverageValue": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "central": {"$ref": "#/definitions/Point"},
                    "uncertainty": {"$ref": "#/definitions/Point"},
                    "statistical": {"$ref": "#/definitions/Point"},
                    "systematic": {"$ref": "#/definitions/Point"},
                    "upperlimit": {"type": "number"},
                    "unit": {
                        "type": "string",
                        "minLength": 1,
                        "pattern": "^[\\x20-\\x7E]*$",
                    },
                },
                "required": [
                    "central",
                    "statistical",
                    "systematic",
                    "uncertainty",
                    "unit",
                    "upperlimit",
                ],
                "title": "AverageValue",
            },
            "Contour": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "name": {
                        "type": "string",
                        "minLength": 1,
                        "pattern": "^[\\x20-\\x7E]*$",
                    },
                    "x": {"$ref": "#/definitions/ContourX"},
                    "y": {"$ref": "#/definitions/ContourX"},
                    "CL": {"type": "number"},
                    "points": {
                        "type": "array",
                        "items": {"type": "array", "items": {"type": "number"}},
                        "minItems": 1,
                    },
                },
                "required": ["CL", "name", "points", "x", "y"],
                "title": "Contour",
            },
            "ContourX": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "name": {
                        "type": "string",
                        "minLength": 1,
                        "pattern": "^[\\x20-\\x7E]*$",
                    },
                    "unit": {
                        "type": "string",
                        "minLength": 1,
                        "pattern": "^[\\x20-\\x7E]*$",
                    },
                },
                "required": ["name", "unit"],
                "title": "ContourX",
            },
            "Fit": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "chi2": {"type": "number"},
                    "ndf": {"type": "integer"},
                    "p": {"type": "number"},
                },
                "required": ["chi2", "ndf", "p"],
                "title": "Fit",
            },
            "Input": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "name": {
                        "type": "string",
                        "minLength": 1,
                        "pattern": "^[\\x20-\\x7E]*$",
                    },
                    "comment": {
                        "type": "string",
                        "minLength": 1,
                        "pattern": "^[\\x20-\\x7E]*$",
                    },
                    "sources": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/Source"},
                        "minItems": 1,
                    },
                    "intervals": {
                        "type": "array",
                        "items": {"type": "array", "items": {"type": "number"}},
                    },
                },
                "required": ["comment", "intervals", "name", "sources"],
                "title": "Input",
            },
            "Source": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "name": {
                        "type": "string",
                        "minLength": 1,
                        "pattern": "^[\\x20-\\x7E]*$",
                    },
                    "comment": {
                        "type": "string",
                        "minLength": 1,
                        "pattern": "^[\\x20-\\x7E]*$",
                    },
                    "value": {"$ref": "#/definitions/SourceValue"},
                    "references": {"$ref": "#/definitions/References"},
                },
                "required": ["comment", "name", "references", "value"],
                "title": "Source",
            },
            "References": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "bibtex": {
                        "type": "string",
                        "minLength": 1,
                        "pattern": "^[\\x20-\\x7E]*$",
                    },
                    "pub": {
                        "type": "string",
                        "minLength": 1,
                        "pattern": "^[\\x20-\\x7E]*$",
                    },
                    "doi": {
                        "type": "string",
                        "pattern": "^10\\.\\d{4,9}/[-._;()/:A-Z0-9]+$",
                    },
                    "arxiv": {
                        "type": "string",
                        "pattern": "^(arXiv:\\d{4}\\.\\d{4,5}|\\d{4}\\.\\d{4,5}v\\d+)$",
                    },
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "pattern": "^https?://[^\\s]+$",
                    },
                },
                "required": ["arxiv", "bibtex", "doi", "pub", "url"],
                "title": "References",
            },
            "SourceValue": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "central": {"$ref": "#/definitions/Point"},
                    "statistical": {"$ref": "#/definitions/Point"},
                    "systematic": {"$ref": "#/definitions/Point"},
                    "uncertainty": {"type": "number"},
                    "unit": {
                        "type": "string",
                        "minLength": 1,
                        "pattern": "^[\\x20-\\x7E]*$",
                    },
                },
                "required": [
                    "central",
                    "statistical",
                    "systematic",
                    "uncertainty",
                    "unit",
                ],
                "title": "SourceValue",
            },
            "Scan": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "name": {
                        "type": "string",
                        "minLength": 1,
                        "pattern": "^[\\x20-\\x7E]*$",
                    },
                    "x": {"$ref": "#/definitions/ScanX"},
                    "y": {"$ref": "#/definitions/ScanX"},
                    "points": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/Point"},
                        "minItems": 1,
                    },
                },
                "required": ["name", "points", "x", "y"],
                "title": "Scan",
            },
            "ScanX": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "name": {
                        "type": "string",
                        "minLength": 1,
                        "pattern": "^[\\x20-\\x7E]*$",
                    },
                    "unit": {
                        "type": "string",
                        "minLength": 1,
                        "pattern": "^[\\x20-\\x7E]*$",
                    },
                    "values": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 1,
                    },
                },
                "required": ["name", "unit", "values"],
                "title": "ScanX",
            },
            "Metadata": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "title": {
                        "type": "string",
                        "minLength": 1,
                        "pattern": "^[\\x20-\\x7E]*$",
                    },
                    "description": {
                        "type": "string",
                        "minLength": 1,
                        "pattern": "^[\\x20-\\x7E]*$",
                    },
                    "version": {
                        "type": "string",
                        "pattern": "^\\d+\\.\\d+\\.\\d+$",
                    },
                    "date": {
                        "type": "string",
                        "format": "date",
                        "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
                    },
                    "author": {
                        "type": "string",
                        "minLength": 1,
                        "pattern": "^[\\x20-\\x7E]*$",
                    },
                    "schema": {
                        "type": "string",
                        "const": "http://json-schema.org/draft-06/schema#",
                    },
                },
                "required": [
                    "author",
                    "date",
                    "description",
                    "schema",
                    "title",
                    "version",
                ],
                "title": "Metadata",
            },
            "Point": {
                "anyOf": [
                    {"type": "array", "items": {"type": "number"}},
                    {"type": "number"},
                ],
                "title": "Point",
            },
        },
    }

    _random_generated_data_name = "random_generated_data.json"

    _schema_name = "hflav_zenodo_schema.schema"

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
