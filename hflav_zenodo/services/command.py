from abc import ABC, abstractmethod
from typing import Any
from hflav_zenodo.logger import get_logger

logger = get_logger(__name__)


class Command(ABC):
    @abstractmethod
    def execute(self) -> Any:
        pass

    @abstractmethod
    def undo(self) -> Any:
        pass


class CommandInvoker:
    """Invoker class to execute and manage commands using the Command pattern."""

    def __init__(self):
        self._command = None
        self._history = CommandHistory()

    def set_command(self, command: Command):
        self._command = command

    def execute_command(self):
        if self._command:
            self._history.add_command(self._command)
            return self._command.execute()
        else:
            raise ValueError("No command set")

    def undo_command(self):
        return self._history.undo_last()


class CommandHistory:
    def __init__(self):
        self._history: list[Command] = []

    def add_command(self, command: Command):
        self._history.append(command)

    def undo_last(self):
        if self._history:
            command = self._history.pop()
            command.undo()
        else:
            logger.info("No commands to undo.")
