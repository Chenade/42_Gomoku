from .heuristic import heuristic_score
from setting.constants import (
    WHITE,
    BLACK,
    EMPTY,
    OFF_BOARD,
    ROWS,
    COLS,
    DIRECTIONS,
    DIRECTIONS_FRONT_BACK,
    CAPTURE_WHITE,
    CAPTURE_BLACK,
    WINNING_SCORE_WHITE,
    WINNING_SCORE_BLACK,
    FORBIDDEN_SCORE_WHITE,
    FORBIDDEN_SCORE_BLACK,
    DRAW_SCORE,
)
import random
import logging
from game.rules.rule_double_three import check_double_three


class Node:
    def __init__(
        self,
        board,
        move=None,
        stone_type=None,
        heuristic_cost=None,
        depth=0,
        parent_my_captures=0,
        parent_opponent_captures=0,
    ):
        """
        Initialize a Node for minimax search.

        Args:
            board (list of list of int): The current board state.
            move (tuple, optional): The move (row, col) that led to this board state.
            stone_type (int, optional): The type of stone placed in the move.
            heuristic_cost (int or float, optional): The heuristic evaluation of the current board.
            depth (int, optional): The depth of this node in the search tree.
            parent_my_captures (int, optional): The number of captures for the player.
            parent_opponent_captures (int, optional): The number of captures for the opponent.
        """
        self.board = board
        self.move = move
        self.stone_type = stone_type
        self.heuristic_cost = heuristic_cost
        self.depth = depth
        self.children = []
        self.captures = {WHITE: parent_my_captures, BLACK: parent_opponent_captures}

        ## is_forbidden_move is a flag indicating whether the move is forbidden.
        self.is_forbidden_move = check_double_three(board, move, stone_type)

        # Update the captures based on the current board state and store them as attributes.
        self.board, self.captures = self.update_captures()

        # Now we can call is_gameover() as an instance method.
        self.is_terminal, self.winner = self.is_gameover()

    def update_captures(self):
        """
        Update the number of captures for each player based on the current board state.

        From the coordinates of the new stone (self.move) in each direction,
        if a window of 4 cells (including the new stone) matches the following pattern,
        then the two enemy stones in the middle are removed from the board and the capture count is increased by 2:

            - If stone_type is WHITE: [WHITE, BLACK, BLACK, WHITE]
            - If stone_type is BLACK: [BLACK, WHITE, WHITE, BLACK]

        Cells outside the board are treated as OFF_BOARD, thus the pattern does not match.

        Returns:
            tuple: (updated_board, captures) after processing any captures.
        """
        # If no new stone has been placed, do nothing and return the current board and captures.
        if self.move is None:
            return self.board, self.captures

        def in_bounds(r, c):
            return 0 <= r < ROWS and 0 <= c < COLS

        new_row, new_col = self.move

        # Select the pattern and the opponent's stone type according to the color of the stone.
        if self.stone_type == WHITE:
            pattern = CAPTURE_WHITE[:]
        elif self.stone_type == BLACK:
            pattern = CAPTURE_BLACK[:]
        else:
            return self.board, self.captures

        captures_made = 0

        for dx, dy in DIRECTIONS:
            # ★ Forward check: When the new stone is at the beginning of the window.
            forward_window = []
            coordinates_forward = []
            for k in range(4):  # k: 0,1,2,3; obtaining each cell.
                r = new_row + k * dx
                c = new_col + k * dy
                coordinates_forward.append((r, c))
                if in_bounds(r, c):
                    forward_window.append(self.board[r][c])
                else:
                    forward_window.append(OFF_BOARD)
            if forward_window == pattern:
                # The middle two stones (indices 1 and 2) are eligible for capture.
                r1, c1 = coordinates_forward[1]
                r2, c2 = coordinates_forward[2]
                self.board[r1][c1] = EMPTY
                self.board[r2][c2] = EMPTY
                captures_made += 2

            # ★ Backward check: When the new stone is at the end of the window.
            backward_window = []
            coordinates_backward = []
            # For the backward check, obtain 3 cells in the reverse direction from the new stone, and then reverse the order to match the pattern.
            for k in range(3, -1, -1):  # k = 3,2,1,0
                r = new_row - k * dx
                c = new_col - k * dy
                coordinates_backward.append((r, c))
                if in_bounds(r, c):
                    backward_window.append(self.board[r][c])
                else:
                    backward_window.append(OFF_BOARD)
            if backward_window == pattern:
                # The stones at positions with indices 1 and 2 are eligible for capture.
                r1, c1 = coordinates_backward[1]
                r2, c2 = coordinates_backward[2]
                self.board[r1][c1] = EMPTY
                self.board[r2][c2] = EMPTY
                captures_made += 2

        # Update the capture count (self.captures is already initialized as {WHITE: ..., BLACK: ...})
        if self.stone_type == WHITE:
            self.captures[WHITE] += captures_made
        else:
            self.captures[BLACK] += captures_made

        # Return the updated board and captures.
        return self.board, self.captures

    def check_five_in_a_row(self):
        """
        Check if there is any alignment of five or more stones matching the stone type of the last move on the board.

        This function scans the board for five consecutive stones in any of the
        following directions:
            - Horizontal (to the right)
            - Vertical (downwards)
            - Diagonal down-right
            - Diagonal up-right

        If such an alignment is found, self.winner is set to the stone type (BLACK or WHITE).

        Returns:
            bool: True if an alignment is found, False otherwise.
        """
        if self.stone_type is None:
            return False
        target = self.stone_type
        for i in range(ROWS):
            for j in range(COLS):
                if self.board[i][j] == target:
                    for dx, dy in DIRECTIONS:
                        count = 1
                        x, y = i, j
                        while True:
                            x += dx
                            y += dy
                            if x < 0 or x >= ROWS or y < 0 or y >= COLS:
                                break
                            if self.board[x][y] == target:
                                count += 1
                            else:
                                break
                        if count >= 5:
                            return True
        return False

    def check_capture(self):
        """
        Check if either player has reached the capture limit.

        Returns:
            tuple: (bool, winner) where bool indicates if the capture limit is reached,
                   and winner is either WHITE, BLACK, or None.
        """
        if self.captures[WHITE] >= 10:
            return True, WHITE
        if self.captures[BLACK] >= 10:
            return True, BLACK
        return False, None

    def is_gameover(self):
        """
        Check if the game is over.

        Returns:
            tuple: (bool, winner) indicating the game over status and the winner.
        """
        if self.check_five_in_a_row():
            return True, self.stone_type
        capture_over, winner = self.check_capture()
        if capture_over:
            return True, winner
        return False, None

    def add_child(self, child_node):
        self.children.append(child_node)

    def __repr__(self):
        board_str = "\n".join(" ".join(str(cell) for cell in row) for row in self.board)
        return (
            f"Node(move={self.move}, stone_type={self.stone_type},\n"
            f"     heuristic_cost={self.heuristic_cost}, depth={self.depth},\n"
            f"     captures={self.captures},\n"
            f"     is_terminal={self.is_terminal},\n"
            f"     winner={self.winner},\n"
            f"     is_forbidden_move={self.is_forbidden_move})\n"
            f"     board=\n{board_str}"
        )

    def get_heuristic_score(self):
        """
        Compute and return the heuristic score for the current board state.

        This method utilizes the updated heuristic_score function from heuristic.py,
        which calculates the score as the sum of the alignment score (from pattern detection)
        and the capture bonus defined as:
            capture_bonus = 1000 * (my captures - opponent captures)

        Returns:
            int: The heuristic score.
        """
        if self.is_forbidden_move:
            if self.stone_type == WHITE:
                return FORBIDDEN_SCORE_WHITE
            else:
                return FORBIDDEN_SCORE_BLACK
        # If it's a terminal state, return a fixed score based on the game result.
        if self.is_terminal:
            # self.winner is expected to be set within is_gameover().
            if self.winner == WHITE:  # e.g., when the maximizing player is WHITE
                return WINNING_SCORE_WHITE
            elif self.winner == BLACK:
                return WINNING_SCORE_BLACK
            else:
                return DRAW_SCORE
        else:
            # Perform a regular board evaluation.
            return heuristic_score(self.board, self.captures)

    def generate_child_nodes(self, next_stone_type=None):
        """
        Generate and return the child nodes representing all possible moves that are in
        the rectangular window surrounding the placed stones.
        If no stones have been allocated (i.e., the board is empty), this function will consider
        the center of the board as the only candidate move.

        Additionally, if there exists at least one child node for which placing the stone
        (regardless of color) creates three consecutive stones (vertically, horizontally,
        diagonally right, or diagonally left), only those nodes are returned.
        If no such node exists, 5 random child nodes from the generated candidates are returned.

        Args:
            next_stone_type (int, optional): The stone type for the next move. If not provided,
                it will be determined as the opposite of the current stone (or a default if no move has been made).

        Returns:
            list: A list of child Node objects.
        """
        # Determine the stone type for the next move.
        if next_stone_type is None:
            if self.stone_type is None:
                next_stone_type = (
                    BLACK  # Assume Black goes first if no move has been made.
                )
            else:
                next_stone_type = BLACK if self.stone_type == WHITE else WHITE

        possible_moves = set()
        # For every allocated stone, add all empty adjacent positions.
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c] != EMPTY:
                    # Check the surrounding 3x3 area.
                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < ROWS and 0 <= nc < COLS:
                                if self.board[nr][nc] == EMPTY:
                                    possible_moves.add((nr, nc))

        # If no stone has been placed, choose the center.
        if not possible_moves:
            center_move = (ROWS // 2, COLS // 2)
            possible_moves.add(center_move)

        child_nodes = []
        for move in possible_moves:
            # Create a deep copy of the board to simulate the move.
            new_board = [row[:] for row in self.board]
            new_r, new_c = move
            new_board[new_r][new_c] = next_stone_type
            child_node = Node(
                board=new_board,
                move=move,
                stone_type=next_stone_type,
                depth=self.depth + 1,
                parent_my_captures=self.captures[WHITE],
                parent_opponent_captures=self.captures[BLACK],
            )
            child_nodes.append(child_node)
        logging.debug("Generated %d child nodes.", len(child_nodes))

        # --- 以下、各子ノードにおいて、置いた石が3連続になっているかチェックする ---
        def in_bounds(r, c):
            return 0 <= r < ROWS and 0 <= c < COLS

        def has_three_in_a_row(board, r, c):
            """
            Returns True if the stone at (r, c) forms at least 3 consecutive stones
            (of any color: WHITE or BLACK) when checking both forward and backward in each of the 8 directions.
            """
            stone = board[r][c]
            if stone == EMPTY:
                return False

            def in_bounds(x, y):
                return 0 <= x < ROWS and 0 <= y < COLS

            for dx, dy in DIRECTIONS_FRONT_BACK:
                count = 1  # 現在の石をカウント
                # 正方向
                x, y = r + dx, c + dy
                while in_bounds(x, y) and board[x][y] == stone:
                    count += 1
                    x += dx
                    y += dy
                # 逆方向
                x, y = r - dx, c - dy
                while in_bounds(x, y) and board[x][y] == stone:
                    count += 1
                    x -= dx
                    y -= dy
                if count >= 3:
                    return True
            return False

        def has_three_in_a_row(board, r, c):
            """
            Returns True if the stone at (r, c) forms at least 3 consecutive stones
            in one of the 4 directions: horizontal, vertical,
            diagonal right, or diagonal left.
            """
            for dx, dy in DIRECTIONS_FRONT_BACK:
                count = 1
                x, y = r + dx, c + dy
                while in_bounds(x, y) and board[x][y] in (WHITE, BLACK):
                    count += 1
                    x += dx
                    y += dy
                if count >= 3:
                    return True
            return False

        returned_child_nodes = []
        three_row_nodes = [
            child
            for child in child_nodes
            if has_three_in_a_row(child.board, child.move[0], child.move[1])
        ]
        if three_row_nodes:
            logging.debug(
                "Found %d child node(s) with three in a row.", len(three_row_nodes)
            )
            if len(three_row_nodes) >= 10:
                return three_row_nodes
            else:
                remaining = [
                    child for child in child_nodes if child not in three_row_nodes
                ]
                num_needed = 10 - len(three_row_nodes)
                additional = (
                    random.sample(remaining, min(num_needed, len(remaining)))
                    if remaining
                    else []
                )
                returned_child_nodes = three_row_nodes + additional
                return returned_child_nodes
        else:
            num_to_return = min(10, len(child_nodes))
            random_nodes = random.sample(child_nodes, num_to_return)
            logging.debug(
                "No three-in-a-row child node found. Returning %d random child nodes.",
                num_to_return,
            )
            return random_nodes
