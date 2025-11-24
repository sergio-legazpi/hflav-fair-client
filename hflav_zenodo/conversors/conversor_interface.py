from abc import ABC, abstractmethod
from types import SimpleNamespace


class ConversorInterface(ABC):
    """Abstract interface for conversion from template and data to domain objects used by HFLAV.

    This defines the public contract to convert HFLAV data. Implementations must provide the methods below and
    follow the documented input/output shapes.
    """

    @abstractmethod
    def generate_instance_from_template_and_data(
        self, template_path: str, data_path: str
    ) -> SimpleNamespace:
        """Generate an instance from a template and data files.

        Args:
                template_path: path to the JSON template file
                data_path: path to the JSON data file

        Returns:
                An instance validated and generated from the template and data files

        Raises:
                ValueError: If the template or data files are invalid.
                StructureException: If the data structure does not match the template format.

        """
