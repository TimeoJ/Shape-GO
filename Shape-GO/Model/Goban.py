import logging

import numpy as np
from scipy.ndimage import label


class Goban:
    hc_array = [[3, 3], [15, 15], [3, 15], [15, 3], [9, 9], [3, 9], [15, 9], [9, 3], [9, 15]]
    max_hc = 10
    max_group_size = 19 * 19

    def __init__(self, board_size=19, hc=0):
        self.visited = None
        self.board_size = board_size
        self.goban = np.zeros((board_size + 4, board_size + 4), dtype=int)
        for i in range(board_size, board_size + 4):
            self.goban[i, :] = 1000
            self.goban[:, i] = 1000
        self.hc = hc

    def start_game(self):
        if self.hc > self.max_hc:
            self.hc = 9
            logging.info("Maximum handicap of 9 is allowed")
            logging.info("handicap set to 9!")

        for i in range(self.hc):
            self.goban[self.hc_array[i][0]][self.hc_array[i][1]] = 1

    @property
    def hc(self):
        return self._hc

    @hc.setter
    def hc(self, value):
        if value > 10:
            logging.info("handicap set to 9")
            self._hc = 9
        else:
            self._hc = value

    def fits_shape_in_goban(self, shape: np.ndarray, x: int, y: int):
        # shape is maximum a 2D array
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] != 0:
                    if self.goban[x + j][y - i] == 0:
                        continue
                    else:
                        return False  # Shape doesn't fit
        return True  # Shape fits

    def place_shape(self, shape: np.array, x_offset: int, y_offset: int, curr_player: int):
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i, j]:
                    self.goban[x_offset + j][y_offset - i] = curr_player

    def _find_groups(self, val):
        ## FLOOD FILL ALGORITHM
        groups = []

        struct = np.array([[0, 1, 0],
                           [1, 1, 1],
                           [0, 1, 0]])
        labeled_array, num_feat = label(self.goban == val, structure=struct)
        self.visited = np.zeros((self.board_size, self.board_size), dtype=bool)

        for label_num in range(1, num_feat + 1):
            group_coords = np.argwhere(labeled_array == label_num)
            groups.append(group_coords.tolist())

        return groups

    def _color_cap(self, groups, own_val):
        cap = False
        for group in groups:
            # check the neighbours of the opposite group and see if it is surrounded by your stones
            if self.check_neighbours(group, val=own_val):
                for (x, y) in group:
                    self.goban[x, y] = 0  # remove the stones
                cap = True
        return cap

    def captured(self, curr_player: int):
        # get neighbours of the x and y stones
        black_groups = self._find_groups(1)
        white_groups = self._find_groups(2)

        if curr_player == 1:  # Blacks turn
            self._color_cap(white_groups, own_val=curr_player)
            if self._color_cap(black_groups, own_val=2):
                return False
            else:
                return True

        if curr_player == 2:  # Whites turn
            self._color_cap(black_groups, own_val=curr_player)
            if self._color_cap(white_groups, own_val=1):
                return False
            else:
                return True

    def check_neighbours(self, coords, val):

        coord_set = set((x, y) for x, y in coords)

        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for x, y in coords:  # gets all coordinates of the group
            for dx, dy in dirs:  # go in every direction
                idx_x, idx_y = x + dx, y + dy  # calc the new indexes
                if 0 <= idx_x < self.board_size and 0 <= idx_y < self.board_size:  # check that new idx is in bounds
                    if (idx_x, idx_y) not in coord_set and self.goban[idx_x, idx_y] != val:
                        return False
        return True

    def remove_shape(self, shape: np.array, x_offset: int, y_offset: int):
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i, j]:
                    self.goban[x_offset + j][y_offset - i] = 0


def test_goban():
    return np.array([[1, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 2, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [2, 2, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])


if __name__ == '__main__':
    # Testing Controller class
    goban = Goban()
    goban.start_game()
    goban.goban = test_goban()
