import numpy as np
import time
from Node import Node
from Tree import Tree

class AIPlayer:
    def __init__(self, depth=3):
        self.depth = depth
        self.tree = []


    def minimax(self, position, depth, alpha, beta, current_player):
        """
        Minimax algorithm with alpha-beta pruning.
        Args:
            position: Current board state as a 2D list.
            depth: Depth of the search tree.
            alpha: Alpha value for pruning.
            beta: Beta value for pruning.
            current_player: The player whose turn it is (-1 for AI, 1 for human).
        Returns:
            The best score for the current player.
        """
        if depth == 0 or self.is_game_over(position):
            return self.evaluate_position(position)

        maximizing_player = current_player == -1

        if maximizing_player:
            max_eval = float("-inf")
            for child, x, y in self.generate_children(position, current_player):
                eval = self.minimax(child, depth - 1, alpha, beta, 1)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for child, x, y in self.generate_children(position, current_player):
                eval = self.minimax(child, depth - 1, alpha, beta, -1)
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
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        score = 0

        for dx, dy in directions:
            count_player = 0
            count_opponent = 0
            opponent = -player

            for i in range(5):
                nx, ny = x + i * dx, y + i * dy
                if 0 <= nx < len(position) and 0 <= ny < len(position[0]):
                    if position[nx][ny] == player:
                        count_player += 1
                    elif position[nx][ny] == opponent:
                        count_opponent += 1
                    else:
                        break

            if count_player > 0 and count_opponent == 0:
                score += 10**count_player

            if count_opponent > 0 and count_player == 0:
                score -= 10**count_opponent

        return score

    def generate_children(self, position, player):
        """
        Generate all possible moves but only for the cells that have a neighbor.
        """
        children = []

        for x in range(len(position)):
            for y in range(len(position[0])):
                if position[x][y] == 0 and self.has_neighbor(position, x, y):
                    new_position = [row[:] for row in position]
                    new_position[x][y] = player
                    children.append((new_position, x, y))

        return children

    def has_neighbor(self, position, x, y, distance=1):
        """
        Check if a cell has a neighbor within a given distance.
        """
        for dx in range(-distance, distance + 1):
            for dy in range(-distance, distance + 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < len(position)
                    and 0 <= ny < len(position[0])
                    and position[nx][ny] != 0
                ):
                    return True
        return False

    def is_game_over(self, position):
        for x in range(len(position)):
            for y in range(len(position[0])):
                if self.check_five_in_a_row(position, x, y):
                    print("Game Over", x, y)
                    return True

        if all(cell != 0 for row in position for cell in row):
            return True

        return False

    def check_five_in_a_row(self, position, x, y):
        if position[x][y] == 0:  # 空きマスではチェックしない
            return False

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 横, 縦, 斜め
        for dx, dy in directions:
            count = 1  # 現在の石をカウント

            # 正方向をカウント
            for i in range(1, 5):
                nx, ny = x + i * dx, y + i * dy
                if (
                    0 <= nx < len(position)
                    and 0 <= ny < len(position[0])
                    and position[nx][ny] == position[x][y]
                ):
                    count += 1
                else:
                    break

            # 逆方向をカウント
            for i in range(1, 5):
                nx, ny = x - i * dx, y - i * dy
                if (
                    0 <= nx < len(position)
                    and 0 <= ny < len(position[0])
                    and position[nx][ny] == position[x][y]
                ):
                    count += 1
                else:
                    break

            # 5連以上が揃ったら勝利
            if count >= 5:
                return True
        return False


    def get_top_moves(self, position, current_player, top_n=3):
        """
        Get the top N best moves for the given player.
        Args:
            position: Current board state as a 2D list.
            current_player: The player whose moves to evaluate (-1 for AI, 1 for human).
            top_n: Number of top moves to return.
        Returns:
            A list of tuples (score, (x, y)) sorted by score in descending order.
        """
        scored_moves = []

        for child, x, y in self.generate_children(position, current_player):
            score = self.minimax(
                child, self.depth, float("-inf"), float("inf"), -current_player
            )
            scored_moves.append((score, (x, y)))

        # Sort moves by score in descending order Tree level1 to level0
        #         1
        #       /   \
        #    -1      -1
        # (ScoreA) > (ScoreB)
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        return scored_moves[:top_n]
    

    def minimax_with_tree(self, position, depth, alpha, beta, current_player, level=0, parent="Root"):
        """
        Modified minimax algorithm to log scores at each level for tree visualization.
        """
        if depth == 0 or self.is_game_over(position):
            score = self.evaluate_position(position)
            self.tree.append(
                f"{' ' * (2 * level)}[Depth {level}] {parent} -> Score: {score}"
            )
            return score

        maximizing_player = current_player == -1
        best_score = float("-inf") if maximizing_player else float("inf")

        for child, x, y in self.generate_children(position, current_player):
            child_id = f"Move ({x}, {y})"
            score = self.minimax_with_tree(child, depth - 1, alpha, beta, -current_player, level + 1, child_id)

            if maximizing_player:
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
            else:
                best_score = min(best_score, score)
                beta = min(beta, best_score)

            if beta <= alpha:
                break

        self.tree.append(
            f"{' ' * (2 * level)}[Depth {level}] {parent} -> Best Score: {best_score}"
        )
        return best_score

    def save_tree_to_file(self, filename):
        """
        Save the tree representation to a file.
        """
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(self.tree))




