from abc import ABC, abstractmethod
from types import SimpleNamespace


class VisualizerInterface(ABC):
    """Abstract base class defining the interface for data visualizers.

    This interface establishes the contract for classes that visualize data
    in various formats. Implementations should provide methods to display
    JSON schemas and JSON data in a user-friendly format.

    The primary purpose is to provide visual representation of structured data to end users.
    """

    @abstractmethod
    def print_schema(schema: dict) -> None:
        """Print a JSON schema in a formatted, visual way.

        This method takes a dictionary representing a JSON schema and displays it
        in a human-readable format. The implementation should enhance readability
        through formatting, colors, or other visual aids.

        Args:
            schema (dict): A dictionary containing the JSON schema to visualize.

        Returns:
            None: This method outputs directly to the console/display.

        Example:
            >>> schema = {"type": "object", "properties": {...}}
            >>> visualizer.print_schema(schema)
            # Displays formatted schema

        Note:
            Implementations should handle nested schemas appropriately and
            provide clear visual hierarchy.
        """
        pass

    @abstractmethod
    def print_json_data(data: SimpleNamespace) -> None:
        """Print JSON data in a formatted, visual way.

        This method takes a SimpleNamespace object containing data and displays it
        in a human-readable JSON format. The implementation should provide
        indentation, syntax highlighting, or other features to improve readability.

        Args:
            data (SimpleNamespace): A SimpleNamespace object containing the data
                                   to visualize. The object's __dict__ attribute
                                   will be used to extract the data structure.

        Returns:
            None: This method outputs directly to the console/display.

        Example:
            >>> from types import SimpleNamespace
            >>> data = SimpleNamespace(name="test", value=123)
            >>> visualizer.print_json_data(data)
            # Displays formatted JSON data

        Note:
            Implementations should handle nested data structures and provide
            proper JSON formatting with appropriate indentation.
        """
        pass
