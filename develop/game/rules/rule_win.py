def has_continuous_sequence(line):
    count = 0
    last_value = None
    for value in line:
        if value == last_value and value != 0:
            count += 1
        else:
            count = 1
            last_value = value
        if count >= 5:
            return True
    return False

def check_win(_stones, rows, cols):
    result = False

    # Horizontal check
    for i in range(rows):
        row = [ _stones[i][j] for j in range(cols)]
        if has_continuous_sequence(row):
            result = True
            return result

    # Vertical check
    for j in range(cols):
        column = [ _stones[i][j] for i in range(rows)]
        if has_continuous_sequence(column):
            result = True
            return result

    # Diagonal check (left to right)
    for i in range(rows - 4):  # Updated to ensure 5 cells in diagonals
        for j in range(cols - 4):
            diagonal = [ _stones[i + k][j + k] for k in range(5)]
            if has_continuous_sequence(diagonal):
                result = True
                return result

    # Diagonal check (right to left)
    for i in range(rows - 4):  # Updated to ensure 5 cells in diagonals
        for j in range(4, cols):  # Start from column 4 to ensure bounds
            diagonal = [ _stones[i + k][j - k] for k in range(5)]
            if has_continuous_sequence(diagonal):
                result = True
                return result

    return result
