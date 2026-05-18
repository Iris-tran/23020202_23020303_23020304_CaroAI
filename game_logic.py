# game_logic.py
from typing import List, Tuple
from constants import BOARD_SIZE, EMPTY, PLAYER_X, AI_O, WIN_COUNT

def check_win(board: List[List[str]], player: str) -> bool:
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == player:
                for dx, dy in directions:
                    count = 1
                    for step in range(1, WIN_COUNT):
                        x = i + step * dx
                        y = j + step * dy
                        if x < 0 or x >= BOARD_SIZE or y < 0 or y >= BOARD_SIZE or board[x][y] != player:
                            break
                        count += 1
                    if count >= WIN_COUNT:
                        return True
    return False

def is_draw(board: List[List[str]]) -> bool:
    for row in board:
        if EMPTY in row:
            return False
    return True

def get_empty_cells(board: List[List[str]]) -> List[Tuple[int, int]]:
    return [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if board[i][j] == EMPTY]