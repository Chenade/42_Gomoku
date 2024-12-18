import numpy as np
from scipy.signal import convolve2d


class Node:
    def __init__(self, position, current_player, x=None, y=None, parent=None):
        """
        Represents a single node in the game tree.

        Args:
            position (list[list[int]]): The current board state.
            current_player (int): The current player (-1 for AI, 1 for human).
            x (int, optional): X-coordinate of the new stone placed. Defaults to None.
            y (int, optional): Y-coordinate of the new stone placed. Defaults to None.
            parent (Node, optional): The parent node. Defaults to None.
        """
        self.position = position  # Current board state
        self.current_player = current_player  # -1 for AI, 1 for human
        self.x = x  # Last move X-coordinate
        self.y = y  # Last move Y-coordinate
        self.parent = parent  # Optional parent node
        self.children = []  # List of child nodes
        self.score = None  # Evaluation score

    def add_child(self, child_node):
        """Add a child node to the current node."""
        self.children.append(child_node)

    def is_leaf(self):
        """Check if the node is a leaf node (no children)."""
        return len(self.children) == 0

    def __repr__(self):
        """String representation for debugging."""
        return f"Node(Player={self.current_player}, Move=({self.x}, {self.y}), Score={self.score})"

    def generate_children(self):
        """
        Generate all possible child nodes for the current node using convolution-based neighbor check.

        Returns:
            List[Node]: List of child nodes.
        """
        # Define the kernel for neighbor detection
        kernel = np.ones((3, 3))
        kernel[1, 1] = 0  # Exclude the center cell

        # Perform convolution to identify cells with neighbors
        neighbor_mask = (
            convolve2d(
                np.abs(self.position), kernel, mode="same", boundary="fill", fillvalue=0
            )
            > 0
        )

        # Identify valid moves: empty cells (self.position == 0) with neighbors
        valid_moves_mask = (self.position == 0) & neighbor_mask

        # Find indices of valid moves
        valid_moves = np.argwhere(valid_moves_mask)

        # Generate child nodes based on valid moves
        children = []
        for x, y in valid_moves:
            new_position = np.copy(self.position)
            new_position[x, y] = self.current_player
            child_node = Node(new_position, -self.current_player, x, y, parent=self)
            children.append(child_node)

        return children

    def has_neighbor(self, grid, distance=1):
        """
        Use convolution to check if each cell has a neighbor.

        Args:
            grid (np.ndarray): The current game board.
            distance (int): The distance to check for neighbors (default=1).

        Returns:
            np.ndarray: A boolean mask where True indicates a neighbor is present.
        """
        # Define the kernel to check for neighbors
        kernel = np.ones((2 * distance + 1, 2 * distance + 1))
        kernel[distance, distance] = 0  # Exclude the center cell itself

        # Perform convolution to count neighbors
        neighbor_count = convolve2d(
            np.abs(grid), kernel, mode="same", boundary="fill", fillvalue=0
        )

        # Return a boolean mask where True indicates the presence of at least one neighbor
        return neighbor_count > 0

    def evaluate_position(self):
        """
        Evaluate the board position and return a score.

        Args:
            position (list[list[int]]): The current board state.

        Returns:
            int: The evaluation score of the position.
        """
        score = 0

        for x in range(len(self.position)):
            for y in range(len(self.position[0])):
                if self.position[x][y] == 1:  # 黒石
                    score += self.evaluate_cell(x, y, 1)
                elif self.position[x][y] == -1:  # 白石
                    score -= self.evaluate_cell(x, y, -1)

        return score

    def evaluate_cell(self, x, y, player):
        """
        Evaluate a single cell in the board.

        Args:
            position (list[list[int]]): The current board state.
            x (int): X-coordinate of the cell.
            y (int): Y-coordinate of the cell.
            player (int): The player to evaluate for (1 or -1).

        Returns:
            int: The evaluation score of the cell.
        """
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        score = 0

        for dx, dy in directions:
            count_player = 0
            count_opponent = 0
            opponent = -player

            for i in range(5):
                nx, ny = x + i * dx, y + i * dy
                if 0 <= nx < len(self.position) and 0 <= ny < len(self.position[0]):
                    if self.position[nx][ny] == player:
                        count_player += 1
                    elif self.position[nx][ny] == opponent:
                        count_opponent += 1
                    else:
                        break

            if count_player > 0 and count_opponent == 0:
                score += 10**count_player

            if count_opponent > 0 and count_player == 0:
                score -= 10**count_opponent

        return score

    def is_game_over(self):
        """
        Check if the game is over.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        # Check for five in a row for both players
        if self.check_five_in_a_row_cnn(self.position == 1):  # Check for player 1
            print("Game Over: Player 1 wins!")
            return True
        if self.check_five_in_a_row_cnn(self.position == -1):  # Check for player -1
            print("Game Over: Player -1 wins!")
            return True

        # Check if the board is full
        if np.all(self.position != 0):
            print("Game Over: Draw!")
            return True

        return False

    def check_five_in_a_row_cnn(self, board):
        """
        Check if there are five in a row using convolution.

        Args:
            board (np.ndarray): The current game board.

        Returns:
            bool: True if there are five in a row, False otherwise.
        """
        # Define kernels for different directions
        horizontal_kernel = np.array([[1, 1, 1, 1, 1]])
        vertical_kernel = horizontal_kernel.T
        diagonal_kernel1 = np.eye(5, dtype=int)
        diagonal_kernel2 = np.fliplr(diagonal_kernel1)

        # Check for five in a row using convolution
        directions = [
            horizontal_kernel,
            vertical_kernel,
            diagonal_kernel1,
            diagonal_kernel2,
        ]

        for kernel in directions:
            # Perform convolution for the current direction
            result = convolve2d(board, kernel, mode="valid")
            # Check if any cell has a value of 5 (indicating 5 in a row)
            if np.any(result == 5):
                return True

        return False
