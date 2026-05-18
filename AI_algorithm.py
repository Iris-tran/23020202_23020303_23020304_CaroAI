# minimax.py
import math
from typing import List, Tuple
from constants import MAX_DEPTH, EMPTY, PLAYER_X, AI_O, BOARD_SIZE
from game_logic import check_win, is_draw, get_empty_cells
from evaluation import evaluate_board

def heuristic_order(board: List[List[str]], moves: List[Tuple[int, int]], ai_player: str) -> List[Tuple[int, int]]:
    def score_move(move):
        i, j = move
        count = 0
        for di in [-1,0,1]:
            for dj in [-1,0,1]:
                ni, nj = i+di, j+dj
                if 0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE and board[ni][nj] != EMPTY:
                    count += 1
        return count
    return sorted(moves, key=score_move, reverse=True)

def minimax(board: List[List[str]], depth: int, is_maximizing: bool, player_ai: str):
    opponent = PLAYER_X if player_ai == AI_O else AI_O
    states = 1
    if check_win(board, player_ai):
        return 1000000, None, states
    if check_win(board, opponent):
        return -1000000, None, states
    if depth == 0 or is_draw(board):
        return evaluate_board(board, player_ai), None, states

    moves = get_empty_cells(board)
    if is_maximizing:
        best_value = -math.inf
        best_move = None
        for move in moves:
            i, j = move
            board[i][j] = player_ai
            value, _, child_states = minimax(board, depth-1, False, player_ai)
            board[i][j] = EMPTY
            states += child_states
            if value > best_value:
                best_value = value
                best_move = move
        return best_value, best_move, states
    else:
        best_value = math.inf
        best_move = None
        for move in moves:
            i, j = move
            board[i][j] = opponent
            value, _, child_states = minimax(board, depth-1, True, player_ai)
            board[i][j] = EMPTY
            states += child_states
            if value < best_value:
                best_value = value
                best_move = move
        return best_value, best_move, states

def alphabeta(board: List[List[str]], depth: int, is_maximizing: bool, alpha: float, beta: float, player_ai: str):
    opponent = PLAYER_X if player_ai == AI_O else AI_O
    states = 1
    if check_win(board, player_ai):
        return 1000000, None, states
    if check_win(board, opponent):
        return -1000000, None, states
    if depth == 0 or is_draw(board):
        return evaluate_board(board, player_ai), None, states

    moves = get_empty_cells(board)
    moves = heuristic_order(board, moves, player_ai)

    if is_maximizing:
        best_value = -math.inf
        best_move = None
        for move in moves:
            i, j = move
            board[i][j] = player_ai
            value, _, child_states = alphabeta(board, depth-1, False, alpha, beta, player_ai)
            board[i][j] = EMPTY
            states += child_states
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_value, best_move, states
    else:
        best_value = math.inf
        best_move = None
        for move in moves:
            i, j = move
            board[i][j] = opponent
            value, _, child_states = alphabeta(board, depth-1, True, alpha, beta, player_ai)
            board[i][j] = EMPTY
            states += child_states
            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value, best_move, states