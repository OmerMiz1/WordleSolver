from game import WordleGame
from players.computer_player import ComputerPlayer


def run(runs_count=1):
    game = WordleGame()
    player = ComputerPlayer()

    wins = 0

    for i in range(1, runs_count + 1):
        game.reset()
        player.reset()

        player.solve(game)
        result = ""
        if game.is_winner():
            result = "Win"
            wins += 1
        else:
            result = "Lose"
        print(f"\rcur run: {i}, win rate: {wins / i}", end="")
    print(f"\nwins: {wins}/{runs_count} ({wins / runs_count}%)")


if __name__ == "__main__":
    run()
    run(100)

