# evaluation.py
from typing import List
from constants import EMPTY, PLAYER_X, AI_O, WIN_COUNT, BOARD_SIZE

PATTERN_VALUES = {
    "0000": 0,
    "1000": 1, "0100": 1, "0010": 1, "0001": 1,
    "2000": -3, "0200": -3, "0020": -3, "0002": -3,
    "1100": 10, "0110": 10, "0011": 10,
    "1010": 8,
    "1110": 50, "0111": 50, "1011": 50, "1101": 50,
    "1001": 15,
    "2002": -20,
    "2020": -15,
    "2202": -60,
    "2022": -60,
    "1111": 100000,
    "2111": 70, "1211": 50, "1121": 50, "1112": 70,
    "2222": -100000,
    "2221": -80, "1222": -80, "2220": -100, "0222": -100,
    "2200": -30, "0220": -30, "0022": -30
}

def get_pattern_score(sequence: str, player: str) -> int:
    """Tính điểm của chuỗi quân trên bàn cờ."""
    mapped = []
    for ch in sequence:
        if ch == EMPTY:
            mapped.append('0')
        elif ch == player:
            mapped.append('1')
        else:
            mapped.append('2')
    pattern = ''.join(mapped)
    return PATTERN_VALUES.get(pattern, 0)

def evaluate_board_for_player(board: List[List[str]], player: str) -> int:
    """Nhận biết các chuỗi của 1 player trên bàn cờ và tính toán tổng điểm của player đó."""
    total = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            for dx, dy in directions:
                end_x = i + (WIN_COUNT - 1) * dx
                end_y = j + (WIN_COUNT - 1) * dy
                if 0 <= end_x < BOARD_SIZE and 0 <= end_y < BOARD_SIZE:
                    seq = []
                    for step in range(WIN_COUNT):
                        x = i + step * dx
                        y = j + step * dy
                        seq.append(board[x][y])
                    total += get_pattern_score(''.join(seq), player)
    return total

def evaluate_board(board: List[List[str]], ai_player: str) -> int:
    """So sánh điểm của AI so với người chơi."""
    opponent = PLAYER_X if ai_player == AI_O else AI_O
    ai_score = evaluate_board_for_player(board, ai_player)
    opponent_score = evaluate_board_for_player(board, opponent)
    return ai_score - opponent_score