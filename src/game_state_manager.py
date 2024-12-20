import threading
from typing import List, Union
from player import Player


class GameStateManager:
    def __init__(self, players: List[Player]):
        self.__players = players
        self.__thumb_position = 0
        self.__game_in_progress = True

        self.__read_lock = threading.Lock()
        self.__write_lock = threading.Lock()
        self.__readers_count = 0

    # allows concurrent reads but block writes
    def __acquire_read_lock(self):
        with self.__read_lock:
            self.__readers_count += 1
            if self.__readers_count == 1:
                self.__write_lock.acquire()

    # releases the read lock
    def __release_read_lock(self):
        with self.__read_lock:
            self.__readers_count -= 1
            if self.__readers_count == 0:
                self.__write_lock.release()

    # for writes only
    def __acquire_write_lock(self):
        self.__write_lock.acquire()

    # releases write lock
    def __release_write_lock(self):
        self.__write_lock.release()

    # this is where write operation happens. It modifies game_state based on player action
    def process_action(self, player_index: int, is_special: bool = False) -> dict:
        self.__acquire_write_lock()
        try:
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

            return {
                'player': player.name,
                'action': action_type,
                'force': push_force,
                'thumb_position': self.__thumb_position,
            }
        finally:
            self.__release_write_lock()

    # read happens here by retrieving the current game_state
    def get_game_state(self) -> dict:
        self.__acquire_read_lock()
        try:
            return {
                'players': {player.name: player.strength for player in self.__players},
                'thumb_position': self.__thumb_position,
                'game_in_progress': self.__game_in_progress,
            }
        finally:
            self.__release_read_lock()

    # This is where the winner is determine (read operation)
    def get_winner(self) -> Union[str, None]:
        self.__acquire_read_lock()
        try:
            if self.__thumb_position <= -50:
                return self.__players[1].name
            elif self.__thumb_position >= 50:
                return self.__players[0].name
            elif not self.__game_in_progress:
                strengths = [player.strength for player in self.__players]
                return self.__players[strengths.index(max(strengths))].name
            return None
        finally:
            self.__release_read_lock()

    # updates the game progress status
    def __check_game_end(self):
        if any(player.strength <= 0 for player in self.__players) or abs(self.__thumb_position) >= 50:
            self.__game_in_progress = False