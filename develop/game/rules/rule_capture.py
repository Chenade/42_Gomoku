
        capture = check_capture(self._stones, self.COL, self.COL, x_stone, y_stone, (-1 if self.play_order else 1))
        print(capture)
        
# def check_capture(stones, rows, cols, x_stone, y_stone, current_player):
#     """
#     Checks for captures after placing a stone at (x_stone, y_stone).
#     Returns a list of captured stones as tuples [(x1, y1), (x2, y2)].
#     """
#     print(f"Checking for captures at ({x_stone}, {y_stone})")
#     directions = [
#         (-1, 0),  # Up
#         (1, 0),   # Down
#         (0, -1),  # Left
#         (0, 1),   # Right
#         (-1, -1), # Top-left diagonal
#         (1, 1),   # Bottom-right diagonal
#         (-1, 1),  # Top-right diagonal
#         (1, -1)   # Bottom-left diagonal
#     ]
    
#     opponent = -current_player
#     captured_stones = set()

#     for dx, dy in directions:
#         # Check if the pattern fits within the board bounds
#         nx1, ny1 = x_stone + dx, y_stone + dy
#         nx2, ny2 = x_stone + 2 * dx, y_stone + 2 * dy
#         nx3, ny3 = x_stone + 3 * dx, y_stone + 3 * dy

#         if (
#             0 <= nx1 < rows and 0 <= ny1 < cols and
#             0 <= nx2 < rows and 0 <= ny2 < cols and
#             0 <= nx3 < rows and 0 <= ny3 < cols and
#             stones[nx1][ny1] == opponent and
#             stones[nx2][ny2] == opponent and
#             stones[nx3][ny3] == current_player
#         ):
#             captured_stones.update([(nx1, ny1), (nx2, ny2)])

#     return list(captured_stones)

def check_capture(stones, rows, cols, x, y, player):
# def capture_stones(stones, x, y, player):
    opponent = -player
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    captured = []

    def find_group_and_liberties(start_x, start_y):
        group = []
        liberties = []
        stack = [(start_x, start_y)]
        visited = set()
        
        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            group.append((cx, cy))
            
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < len(stones) and 0 <= ny < len(stones[0]):
                    if stones[nx][ny] == 0:
                        liberties.append((nx, ny))
                    elif stones[nx][ny] == stones[start_x][start_y]:
                        stack.append((nx, ny))
        
        return group, liberties

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(stones) and 0 <= ny < len(stones[0]) and stones[nx][ny] == opponent:
            group, liberties = find_group_and_liberties(nx, ny)
            if not liberties:
                captured.extend(group)
    
    # Remove captured stones
    # for cx, cy in captured:
        # stones[cx][cy] = 0
    
    return captured
