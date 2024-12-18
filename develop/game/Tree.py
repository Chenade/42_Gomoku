from game.Node import Node


class Tree:
    def __init__(self, root=None):
        """
        Represents the game tree.

        Args:
            root (Node, optional): The root node of the tree. Defaults to None.
        """
        self.root = root  # Root node of the tree

    def add_node(self, parent, position, current_player, x, y):
        """
        Add a new node as a child of the parent node.

        Args:
            parent (Node): The parent node.
            position (list[list[int]]): The board state for the new node.
            current_player (int): The player for this node.
            x (int): X-coordinate of the move.
            y (int): Y-coordinate of the move.

        Returns:
            Node: The newly created node.
        """
        new_node = Node(
            position, current_player, newStoneX=x, newStoneY=y, parent=parent
        )
        parent.add_child(new_node)
        return new_node

    def save_tree_to_file(self, filename):
        """Save the tree structure to a file."""
        with open(filename, "w", encoding="utf-8") as f:
            self._save_node_to_file(f, self.root, level=0)

    def _save_node_to_file(self, file, node, level):
        """
        Recursively save nodes to file for visualization.

        Args:
            file: File object to write the tree.
            node: Current node.
            level: Depth level of the node.
        """
        if node is not None:
            indent = "  " * level
            file.write(
                f"{indent}Node(Player={node.current_player}, Move=({node.newStoneX}, {node.newStoneY}), Score={node.score})\n"
            )
            for child in node.children:
                self._save_node_to_file(file, child, level + 1)
