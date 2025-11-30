from abc import ABC
from types import SimpleNamespace
from typing import List

from hflav_zenodo.processing.visualizer_interface import VisualizerInterface
from hflav_zenodo.utils.namespace_utils import dict_to_namespace, namespace_to_dict


class BaseHflavDataDecorator(ABC):
    """
    Abstract base class for HFLAV data decorators.

    Attributes:
        _hflav_data (SimpleNamespace): The HFLAV data stored as a SimpleNamespace.
    """

    def __init__(self, hflav_data: SimpleNamespace):
        self._hflav_data = hflav_data

    def __getattr__(self, name):
        return getattr(self._hflav_data, name)

    def get_data_as_namespace(self) -> SimpleNamespace:
        return self._hflav_data
