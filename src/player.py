from abc import ABC, abstractmethod
from typing import Type, Union
from push_strategy import PushStrategy

class Player(ABC):
    def __init__(self, name: str, push_strategy: PushStrategy):
        self._name = name
        self._strength = 50.0
        self._push_strategy = push_strategy
        self._special_ability_count = 3

    @property
    def name(self) -> str:
        return self._name

    @property
    def strength(self) -> float:
        return self._strength

    def push(self) -> float:
        push_force = self._push_strategy.generate_push(self._strength)
        self._strength -= push_force / 2
        return push_force

    def special_ability(self) -> float:
        if self._special_ability_count > 0:
            self._special_ability_count -= 1
            return self._perform_special_ability()
        return 0

    @abstractmethod
    def _perform_special_ability(self) -> float:
        pass

class AggressivePlayer(Player):
    def _perform_special_ability(self) -> float:
        power_surge = self._strength / 3
        self._strength -= power_surge / 2
        return power_surge * 2

class DefensivePlayer(Player):
    def _perform_special_ability(self) -> float:
        block_force = self._strength / 4
        self._strength += block_force / 2
        return block_force

class PlayerBuilder:
    def __init__(self):
        self._name: Union[str, None] = None
        self._push_strategy: Union[PushStrategy, None] = None
        self._player_type: Union[Type[Player], None] = None

    def set_name(self, name: str) -> "PlayerBuilder":
        self._name = name
        return self

    def set_push_strategy(self, strategy: PushStrategy) -> "PlayerBuilder":
        self._push_strategy = strategy
        return self

    def set_player_type(self, player_type: Type[Player]) -> "PlayerBuilder":
        self._player_type = player_type
        return self

    def build(self) -> Player:
        if not (self._name and self._push_strategy and self._player_type):
            raise ValueError("Missing properties to build a Player")
        return self._player_type(self._name, self._push_strategy)
