# Debug setting
DEBUG_MODE = True

# Description: Constants for the game of Gomoku.
EMPTY = 0
WHITE = 1
BLACK = -1
OFF_BOARD = 9

ROWS = 19
COLS = 19

DIRECTIONS = [(0, 1), (1, 0), (1, 1), (-1, 1)]
DIRECTIONS_FRONT_BACK = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]

WINNING_SCORE_WHITE = 1000000
WINNING_SCORE_BLACK = -1000000

FORBIDDEN_SCORE_WHITE = -10000000
FORBIDDEN_SCORE_BLACK = 10000000

DRAW_SCORE = 0

# Capture patterns
CAPTURE_WHITE = [WHITE, BLACK, BLACK, WHITE]
CAPTURE_BLACK = [BLACK, WHITE, WHITE, BLACK]

CAPTURE_SCORE = 1000

# Heuristic scoring constants and pattern definitions (moved from heuristic.py)
RATING_SCORES = {
    "open-four-free": 10000,
    "open-four-half-free": 1500,
    "open-three-free": 1000,
    "open-three-half-free": 500,
}

# Bonus constants for the heuristic evaluation
BONUS_DOUBLE_OPEN_FOUR = 1000  # Bonus if count_four is at least 2
BONUS_OPEN_FOUR_AND_THREE = (
    500  # Bonus if at least one open four and one open three are detected
)
BONUS_DOUBLE_OPEN_THREE = 200  # Bonus if count_three is at least 2

# Pattern definitions for open fours and open threes
OPEN_FOUR_FREE = [EMPTY, WHITE, WHITE, WHITE, WHITE, EMPTY]

OPEN_FOUR_HALF_FREE = [
    [BLACK, WHITE, WHITE, WHITE, WHITE, EMPTY],
    [OFF_BOARD, WHITE, WHITE, WHITE, WHITE, EMPTY],
    [EMPTY, WHITE, WHITE, WHITE, WHITE, BLACK],
    [EMPTY, WHITE, WHITE, WHITE, WHITE, OFF_BOARD],
    [WHITE, EMPTY, WHITE, WHITE, WHITE, EMPTY],
    [WHITE, EMPTY, WHITE, WHITE, WHITE, BLACK],
    [WHITE, EMPTY, WHITE, WHITE, WHITE, OFF_BOARD],
    [WHITE, WHITE, EMPTY, WHITE, WHITE, EMPTY],
    [WHITE, WHITE, EMPTY, WHITE, WHITE, BLACK],
    [WHITE, WHITE, EMPTY, WHITE, WHITE, OFF_BOARD],
    [WHITE, WHITE, WHITE, EMPTY, WHITE, EMPTY],
    [WHITE, WHITE, WHITE, EMPTY, WHITE, BLACK],
    [WHITE, WHITE, WHITE, EMPTY, WHITE, OFF_BOARD],
]

OPEN_THREE_FREE = [[EMPTY, WHITE, WHITE, WHITE, EMPTY]]

OPEN_THREE_HALF_FREE = [
    [BLACK, WHITE, WHITE, WHITE, EMPTY],
    [OFF_BOARD, WHITE, WHITE, WHITE, EMPTY],
    [EMPTY, WHITE, WHITE, WHITE, BLACK],
    [EMPTY, WHITE, WHITE, WHITE, OFF_BOARD],
    [WHITE, EMPTY, WHITE, WHITE, EMPTY],
    [EMPTY, WHITE, EMPTY, WHITE, WHITE],
    [WHITE, WHITE, EMPTY, WHITE, EMPTY],
    [EMPTY, WHITE, WHITE, EMPTY, WHITE],
]
