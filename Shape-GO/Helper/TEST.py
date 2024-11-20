import numpy as np

from GO.Model.Goban import Goban

if __name__ == "__main__":
    board_size = 19
    goban = Goban(board_size=board_size, hc=4)
    goban.start_game()

    test_shape = np.identity(3, dtype=int)

    print(test_shape)

    for i in range(board_size):
        for j in range(board_size):
            if not goban._fits_shape_in_goban(test_shape, i, j):
                print(f"Fail @ {i} {j}")
