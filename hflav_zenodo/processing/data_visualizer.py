import json
from types import SimpleNamespace

from rich import print_json

from hflav_zenodo.processing.visualizer_interface import VisualizerInterface
from hflav_zenodo.utils.namespace_utils import namespace_to_dict


class DataVisualizer(VisualizerInterface):

    def print_schema(self, schema: dict):
        print_json(json.dumps(schema))

    def print_json_data(self, data: SimpleNamespace):
        dict_data = namespace_to_dict(data)
        print_json(json.dumps(dict_data, indent=4))
