from game_state_manager import GameStateManager
from observer import Scoreboard, Logger
import time

class ThumbWars:
    def __init__(self, game_state_manager: GameStateManager):
        self.__state_manager = game_state_manager

    def start_simulation(self):
        print("\nWELCOME TO THUMB WARS!")
        print("First to push thumb to their side (+/-50) wins!")
        print(f"Maximum turns: {self.__state_manager.get_game_state()['max_turns']}")
        time.sleep(2)
        print("\nSimulating the game...")
        time.sleep(3)

        # self.__state_manager.add_observer(Scoreboard())
        # self.__state_manager.add_observer(Logger())

        while self.__state_manager.get_game_state()["game_in_progress"]:
            for player_index in range(2): 
                is_special = self.__should_use_special_ability(player_index)
                self.__state_manager.process_action(player_index, is_special)

                if not self.__state_manager.get_game_state()["game_in_progress"]:
                    break

            time.sleep(1)

        self.__announce_winner()

    def __should_use_special_ability(self, player_index: int) -> bool:
        player = self.__state_manager.get_game_state()["players"]
        strength = player[list(player.keys())[player_index]]
        return strength < 20  # Use special ability if strength is low

    def __announce_winner(self):
        winner = self.__state_manager.get_winner()
        if winner == "TIE":
            print("\nMATCH DRAW!")
            game_state = self.__state_manager.get_game_state()
            print(f"Final thumb position: {game_state['thumb_position']}")
            print(f"Final player strengths: {game_state['players']}")
        else:
            print(f"\n{winner} wins the match!")
