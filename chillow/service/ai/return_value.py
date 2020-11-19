from dataclasses import dataclass

from chillow.model.action import Action


@dataclass
class ReturnValue:
    action: Action = None
