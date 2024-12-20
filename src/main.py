import random
from game_state_manager import GameStateManager
from thumb_wrestling_game import ThumbWars
from player import AggressivePlayer, DefensivePlayer
from push_strategy import RandomPushStrategy, PowerPushStrategy, DefensivePushStrategy 


def main():
    strategies = [
        RandomPushStrategy(),
        PowerPushStrategy(),
        DefensivePushStrategy()
    ]

    player1 = AggressivePlayer("Tom", random.choice(strategies))
    player2 = DefensivePlayer("Jerry", random.choice(strategies))

 
    game_state_manager = GameStateManager([player1, player2])

    game = ThumbWars(game_state_manager)
    game.start()


if __name__ == "__main__":
    main()
