from setting.constants import (
    EMPTY,
    WHITE,
    BLACK,
    OFF_BOARD,
    DIRECTIONS,
    CAPTURE_SCORE,
    RATING_SCORES,
    BONUS_DOUBLE_OPEN_FOUR,
    BONUS_OPEN_FOUR_AND_THREE,
    BONUS_DOUBLE_OPEN_THREE,
    OPEN_FOUR_FREE,
    OPEN_FOUR_HALF_FREE,
    OPEN_THREE_FREE,
    OPEN_THREE_HALF_FREE,
)


def board_to_numeric(board):
    """
    Convert the board (list of strings) to a numeric board representation.

    The conversion uses the following mapping:
        - '0': 0
        - 'w': 1
        - 'b': -1
        - 'n': 2

    Args:
        board (list of str): The board state as a list of strings, each representing a row.

    Returns:
        list of list of int: Numeric board representation.
    """
    mapping = {"w": WHITE, "b": BLACK, "n": 2}
    numeric_board = []
    for row in board:
        numeric_row = [mapping.get(cell, EMPTY) for cell in row]
        numeric_board.append(numeric_row)
    return numeric_board


def normalize_board(board, target_color):
    """
    Normalize the board so that patterns for the target_color can be detected
    using the same (white-based) pattern definitions.

    If target_color is BLACK, the board is transformed such that:
      - BLACK stones (-1) become 1
      - WHITE stones (1) become -1
    Other cells remain unchanged.

    Args:
        board (list of list of int): Original board.
        target_color (int): Either WHITE or BLACK.

    Returns:
        list of list of int: Normalized board.
    """
    # If target_color is WHITE, no normalization is needed.
    if target_color == WHITE:
        return board
    normalized_board = []
    for row in board:
        norm_row = []
        for cell in row:
            if cell == WHITE:
                norm_row.append(-1)
            elif cell == BLACK:
                norm_row.append(1)
            else:
                norm_row.append(cell)
        normalized_board.append(norm_row)
    return normalized_board


def get_cells_in_window(i, j, dx, dy, length):
    """
    Return the list of cell coordinates in a window starting at (i,j)
    along direction (dx, dy) of the given length.
    """
    return [(i + k * dx, j + k * dy) for k in range(length)]


def detect_open_four(board, i, j, dx, dy, rows, cols):
    """
    Detect an open four pattern starting at (i, j) in the direction (dx, dy).
    """
    window_cells = []
    for k in range(
        -1, 5
    ):  # create a window from -1 to 4 relative to the current position
        x = i + k * dx
        y = j + k * dy
        # Check bounds; if out of bounds, use OFF_BOARD
        if 0 <= x < rows and 0 <= y < cols:
            window_cells.append((x, y))
        else:
            window_cells.append(None)

    # Convert the coordinates to board values
    window_list = []
    for cell in window_cells:
        if cell is None:
            window_list.append(OFF_BOARD)
        else:
            x, y = cell
            window_list.append(board[x][y])

    if window_list == OPEN_FOUR_FREE:
        rating = "free"
    elif window_list in OPEN_FOUR_HALF_FREE:
        rating = "half-free"
    else:
        return None

    return rating


def detect_open_three(board, i, j, dx, dy, rows, cols):
    """
    Detect an open three pattern starting at (i, j) in the direction (dx, dy).

    The function checks a window of 5 cells (from -1 to 3, inclusive) against the patterns:
      - OPEN_THREE_FREE: [EMPTY, WHITE, WHITE, WHITE, EMPTY]
      - OPEN_THREE_HALF_FREE: various blocked/open configurations.

    Returns:
        "free" if the numeric window matches an open three free pattern,
        "half-free" if it matches an open three half-free pattern,
        None otherwise.
    """

    # Build the window of cell coordinates (using a window of 5 cells)
    window_cells = []
    for k in range(-1, 4):  # k = -1,0,1,2,3 (5 cells)
        x = i + k * dx
        y = j + k * dy
        if 0 <= x < rows and 0 <= y < cols:
            window_cells.append((x, y))
        else:
            window_cells.append(None)  # off-board

    # Build a numeric window list for pattern comparison.
    window_list = []
    for cell in window_cells:
        if cell is None:
            window_list.append(OFF_BOARD)  # Treat off-board as blocked
        else:
            x, y = cell
            window_list.append(board[x][y])

    # Check for open three patterns
    if window_list in OPEN_THREE_FREE:
        rating = "free"
    elif window_list in OPEN_THREE_HALF_FREE:
        rating = "half-free"
    else:
        return None

    return rating


