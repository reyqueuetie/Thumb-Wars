from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, state: dict) -> None:
        pass

class Scoreboard(Observer):
    def update(self, state: dict) -> None:
        print(f"\nScoreboard: {state['players']}, Thumb Position: {state['thumb_position']}")

class Logger(Observer):
    def update(self, state: dict) -> None:
        self.__display_move(state)
        print(f"Force: {state['force']}")
        print(f"Current Turn: {state['current_turn']}\n")

    def __display_move(self, state: dict) -> None:
        player_name = state['player'] 
        action_type = state['action_type']
        print(f"{player_name} performed a {action_type}!")

class Observable(ABC):
    def __init__(self):
        self._observers = []

    def add_observer(self, observer: Observer) -> None:
        self._observers.append(observer)

    def notify_observers(self, state: dict) -> None:
        for observer in self._observers:
            observer.update(state)