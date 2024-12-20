from abc import ABC, abstractmethod
import random

class PushStrategy(ABC):
    @abstractmethod
    def generate_push(self, base_strength: float) -> float:
        pass

class RandomPushStrategy(PushStrategy):
    def generate_push(self, base_strength: float) -> float:
        return random.uniform(1, base_strength / 10)

class PowerPushStrategy(PushStrategy):
    def generate_push(self, base_strength: float) -> float:
        return base_strength / 5 + random.uniform(0, base_strength / 10)

class DefensivePushStrategy(PushStrategy):
    def generate_push(self, base_strength: float) -> float:
        return random.uniform(0.5, base_strength / 20)