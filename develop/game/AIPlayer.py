import time
from Node import Node
from Tree import Tree


class AIPlayer:
    def __init__(self, depth=3):
        self.depth = depth
        self.tree = []

    def minimax(self, node, depth, alpha, beta):
        """
        Minimax algorithm with alpha-beta pruning.
        """
        if depth == 0 or node.is_game_over():
            return node.evaluate_position()

        maximizing_player = node.current_player == -1

        if maximizing_player:
            max_eval = float("-inf")
            for child in node.generate_children():
                eval = self.minimax(child, depth - 1, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for child in node.generate_children():
                eval = self.minimax(child, depth - 1, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_top_moves(self, position, current_player, top_n=3):
        """
        Get the top N best moves for the given player
        """
        root_node = Node(position, current_player)
        scored_moves = []

        for child in root_node.generate_children():
            child.score = self.minimax(
                child,
                self.depth,
                float("-inf"),
                float("inf"),
            )
            scored_moves.append((child.score, (child.x, child.y)))

        scored_moves.sort(key=lambda x: x[0], reverse=True)
        return scored_moves[:top_n]


if __name__ == "__main__":

    # Read the board from file
    def load_board(filename):
        symbol_to_number = {"·": 0, "●": 1, "○": -1}
        with open(filename, "r") as f:
            return [
                [symbol_to_number[cell] for cell in line.strip().split(",")]
                for line in f
            ]

    # Load the sample board from file
    sample_board = load_board("./test/sample.txt")

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
    markers = ["①", "②", "③"]

    # Mark the top moves on the board
    for (score, (x, y)), marker in zip(top_moves, markers):
        print(f"Move {marker}: Score = {score}, Position = ({x}, {y})")
        marked_board[x][y] = marker

    # Convert the marked board to a string representation
    board_str = ""
    for row in marked_board:
        row_str = []
        for cell in row:
            if isinstance(cell, str):  # If it's a marker (A, B, C)
                row_str.append(cell)
            elif cell == 1:
                row_str.append("●")  # Black stone
            elif cell == -1:
                row_str.append("○")  # White stone
            else:
                row_str.append("·")  # Empty cell
        board_str += " ".join(row_str) + "\n"

    # Save the marked board to a file
    with open("./test/marked_board.txt", "w", encoding="utf-8") as f:
        f.write(board_str)
