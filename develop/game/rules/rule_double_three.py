# Check if we have a consistent-three pattern
def check_consistent(stones, rows, cols, x_stone, y_stone, current_player, directions):
    opponent = -current_player
    consistent_threes = []
    seen_positions = set()  # Track positions that have already been counted

    for dx, dy in directions:
        for i in range(-2, 1):
            nx1, ny1 = y_stone + i * dy, x_stone + i * dx
            nx2, ny2 = y_stone + (i + 1) * dy, x_stone + (i + 1) * dx
            nx3, ny3 = y_stone + (i + 2) * dy, x_stone + (i + 2) * dx

            if (
                0 <= nx1 < rows and 0 <= ny1 < cols and
                0 <= nx2 < rows and 0 <= ny2 < cols and
                0 <= nx3 < rows and 0 <= ny3 < cols
            ):
                if (
                    stones[nx1][ny1] == current_player and
                    stones[nx2][ny2] == current_player and
                    stones[nx3][ny3] == current_player
                ):
                    pattern = tuple(sorted([(nx1, ny1), (nx2, ny2), (nx3, ny3)]))
                    
                    if pattern not in seen_positions:
                        consistent_threes.append(pattern)
                        seen_positions.add(pattern)

    return consistent_threes

def check_pattern(stones, rows, cols, x_stone, y_stone, current_player, directions):
    pattern_threes = []

    # Check all directions for free-three patterns
    for dx, dy in directions:
        # Check for a free-three pattern in the current direction
        for i in range(-2, 1):  # We check three consecutive positions starting from i=-2 to i=0
            nx1, ny1 = y_stone + i * dy, x_stone + i * dx
            nx2, ny2 = y_stone + (i + 1) * dy, x_stone + (i + 1) * dx
            nx3, ny3 = y_stone + (i + 2) * dy, x_stone + (i + 2) * dx

            # Check bounds
            if (
                0 <= nx1 < rows and 0 <= ny1 < cols and
                0 <= nx2 < rows and 0 <= ny2 < cols and
                0 <= nx3 < rows and 0 <= ny3 < cols
            ):
                # Check if we have a free-three pattern
                if (
                    stones[nx1][ny1] == current_player and
                    stones[nx2][ny2] == current_player and
                    stones[nx3][ny3] == 0  # Empty spot at the right end
                ):
                    # Check if placing the stone in the middle creates a valid free-three
                    middle_nx, middle_ny = y_stone + (i + 1) * dy, x_stone + (i + 1) * dx
                    if (
                        stones[middle_nx][middle_ny] == 0 and  # Empty spot
                        (middle_nx == 0 or stones[middle_nx - dy][middle_ny - dx] != -current_player) and  # Left end not blocked
                        (middle_nx == rows - 1 or stones[middle_nx + dy][middle_ny + dx] != -current_player)  # Right end not blocked
                    ):
                        pattern_threes.append(((nx1, ny1), (middle_nx, middle_ny), (nx3, ny3)))

    return pattern_threes


def check_double_three(stones, rows, cols, x_stone, y_stone, current_player):

    stones[y_stone][x_stone] = current_player

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

    # Get free-threes for the current move
    free_threes = check_pattern(stones, rows, cols, x_stone, y_stone, current_player, directions)
    print("Pattern fit: ", free_threes)

    if len(free_threes) >= 2:
        print("Double-three detected!")
        stones[y_stone][x_stone] = 0
        return True

    # Get consistent-threes for the current move
    consistent_threes = check_consistent(stones, rows, cols, x_stone, y_stone, current_player, directions)
    print("Consistent threes: ", consistent_threes)

    if len(free_threes) + len(consistent_threes) >= 2:
        print("Double-three detected!")
        stones[y_stone][x_stone] = 0
        return True

    stones[y_stone][x_stone] = 0
    return False
