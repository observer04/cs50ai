"""
Tic Tac Toe Player
"""

import copy
import math
from multiprocessing import Value

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    if x_count == o_count:
        return X
    else:
        return O
    
    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves.add((i, j))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    (x, y) = action
    if board[x][y] != EMPTY:
        raise ValueError("Invalid action")
    
    if x < 0 or x >= len(board) or y < 0 or y>= len(board[0]):
        raise ValueError("Invalid action")
    
    #deep copy of the board
    action_board = copy.deepcopy(board)
    action_board[x][y] = player(board)
    
    return action_board



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row.count(X) == 3:
            return X
        elif row.count(O) == 3:
            return O
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == X:
            return X
        elif board[0][col] == board[1][col] == board[2][col] == O:
            return O
    if board[0][0] == board[1][1] == board[2][2] == X:
        return X
    elif board[0][0] == board[1][1] == board[2][2] == O:
        return O
    # Anti-diagonal
    if board[0][2] == board[1][1] == board[2][0] == X:
        return X
    elif board[0][2] == board[1][1] == board[2][0] == O:
        return O

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) or is_full(board):
        return True
    else:
        return False
    
def is_full(board):
    for row in board:
        if EMPTY in row:
            return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


# def minimax(board):
#     """
#     Returns the optimal action for the current player on the board.
#     """
#     def max_value(state):
#         if terminal(state):
#             return utility(state), None
#         best_value = -math.inf
#         best_action = None
#         for act in actions(state):
#             value, _ = min_value(result(state, act))
#             if value > best_value:
#                 best_value = value
#                 best_action = act
#                 if best_value == 1:
#                     break
#         return best_value, best_action

#     def min_value(state):
#         if terminal(state):
#             return utility(state), None
#         best_value = math.inf
#         best_action = None
#         for act in actions(state):
#             value, _ = max_value(result(state, act))
#             if value < best_value:
#                 best_value = value
#                 best_action = act
#                 if best_value == -1:
#                     break
#         return best_value, best_action

#     if terminal(board):
#         return None
#     current = player(board)
#     if current == X:
#         _, move = max_value(board)
#         return move
#     else:
#         _, move = min_value(board)
#         return move


