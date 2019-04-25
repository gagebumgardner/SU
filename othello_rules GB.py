from copy import deepcopy


def diagram_to_state(diagram):
    """Converts a list of strings into a list of lists of characters (strings of length 1.)"""
    return [list(a) for a in diagram]


INITIAL_STATE = diagram_to_state(['........',
                                  '........',
                                  '........',
                                  '...#O...',
                                  '...O#...',
                                  '........',
                                  '........',
                                  '........'])


def count_pieces(state):
    """Returns a dictionary of the counts of '#', 'O', and '.' in state."""
    result = {'#': 0, 'O': 0, '.': 0}
    for row in state:
        for space in row:
            if space == '#':
                result['#'] += 1
            elif space == 'O':
                result['O'] += 1
            else:
                result['.'] += 1
    return result


def prettify(state):
    """
    Returns a single human-readable string representing state, including row and column indices and counts of
    each color.
    """
    hash = 0
    o = 0
    blank = 0
    pretty = ' 01234567'
    for a in range(0, len(state)):
        pretty += '\n'
        pretty += str(a)
        for b in range(0, len(state[a])):
            pretty += state[a][b]
            if state[a][b] == '#':
                hash += 1
            elif state[a][b] == 'O':
                o += 1
            elif state[a][b] == '.':
                blank += 1
        pretty += str(a)
    pretty += '\n 01234567\n'
    pretty += "{'#': "+str(hash)+", 'O': "+str(o)+", '.': "+str(blank)+"}\n"
    return pretty


def opposite(color):
    """opposite('#') returns 'O'. opposite('O') returns '#'."""
    if color == '#':
        return 'O'
    elif color == 'O':
        return '#'


def flips(state, r, c, color, dr, dc):
    """
    Returns a list of pieces that would be flipped if color played at r, c, but only searching along the line
    specified by dr and dc. For example, if dr is 1 and dc is -1, consider the line (r+1, c-1), (r+2, c-2), etc.

    :param state: The game state.
    :param r: The row of the piece to be  played.
    :param c: The column of the piece to be  played.
    :param color: The color that would play at r, c.
    :param dr: The amount to adjust r on each step along the line.
    :param dc: The amount to adjust c on each step along the line.
    :return A list of (r, c) pairs of pieces that would be flipped.
    """
    flip = []
    row = r + dr
    col = c + dc
    if row > 7 or col > 7:
        return []
    if row < 0 or col < 0:
        return []
    while True:
        tile = state[row][col]
        if tile == '.':
            return []
        elif tile == color:
            return flip
        elif tile == opposite(color):
            flip.append((row, col))
        row += dr
        col += dc
        if row > 7 or col > 7:
            return []
        if row < 0 or col < 0:
            return []


OFFSETS = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))


def flips_something(state, r, c, color):
    """Returns True if color playing at r, c in state would flip something."""
    for x in OFFSETS:
        if len(flips(state, r, c, color, x[0], x[1])) > 0:
            return True
    return False


def legal_moves(state, color):
    """
    Returns a list of legal moves ((r, c) pairs) that color can make from state. Note that a player must flip
    something if possible; otherwise they must play the special move 'pass'.
    """
    moves = []
    for r in range(0, 8):
        for c in range(0, 8):
            if state[r][c] == '.':
                if flips_something(state, r, c, color):
                    moves.append((r, c))
    if len(moves) == 0:
        return ['pass']
    return moves


def successor(state, move, color):
    """
    Returns the state that would result from color playing move (which is either a pair (r, c) or 'pass'.
    Assumes move is legal.
    """
    if move == 'pass':
        return state
    flip = []
    new_state = deepcopy(state)
    for x in OFFSETS:
        if len(flips(state, move[0], move[1], color, x[0], x[1])) > 0:
            flip.append(flips(state, move[0], move[1], color, x[0], x[1]))
    for i in flip:
        for j in i:
            new_state[j[0]][j[1]] = color
        new_state[move[0]][move[1]] = color
    return new_state



def score(state):
    """
    Returns the scores in state. More positive values (up to 64 for occupying the entire board) are better for '#'.
    More negative values (down to -64) are better for 'O'.
    """
    scores = 0
    for r in range(0, 8):
        for c in range(0, 8):
            if state[r][c] == '#':
                scores += 1
            if state[r][c] == 'O':
                scores -= 1
    return scores


def game_over(state):
    """
    Returns true if neither player can flip anything.
    """
    if legal_moves(state, '#') == ['pass'] and legal_moves(state, 'O') == ['pass']:
        return True
    return False
