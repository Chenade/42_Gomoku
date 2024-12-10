def evaluate_position(position):
    score = 0

    # 勝利に近い状態を評価
    for x in range(len(position)):
        for y in range(len(position[0])):
            if position[x][y] == 1:  # 黒石
                score += evaluate_cell(position, x, y, 1)
            elif position[x][y] == -1:  # 白石
                score -= evaluate_cell(position, x, y, -1)

    return score


def evaluate_cell(position, x, y, player):
    """指定したマスのスコアを計算"""
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 横, 縦, 斜め
    score = 0

    for dx, dy in directions:
        count = 0
        for i in range(5):  # 最大5つ先までチェック
            nx, ny = x + i * dx, y + i * dy
            if 0 <= nx < len(position) and 0 <= ny < len(position[0]) and position[nx][ny] == player:
                count += 1
            else:
                break
        if count > 0:
            score += 10 ** count  # 連続数に応じて指数的にスコアを加算

    return score
