import time
import sys
import threading
from game_state_manager import GameStateManager


class ThumbWars:
    def __init__(self, game_state_manager: GameStateManager):
        self.__state_manager = game_state_manager

    def start(self):
        print("\n----- WELCOME TO THUMB WARS! -----")
        print("Instructions:")
        print("Player 1: press 'a' for push and 's' for special ability")
        print("Player 2: press 'l' for push and 'k' for special ability")
        print("Press 'q' to quit")

        def input_handler():
            while True:
                key = input().lower()
                if key == 'a':
                    self.__handle_player_action(0, False)
                elif key == 's':
                    self.__handle_player_action(0, True)
                elif key == 'l':
                    self.__handle_player_action(1, False)
                elif key == 'k':
                    self.__handle_player_action(1, True)
                elif key == 'q':
                    print("\nExiting game...")
                    time.sleep(1.0)
                    print("\nGame terminated.")
                    sys.exit(0)

        input_thread = threading.Thread(target=input_handler, daemon=True)
        input_thread.start()

        self.__monitor_game()

    # handles player actions
    def __handle_player_action(self, player_index: int, is_special: bool):
        action_result = self.__state_manager.process_action(player_index, is_special)
        self.__display_action(action_result)

    # displays the player actions
    def __display_action(self, action_result: dict):
        print(f"{action_result['player']} performs {action_result['action']}")
        print(f"Force: {action_result['force']:.2f}")
        print(f"Thumb Position: {action_result['thumb_position']:.2f}")

    # responsible for monitoring game state continiously
    def __monitor_game(self):  
        while True:
            time.sleep(0.5)
            game_state = self.__state_manager.get_game_state()
            if not game_state['game_in_progress']:
                winner = self.__state_manager.get_winner()
                print(f"\n===== {winner} WINS THE THUMB WRESTLING MATCH! =====")
                sys.exit(0)