# Example usage:
if __name__ == "__main__":
    
    # Read the board from file
    def load_board(filename):
        symbol_to_number = {
            '·': 0,
            '●': 1,
            '○': -1
        }
        with open(filename, 'r') as f:
            return [[symbol_to_number[cell] for cell in line.strip().split(',')] 
                   for line in f]
    
    # Load the sample board from file
    sample_board = load_board('./test/sample.txt')

    # for row in sample_board:
    #     print(row)

    # Create an AIPlayer instance
    ai = AIPlayer(depth=3)


    # # Create a score visualization board
    # position = np.array(sample_board)
    # score_board = np.zeros_like(position, dtype=float)

    # # Fill the score board
    # for x in range(position.shape[0]):
    #     for y in range(position.shape[1]):
    #         if position[x, y] == 0:  # Evaluate only empty cells
    #             test_position = position.copy()
    #             test_position[x, y] = -1  # Assume AI (-1) places a stone
    #             score_board[x, y] = ai.evaluate_position(test_position)

    # # Convert the score board to a string representation
    # score_board_str = ''
    # for row in score_board:
    #     score_board_str += ' '.join(f"{cell:6.1f}" for cell in row) + '\n'

    # # Save the score board to a file
    # with open('./test/score_board.txt', 'w', encoding='utf-8') as f:
    #     f.write(score_board_str)

    # print("Score visualization saved to './test/score_board.txt'")

    # Get the top 3 moves for the AI player
    start_time = time.time()
    top_moves = ai.get_top_moves(sample_board, current_player=-1, top_n=3)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.3f} seconds")

    # Create a board with markers for top moves
    marked_board = [row[:] for row in sample_board]
    markers = ['A', 'B', 'C']
    
    # Mark the top moves on the board
    for (score, (x, y)), marker in zip(top_moves, markers):
        print(f"Move {marker}: Score = {score}, Position = ({x}, {y})")
        marked_board[x][y] = marker

    # Convert the marked board to a string representation
    board_str = ''
    for row in marked_board:
        row_str = []
        for cell in row:
            if isinstance(cell, str):  # If it's a marker (A, B, C)
                row_str.append(cell)
            elif cell == 1:
                row_str.append('●')  # Black stone
            elif cell == -1:
                row_str.append('○')  # White stone
            else:
                row_str.append('·')  # Empty cell
        board_str += ' '.join(row_str) + '\n'

    # Save the marked board to a file
    with open('./test/marked_board.txt', 'w', encoding='utf-8') as f:
        f.write(board_str)

    
    
    #bestScore = ai.minimax_with_tree(sample_board, depth=3, alpha=float("-inf"), beta=float("inf"), current_player=-1)
    #print(f"Best Score: {bestScore}")
    #ai.save_tree_to_file('./test/tree_structure.txt')
    
    #print("Tree structure saved to './test/tree_structure.txt'")
