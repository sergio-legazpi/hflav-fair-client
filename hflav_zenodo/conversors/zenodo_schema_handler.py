from hflav_zenodo import logger
from types import SimpleNamespace
from hflav_zenodo.conversors.conversor_handler import ConversorHandler
from hflav_zenodo.models.models import Template

logger = logger.get_logger(__name__)


class ZenodoSchemaHandler(ConversorHandler):
    """Handler for Zenodo schema conversor.

    It's the first handler in the chain of responsibility for processing

    It is triggered when the schema is found inside Zenodo records.

    If it cannot handle the request, it passes it to the next handler in the chain.
    """

    def handle(self, template: Template, data_path: str) -> SimpleNamespace:
        logger.info("ZenodoSchemaHandler: Handling the request...")
        if not self.can_handle(template, data_path):
            logger.info(
                "ZenodoSchemaHandler: Cannot handle the request, passing to next handler..."
            )
            self._next_handler.handle(template, data_path)

    def can_handle(self, template: Template, data_path: str) -> bool:
        return template.jsonschema is not None

    def set_next(self, handler: "ConversorHandler") -> "ConversorHandler":
        self._next_handler = handler
        return handler
