from game.ai.Node import Node
from .Node import Node
from setting.constants import BLACK, WHITE


class AIPlayer:
    def __init__(self, depth=3, setting=None):
        self.depth = depth - 1
        self.setting = setting

    def minimax_alpha_beta(self, node, depth, alpha, beta):
        """
        Minimax algorithm with alpha-beta pruning.
        """
        if depth == 0 or node.is_game_over():
            return node.score

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

    def minimax_a_b_pruning(
        self, node, depth, maximizing_player, alpha=float("-inf"), beta=float("inf")
    ):
        """
        Perform the minimax search with alpha-beta pruning.

        Args:
            node (Node): The current game state.
            depth (int): The depth to search.
            maximizing_player (bool): True if the current search level is the maximizing player (AI, WHITE),
                                    else False (opponent, BLACK).
            alpha (float): The current alpha value.
            beta (float): The current beta value.

        Returns:
            tuple: (score, best_node) where score is the heuristic evaluation and best_node is the best child Node.
        """
        # もし葉なら（深さ0、終局、もしくは禁止手の場合）、評価値を返す
        if depth == 0 or node.is_terminal or node.is_forbidden_move:
            return node.get_heuristic_score(), node

        if maximizing_player:
            max_eval = float("-inf")
            best_move = None
            for child in node.generate_child_nodes():
                eval, _ = self.minimax_a_b_pruning(child, depth - 1, False, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    best_move = child
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # beta cut-off
            return max_eval, best_move
        else:
            min_eval = float("inf")
            best_move = None
            for child in node.generate_child_nodes():
                eval, _ = self.minimax_a_b_pruning(child, depth - 1, True, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    best_move = child
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # alpha cut-off
            return min_eval, best_move

    def initiate_minimax(self, node, depth):
        """
        Generate all possible moves from the current node and evaluate them with minimax,
        then return the top_n moves sorted by descending heuristic score.

        Args:
            node (Node): The current game state.
            depth (int): The search depth for minimax (should be >= 1).
            top_n (int): Number of top moves to return.

        Returns:
            list of tuples: Each tuple is (score, child_node).
        """
        moves_scores = []
        # Generate candidate moves. Note: next move is AI (WHITE) since current node stone_type is BLACK.
        for child in node.generate_child_nodes():
            # For each candidate move, evaluate with minimax (depth-1, opponent's turn)
            score, _ = self.minimax_a_b_pruning(
                child, depth - 1, False, alpha=float("-inf"), beta=float("inf")
            )
            moves_scores.append((score, child))

        return moves_scores


    def get_top_moves(self, position, current_player, top_n=3):
        """
        Generate all possible moves from the current node and evaluate them with minimax,
        then return the top_n moves sorted by descending heuristic score.

        Args:
            position (list of list of int): The current game board.
            current_player (int): The player making the move (1 for AI, -1 for human).
            top_n (int): Number of top moves to return.

        Returns:
            list of tuples: Each tuple is (score, (x, y)) where (x, y) are the move coordinates.
        """
        # Determine the last stone type based on the current player
        if current_player == 1:
            last_stone = BLACK
        elif current_player == -1:
            last_stone = WHITE
        else:
            raise ValueError("current_player must be either 1 (white) or -1 (black)")

        # Create the root node
        node = Node(
            board=position,
            move=None,
            stone_type=last_stone,
            depth=0,
            setting=self.setting,
        )
        
        # Generate all possible moves and evaluate with minimax
        next_moves = self.initiate_minimax(node, depth=self.depth)
        
        # Sort moves by score in descending order (higher is better for maximizing player)
        if current_player == 1:
            next_moves.sort(key=lambda x: x[0], reverse=True)
        else:
            next_moves.sort(key=lambda x: x[0], reverse=False)

        # take top_n moves
        top_moves = next_moves[:top_n]

        # return list of (score, move) tuples
        return [(score, child.move) for score, child in top_moves]
