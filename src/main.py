import random
from game_state_manager import GameStateManager
from thumb_wrestling_game import ThumbWars
from player import AggressivePlayer, DefensivePlayer
from push_strategy import RandomPushStrategy, PowerPushStrategy, DefensivePushStrategy
from observer import Scoreboard, Logger

def main():
    strategies = [
        RandomPushStrategy(),
        PowerPushStrategy(),
        DefensivePushStrategy()
    ]

    #You can select between aggressive or defensive player
    player1 = AggressivePlayer("Bing", random.choice(strategies))
    player2 = AggressivePlayer("Chilling", random.choice(strategies))

    game_state_manager = GameStateManager([player1, player2])

    scoreboard = Scoreboard()
    logger = Logger()

    game_state_manager.add_observer(scoreboard)
    game_state_manager.add_observer(logger)

    game = ThumbWars(game_state_manager)
    game.start_simulation()

if __name__ == "__main__":
    main()
