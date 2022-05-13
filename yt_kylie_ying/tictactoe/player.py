# Player classes for the 06 and 07 TicTacToe games
import math
import random


class Player:
    def __init__(self, letter):
        # letter is x or o
        self.letter = letter

    # we want all players to get their next move given a game
    def get_move(self, game):
        pass


class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-8):')
            # check that it is a correct value by trying to cast it to an integer
            # if it's not, then i's invalid
            # if spot taken, it's invalid too
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True  # if gets here, input is ok
            except ValueError:
                print('Invalid square. Try again.')

        return val


class GeniusComputerPlayer(Player):
    # AI for 07
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            # randomly choose at the start
            square = random.choice(game.available_moves())
        else:
            # get the square based off the minimax algorithm
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter  # yourself
        other_player = 'O' if player == 'X' else 'X'  # the other player

        # first check if previous is winner move
        if state.current_winner == other_player:
            # return position and score to keep track of the score for minimax to work
            return {
                'position': None,
                'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)
            }

        elif not state.empty_squares():  # no empty squares
            return {
                'position': None,
                'score': 0
            }

        if player == max_player:
            best = {'position': None, 'score': -math.inf}
            # each score should maximize (be larger)
        else:
            best = {'position': None, 'score': math.inf}
            # each score should minimize

        for possible_move in state.available_moves():
            # step 1 make a move, try that spot
            state.make_move(possible_move, player)
            # step 2 recurse using minimax to simulate a game after that move
            sim_score = self.minimax(state, other_player)
            # step 3 undo that move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move
            # step 4 update the dictionaries if necessary
            if player == max_player:
                if sim_score['score'] > best['score']:
                    # maximizing the max_player, good, keep it
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    # minimizing the other player, also good, keep it
                    best = sim_score

        return best
