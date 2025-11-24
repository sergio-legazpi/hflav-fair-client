import json
from types import SimpleNamespace

from rich import print_json

from hflav_zenodo.processing.visualizer_interface import VisualizerInterface


class DataVisualizer(VisualizerInterface):

    def print_schema(self, schema: dict):
        print_json(json.dumps(schema))

    def print_json_data(self, data: SimpleNamespace):
        print_json(json.dumps(data.__dict__, indent=4))
