import json

from abc import ABCMeta, abstractmethod
from chillow.model.action import Action


class DataWriter(metaclass=ABCMeta):
    """Converts an object to a string."""

    @abstractmethod
    def write(self, action: Action) -> str:
        """Converts an action to a string.

        Args:
            action: The action to be converted.

        Returns:
            The action as a string.
        """
        pass


class JSONDataWriter(DataWriter):
    """Converts an object to a JSON string."""

    def write(self, action: Action) -> str:
        """Converts an action to a JSON string.

        Args:
            action: The action to be converted.

        Returns:
            The action as a JSON string.
        """

        return json.dumps({"action": action.name})
