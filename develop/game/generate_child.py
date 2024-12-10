def generate_children(position):
    children = []

    # 空いているマスに石を置く
    for x in range(len(position)):
        for y in range(len(position[0])):
            if position[x][y] == 0:  # 空きマス
                new_position = [row[:] for row in position]  # 現在の盤面をコピー
                new_position[x][y] = 1  # 仮に黒石を置く
                children.append(new_position)

    return children
