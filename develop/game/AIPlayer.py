from game.Node import Node
import numpy as np


class AIPlayer:
    def __init__(self, depth=3):
        self.depth = depth
        self.tree = []

    def minimax_alpha_beta(self, node, depth, alpha, beta):
        """
        Minimax algorithm with alpha-beta pruning.
        """
        if depth == 0 or node.is_game_over():
            return node.evaluate_position()

        maximizing_player = node.current_player == 1

        if maximizing_player:
            max_eval = float("-inf")
            for child in node.generate_children():
                eval = self.minimax_alpha_beta(child, depth - 1, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for child in node.generate_children():
                eval = self.minimax_alpha_beta(child, depth - 1, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_top_moves(self, position, current_player, top_n=3):
        """
        Get the top N best moves for the given player.

        Args:
            position (list of list of int): The current game board.
            current_player (int): The player making the move (1 for AI, -1 for human).
            top_n (int): Number of top moves to return.

        Returns:
            list: Top N moves as (score, (x, y)).
        """

        # Create the root node with the padded board
        root_node = Node(np.array(position), current_player)

        scored_moves = []
        for child in root_node.generate_children():
            child.score = self.minimax_alpha_beta(
                child,
                self.depth,
                float("-inf"),
                float("inf"),
            )
            # Convert padded coordinates back to the original board coordinates
            scored_moves.append((child.score, (child.x, child.y)))

        scored_moves.sort(key=lambda x: x[0], reverse=True)
        return scored_moves[:top_n]
