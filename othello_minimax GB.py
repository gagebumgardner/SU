from othello_rules import *


def evaluate(state):
    """
    Returns 1 if '#' has won, -1 if 'O' has won, and 0 if the game has ended in a draw.
    If the game is not over, returns score / 100, giving a number from -0.64 to 0.64.
    This way, search will prefer winning to merely being ahead by any amount.
    """
    scores = score(state)
    if game_over(state):
        if scores < 0:
            return -1
        if scores > 0:
            return 1
    else:
        scorez = scores/100.0
        return scorez


def minimax(state, player, max_depth):
    """
    Returns the value of state with player to play. max_depth gives the search depth; if 0, returns the evaluation
    of state.
    """
    if max_depth ==0:
        return evaluate(state)
    successors = (successor(state, move, player) for move in legal_moves(state, player))
    if player == '#':
        return max(minimax(s, 'O',max_depth - 1) for s in successors)
    else:
        return min(minimax(s, '#',max_depth - 1) for s in successors)


def best_move(state, player, max_depth):
    """Returns player's best move. max_depth, which must be at least 1, gives the search depth."""
    moves = legal_moves(state, player)
    if player == '#':
        return max(moves, key=lambda m: minimax(successor(state, m, '#'), 'O', max_depth - 1))
    else:
        return min(moves, key=lambda m: minimax(successor(state, m, 'O'), '#', max_depth - 1))


if __name__ == '__main__':
    game = INITIAL_STATE
    while not game_over(game):
        print('# to play')
        print(prettify(game))
        print('Thinking...')
        m = best_move(game, '#', 5)
        print(m)
        game = successor(game, m, '#')
        if not game_over(game):
            while True:
                print('O to play')
                print(prettify(game))
                m = input('Enter row and column (0-7, separated by a space) or pass: ')
                if m != 'pass':
                    m = tuple([int(n) for n in m.split()])
                print(m)
                if m in legal_moves(game, 'O'):
                    break
            game = successor(game, m, 'O')
    print(prettify(game))
    result = score(game)
    if result > 0:
        print('# wins!')
    elif result == 0:
        print('Draw.')
    else:
        print('O wins!')
