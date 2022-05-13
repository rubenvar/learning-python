from tictactoe.player import HumanPlayer, RandomComputerPlayer, GeniusComputerPlayer
from tictactoe.game import TicTacToe, play


if __name__ == '__main__':
    # # human starts
    # x_player = HumanPlayer('X')
    # o_player = GeniusComputerPlayer('O')
    # t = TicTacToe()
    # play(t, x_player, o_player, print_game=True)
    # # or computer starts:
    # x_player = GeniusComputerPlayer('X')
    # o_player = HumanPlayer('O')
    # t = TicTacToe()
    # play(t, x_player, o_player, print_game=True)
    # or computer vs genius computer
    x_wins = 0
    o_wins = 0
    ties = 0
    for _ in range(1000):
        x_player = RandomComputerPlayer('X')
        o_player = GeniusComputerPlayer('O')
        t = TicTacToe()
        result = play(t, x_player, o_player, print_game=False)
        if result == 'X':
            x_wins += 1
        elif result == 'O':
            o_wins += 1
        else:
            ties += 1

    print(
        f"After 1000 iterations, we see {x_wins} 'X' wins, {o_wins} 'O' wins, and {ties} ties")
