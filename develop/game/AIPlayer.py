import numpy as np
import time


class AIPlayer:
    def __init__(self, depth=3):
        self.depth = depth

    def minimax(self, position, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_game_over(position):
            return self.evaluate_position(position)

        if maximizing_player:
            max_eval = float("-inf")
            for child in self.generate_children(position):
                eval = self.minimax(child, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval

        else:
            min_eval = float("inf")
            for child in self.generate_children(position):
                eval = self.minimax(child, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_position(self, position):
        score = 0

        for x in range(len(position)):
            for y in range(len(position[0])):
                if position[x][y] == 1:  # 黒石
                    score += self.evaluate_cell(position, x, y, 1)
                elif position[x][y] == -1:  # 白石
                    score -= self.evaluate_cell(position, x, y, -1)

        return score

    def evaluate_cell(self, position, x, y, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 横, 縦, 斜め
        score = 0

        for dx, dy in directions:
            count = 0
            for i in range(5):  # 最大5つ先までチェック
                nx, ny = x + i * dx, y + i * dy
                if (
                    0 <= nx < len(position)
                    and 0 <= ny < len(position[0])
                    and position[nx][ny] == player
                ):
                    count += 1
                else:
                    break
            if count > 0:
                score += 10**count  # 連続数に応じて指数的にスコアを加算

        return score

    def generate_children(self, position):
        children = []

        for x in range(len(position)):
            for y in range(len(position[0])):
                if position[x][y] == 0:  # 空きマス
                    new_position = [row[:] for row in position]  # 現在の盤面をコピー
                    new_position[x][y] = 1  # 仮に黒石を置く
                    children.append(
                        (new_position, x, y)
                    )  # Return the position and the move coordinates

        return children

    def is_game_over(self, position):
        for x in range(len(position)):
            for y in range(len(position[0])):
                if self.check_five_in_a_row(position, x, y):
                    return True

        if all(cell != 0 for row in position for cell in row):
            return True

        return False

    def check_five_in_a_row(self, position, x, y):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 横, 縦, 斜め
        for dx, dy in directions:
            count = 0
            for i in range(5):  # 5マス先までチェック
                nx, ny = x + i * dx, y + i * dy
                if (
                    0 <= nx < len(position)
                    and 0 <= ny < len(position[0])
                    and position[nx][ny] == position[x][y]
                ):
                    count += 1
                else:
                    break
            if count == 5:
                return True
        return False

    def get_best_move(self, position):
        best_move = None
        best_score = float("-inf")

        for child in self.generate_children(position):
            score = self.minimax(child, self.depth, float("-inf"), float("inf"), False)
            if score > best_score:
                best_score = score
                best_move = child

        return best_move

    def visualize_scores(self, position):
        """
        Visualize the score for each position on the board.
        Args:
            ai_player: Instance of AIPlayer.
            position: Current game board as a 2D list or numpy array.
        """
        position = np.array(position)
        score_board = np.zeros_like(position, dtype=float)

        for x in range(position.shape[0]):
            for y in range(position.shape[1]):
                if position[x, y] == 0:  # Evaluate only empty cells
                    test_position = position.copy()
                    test_position[x, y] = 1  # Simulate placing a black stone
                    score_board[x, y] = self.evaluate_position(test_position)

        print("Score Visualization:")
        for row in score_board:
            print(" ".join(f"{cell:6.1f}" for cell in row))

    def get_top_moves(self, position, top_n=3):
        """
        Get the top N best moves for the current position.
        Args:
            position: The current game board as a 2D list.
            top_n: The number of top moves to return.
        Returns:
            A list of tuples (score, (x, y)) sorted by score in descending order.
        """
        scored_moves = []

        for child, x, y in self.generate_children(position):
            score = self.minimax(child, self.depth, float("-inf"), float("inf"), False)
            scored_moves.append((score, (x, y)))

        scored_moves.sort(
            key=lambda x: x[0], reverse=True
        )  # Sort by score in descending order
        return scored_moves[:top_n]


# Example usage:
if __name__ == "__main__":

    # Sample board setup
    sample_board = [
        [0, 0, 0, 0, 0],
        [0, 1, -1, 0, 0],
        [0, -1, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0],
    ]

    # Create an AIPlayer instance
    ai = AIPlayer(depth=3)

    # Visualize scores for the given board
    ai.visualize_scores(sample_board)

    # 上位3つの手を取得
    start_time = time.time()
    top_moves = ai.get_top_moves(sample_board, top_n=3)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.3f} seconds")
    # 結果を表示
    for rank, (score, (x, y)) in enumerate(top_moves, start=1):
        print(f"Rank {rank}: Score = {score}, Move = ({x}, {y})")
