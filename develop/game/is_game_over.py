def is_game_over(position):
    # 勝利条件: 5つ連続している石をチェック
    for x in range(len(position)):
        for y in range(len(position[0])):
            if check_five_in_a_row(position, x, y):
                return True

    # 引き分け条件: 空きマスがない場合
    if all(cell != 0 for row in position for cell in row):
        return True

    return False


def check_five_in_a_row(position, x, y):
    """現在の座標 (x, y) を起点にして5つ連続をチェック"""
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 横, 縦, 斜め (右下), 斜め (左下)
    for dx, dy in directions:
        count = 0
        for i in range(5):  # 5マス先までチェック
            nx, ny = x + i * dx, y + i * dy
            if 0 <= nx < len(position) and 0 <= ny < len(position[0]) and position[nx][ny] == position[x][y]:
                count += 1
            else:
                break
        if count == 5:
            return True
    return False
