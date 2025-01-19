def check_capture(stones, rows, cols, x_stone, y_stone, current_player):
    directions = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1),   # Right
        (-1, -1), # Top-left diagonal
        (1, 1),   # Bottom-right diagonal
        (-1, 1),  # Top-right diagonal
        (1, -1)   # Bottom-left diagonal
    ]
    
    opponent = -current_player
    captured_stones = set()

    for dx, dy in directions:
        # Check if the pattern fits within the board bounds
        nx1, ny1 = y_stone + dx, x_stone + dy
        nx2, ny2 = y_stone + 2 * dx, x_stone + 2 * dy
        nx3, ny3 = y_stone + 3 * dx, x_stone + 3 * dy

        if (
            0 <= nx1 < rows and 0 <= ny1 < cols and
            0 <= nx2 < rows and 0 <= ny2 < cols and
            0 <= nx3 < rows and 0 <= ny3 < cols and
            stones[nx1][ny1] == opponent and
            stones[nx2][ny2] == opponent and
            stones[nx3][ny3] == current_player
        ):
            captured_stones.update([(nx1, ny1), (nx2, ny2)])

    return list(captured_stones)
