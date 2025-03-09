from setting.constants import (
    DIRECTIONS_FRONT_BACK,
)
from setting.config import Config

def check_capture(stones, move,  current_player):
    y_stone, x_stone = move
    opponent = -current_player
    captured_stones = set()
    setting = Config()
    rows = setting.COL
    cols = setting.COL
    

    for dx, dy in DIRECTIONS_FRONT_BACK:
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
