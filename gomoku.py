from Game import Game


def main():
    g = Game()
    g.print_board()
    g.place_stone(9, 9, 1)
    print("------------------------------------")
    g.print_board()
    result = g.place_stone(9, 9, 1)
    print("Stone placed successfully?", result)
    print("------------------------------------")
    g.place_stone(8, 8, 1)
    g.place_stone(8, 9, 1)
    g.place_stone(8, 10, 1)
    g.place_stone(8, 11, 1)
    g.place_stone(8, 12, 1)
    g.print_board()
    print("Player1 is win?", g.check_win(1))


if __name__ == "__main__":
    main()
