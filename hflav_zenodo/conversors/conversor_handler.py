from abc import ABC, abstractmethod
from types import SimpleNamespace
from dependency_injector.wiring import inject, Provide

from hflav_zenodo.conversors.conversor_interface import ConversorInterface
from hflav_zenodo.models.models import Template
from hflav_zenodo.processing.visualizer_interface import VisualizerInterface
from hflav_zenodo.source.source_interface import SourceInterface


class ConversorHandler(ABC):

    @inject
    def __init__(
        self,
        source: SourceInterface = Provide["source"],
        conversor: ConversorInterface = Provide["conversor"],
        visualizer: VisualizerInterface = Provide["visualizer"],
    ) -> None:
        self._source = source
        self._conversor = conversor
        self._visualizer = visualizer

    @abstractmethod
    def handle(self, template: Template, data_path: str) -> SimpleNamespace:
        pass

    @abstractmethod
    def can_handle(self, template: Template, data_path: str) -> bool:
        pass

    @abstractmethod
    def set_next(self, handler: "ConversorHandler") -> "ConversorHandler":
        pass
