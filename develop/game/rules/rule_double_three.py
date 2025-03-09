from setting.constants import (
    DIRECTIONS_FRONT_BACK,
    EMPTY,
)
from setting.config import Config

def check_double_three(stones, move, current_player):

    if move is None:
        return False

    def in_bounds(r, c):
        return 0 <= r < setting.COL and 0 <= c < setting.COL

    setting = Config()
    new_row, new_col = move
    stone = current_player
    open_rows = 0

    for dx, dy in DIRECTIONS_FRONT_BACK:
        count = 1
        x, y = new_row, new_col
        while True:
            x += dx
            y += dy
            if not in_bounds(x, y):
                break
            if stones[x][y] == stone:
                count += 1
            elif stones[x][y] == EMPTY:
                continue
            else:
                break
        if count == 3:
            open_rows += 1
    return open_rows == 2
