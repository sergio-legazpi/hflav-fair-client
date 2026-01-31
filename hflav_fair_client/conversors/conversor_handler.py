from abc import ABC, abstractmethod
from types import SimpleNamespace
from dependency_injector.wiring import inject, Provide

from hflav_fair_client.conversors.conversor_interface import ConversorInterface
from hflav_fair_client.models.models import Template
from hflav_fair_client.processing.visualizer_interface import VisualizerInterface
from hflav_fair_client.source.source_interface import SourceInterface


class ConversorHandler(ABC):
    """Abstract base class for Conversor Handlers in the Chain of Responsibility pattern."""

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
        """
        Process the request or pass it to the next handler in the chain.

        Raises:
            NoHandlerCapableException: If no handler in the chain can process the request.
        """
        pass

    @abstractmethod
    def can_handle(self, template: Template, data_path: str) -> bool:
        pass

    @abstractmethod
    def set_next(self, handler: "ConversorHandler") -> "ConversorHandler":
        pass
