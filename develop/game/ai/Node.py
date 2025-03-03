import numpy as np
from scipy.signal import convolve2d


class Node:
    def __init__(self, position, current_player, x=None, y=None, parent=None):
        """
        Represents a single node in the game tree.

        Args:
            position (list[list[int]]): The current board state.
            current_player (int): The current player (1 for AI, -1 for human).
            x (int, optional): X-coordinate of the new stone placed. Defaults to None.
            y (int, optional): Y-coordinate of the new stone placed. Defaults to None.
            parent (Node, optional): The parent node. Defaults to None.
        """
        self.position = position  # Current board state
        self.current_player = current_player  # 1 for AI, -1 for human
        self.x = x  # Last move X-coordinate
        self.y = y  # Last move Y-coordinate
        self.parent = parent  # Optional parent node
        self.children = []  # List of child nodes
        self.score = (
            self.parent.score + self.update_score()
            if self.parent
            else self.update_score()
        )

    def generate_children(self):
        """
        Generate all possible child nodes for the current node using convolution-based neighbor check.

        Returns:
            Generator[Node]: Generator of child nodes.
        """
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

        for (x, y), is_valid in np.ndenumerate(valid_moves_mask):
            if is_valid:
                new_position = self.position.copy()
                new_position[x, y] = self.current_player
                yield Node(new_position, -self.current_player, x, y, parent=self)

    def update_score(self):
        """
        Update the score of the current node based on the last move.

        Returns:
            int: The score of the current node.
        """
        if self.x is None or self.y is None:
            return 0  # 初期状態（親がいない場合）のスコアは0

        # 定義されたカーネル（2連、3連、4連、5連）
        k_2 = np.array([[1, 1]])
        k_3 = np.array([[1, 1, 1]])
        k_4 = np.array([[1, 1, 1, 1]])
        k_5 = np.array([[1, 1, 1, 1, 1]])
        kernels = [
            k_2,
            k_3,
            k_4,
            k_5,
            k_2.T,
            k_3.T,
            k_4.T,
            k_5.T,
            np.eye(2, dtype=int),
            np.eye(3, dtype=int),
            np.eye(4, dtype=int),
            np.eye(5, dtype=int),
            np.fliplr(np.eye(2, dtype=int)),
            np.fliplr(np.eye(3, dtype=int)),
            np.fliplr(np.eye(4, dtype=int)),
            np.fliplr(np.eye(5, dtype=int)),
        ]

        weights = {2: 10, 3: 100, 4: 1000, 5: 10000}  # スコアリングの重み

        # チェック範囲を石を置いた位置の近く（5x5）に限定
        xmin = max(0, self.x - 4)
        xmax = min(self.position.shape[0], self.x + 5)
        ymin = max(0, self.y - 4)
        ymax = min(self.position.shape[1], self.y + 5)

        # スコア計算
        score = 0
        local_board = self.position[xmin:xmax, ymin:ymax]  # 局所的な盤面を取得

        for kernel in kernels:
            # カーネルを適用した結果を計算
            result_ai = convolve2d((local_board == 1).astype(int), kernel, mode="valid")
            result_human = convolve2d(
                (local_board == -1).astype(int), kernel, mode="valid"
            )

            # **修正：カーネル全体が特定のプレイヤーの石だけで構成されているかを確認**
            stones = kernel.sum()  # カーネルでチェックする連続石の数
            ai_matches = result_ai == stones  # AIが純粋に連続している部分
            human_matches = result_human == stones  # Humanが純粋に連続している部分

            # **修正：条件を満たした部分のみスコアに反映**
            score += weights.get(stones, 0) * np.sum(ai_matches)  # AIのスコア
            score -= weights.get(stones, 0) * np.sum(human_matches)  # Humanのスコア

        return score

    def is_game_over(self):
        """
        Check if the game is over.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        if self.check_five_in_a_row(self.position == 1):  # Check for AI
            print("Game Over: AI wins!")
            return True
        if self.check_five_in_a_row(self.position == -1):  # Check for Human
            print("Game Over: Human wins!")
            return True

        if np.all(self.position != 0):  # Board is full
            print("Game Over: Draw!")
            return True

        return False

    def check_five_in_a_row(self, board):
        """
        Check if there are five in a row using convolution.

        Args:
            board (np.ndarray): The current game board.

        Returns:
            bool: True if there are five in a row, False otherwise.
        """
        horizontal_kernel = np.array([[1, 1, 1, 1, 1]])
        vertical_kernel = horizontal_kernel.T
        diagonal_kernel1 = np.eye(5, dtype=int)
        diagonal_kernel2 = np.fliplr(diagonal_kernel1)

        directions = [
            horizontal_kernel,
            vertical_kernel,
            diagonal_kernel1,
            diagonal_kernel2,
        ]

        for kernel in directions:
            result = convolve2d(board, kernel, mode="valid")
            if np.any(result == 5):
                return True

        return False
