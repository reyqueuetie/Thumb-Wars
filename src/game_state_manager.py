import threading
from typing import List, Union
from player import Player
from observer import Observable

class GameStateManager(Observable):
    def __init__(self, players: List[Player], max_turns: int = 50):
        super().__init__()
        self.__players = players
        self.__thumb_position = 0
        self.__game_in_progress = True
        self.__current_turn = 0
        self.__max_turns = max_turns

        self.__read_lock = threading.Lock()
        self.__write_lock = threading.Lock()
        self.__readers_count = 0

    def __acquire_read_lock(self):
        with self.__read_lock:
            self.__readers_count += 1
            if self.__readers_count == 1:
                self.__write_lock.acquire()

    def __release_read_lock(self):
        with self.__read_lock:
            self.__readers_count -= 1
            if self.__readers_count == 0:
                self.__write_lock.release()

    def __acquire_write_lock(self):
        self.__write_lock.acquire()

    def __release_write_lock(self):
        self.__write_lock.release()

    def process_action(self, player_index: int, is_special: bool = False) -> dict:
        self.__acquire_write_lock()
        try:
            self.__current_turn += 1
            player = self.__players[player_index]
            
            if is_special:
                push_force = player.special_ability()
                action_type = "SPECIAL ABILITY"
            else:
                push_force = player.push()
                action_type = "PUSH"

            direction = 1 if player_index % 2 == 1 else -1
            self.__thumb_position += push_force * direction

            self.__check_game_end()

            state = {
                'player': player.name,
                'action_type': action_type,  
                'force': push_force,
                'thumb_position': self.__thumb_position,
                'players': {player.name: player.strength for player in self.__players},
                'game_in_progress': self.__game_in_progress,
                'current_turn': self.__current_turn,
                'max_turns': self.__max_turns
            }
            self.notify_observers(state)

            return state
        finally:
            self.__release_write_lock()

    def get_game_state(self) -> dict:
        self.__acquire_read_lock()
        try:
            return {
                'players': {player.name: player.strength for player in self.__players},
                'thumb_position': self.__thumb_position,
                'game_in_progress': self.__game_in_progress,
                'current_turn': self.__current_turn,
                'max_turns': self.__max_turns
            }
        finally:
            self.__release_read_lock()

    def get_winner(self) -> Union[str, None, str]:
        self.__acquire_read_lock()
        try:
            if self.__thumb_position <= -50:
                return self.__players[1].name
            elif self.__thumb_position >= 50:
                return self.__players[0].name
            elif not self.__game_in_progress:
                if self.__current_turn >= self.__max_turns:
                    if abs(self.__thumb_position) < 5:  # If thumb is close to center
                        return "TIE"
                    return self.__players[1].name if self.__thumb_position < 0 else self.__players[0].name  # determines winner based on thumb position direction
                
                strengths = [player.strength for player in self.__players]  # if game ended due to strength depletion, winner is player with more strength
                if abs(strengths[0] - strengths[1]) < 1: 
                    return "TIE"
                return self.__players[strengths.index(max(strengths))].name
            return None
        finally:
            self.__release_read_lock()

    def __check_game_end(self):
        if (any(player.strength <= 0 for player in self.__players) or 
            abs(self.__thumb_position) >= 50 or 
            self.__current_turn >= self.__max_turns):
            self.__game_in_progress = False