def create_target_board(board, rows, cols):
    """
    Collect candidate coordinates based on the stones on the board.
    For each stone (non-EMPTY cell), add all 8 adjacent and the stone's coordinate.

    Returns:
        set: Candidate positions (i, j) on the board.
    """

    candidate_positions = set()
    for i in range(rows):
        for j in range(cols):
            if board[i][j] != EMPTY:
                for di in range(-1, 2):  # -1, 0, 1
                    for dj in range(-1, 2):  # -1, 0, 1
                        ni = i + di
                        nj = j + dj
                        if 0 <= ni < rows and 0 <= nj < cols:
                            candidate_positions.add((ni, nj))
    return candidate_positions


def detect_patterns(board, candidate_positions, target_color, rows=19, cols=19):
    """
    Scan the board for patterns for the given target_color using the candidate positions.

    If target_color is BLACK, the board is normalized so that the white-based
    pattern definitions can be used.

    Args:
        board (list of list of int): The numeric board representation.
        candidate_positions (set): Candidate positions (i, j) to check.
        target_color (int): WHITE or BLACK.

    Returns:
        int: The total score from detected patterns (including bonus).
    """
    norm_board = (
        board if target_color == WHITE else normalize_board(board, target_color)
    )
    open_four_scores = []
    open_three_scores = []

    for i, j in candidate_positions:
        for dx, dy in DIRECTIONS:
            rating = detect_open_four(norm_board, i, j, dx, dy, rows, cols)
            if rating is not None:
                key = f"open-four-{rating}"
                open_four_scores.append(RATING_SCORES.get(key, 0))
            rating = detect_open_three(norm_board, i, j, dx, dy, rows, cols)
            if rating is not None:
                key = f"open-three-{rating}"
                open_three_scores.append(RATING_SCORES.get(key, 0))

    # Base score is the sum of the detected patterns
    base_score = sum(open_four_scores) + sum(open_three_scores)

    bonus = 0
    count_four = len(open_four_scores)
    count_three = len(open_three_scores)

    if count_four >= 2:
        bonus += BONUS_DOUBLE_OPEN_FOUR
    if count_four >= 1 and count_three >= 1:
        bonus += BONUS_OPEN_FOUR_AND_THREE
    if count_three >= 2:
        bonus += BONUS_DOUBLE_OPEN_THREE

    total_score = base_score + bonus
    return total_score


def heuristic_score(board, captures=None, rows=19, cols=19):
    """
    Calculate the heuristic score for the given board state.

    First, candidate positions are computed based on the placement of stones.
    Then, scores for both WHITE and BLACK are computed using these candidate positions.
    The base score is the difference (my_score - opp_score) from pattern detection.
    A capture bonus is added, which is computed as:
        capture_bonus = k * (my_captures - opponent_captures)
    where k is set to 1000. The capture counts are taken from the captures dictionary
    (with keys WHITE and BLACK). If no captures dictionary is provided, the bonus is 0.

    Args:
        board (list of list of int): The numeric board state.
        captures (dict, optional): A dictionary with keys WHITE and BLACK corresponding
                                   to capture counts. If not provided, capture bonus is 0.

    Returns:
        int: The resulting heuristic score.
    """
    candidate_positions = create_target_board(board, rows=rows, cols=cols)
    my_score = detect_patterns(board, candidate_positions, target_color=WHITE, rows=rows, cols=cols)
    opp_score = detect_patterns(board, candidate_positions, target_color=BLACK, rows=rows, cols=cols)
    alignment_score = my_score - opp_score

    capture_bonus = 0
    if captures is not None:
        my_captures = captures.get(WHITE, 0)
        opp_captures = captures.get(BLACK, 0)
        capture_bonus = CAPTURE_SCORE * (my_captures - opp_captures)

    return alignment_score + capture_bonus
