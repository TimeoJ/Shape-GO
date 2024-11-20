import csv
import logging

import matplotlib

from GO.Controller.Controller import Controller
from GO.Helper.Shape import Shape
from GO.Model.Goban import Goban
from GO.View.Goban_View import GobanView

from numpy import array, array_equal, fliplr

if __name__ == "__main__":
    # PyCharm feature :)
    matplotlib.use("TkAgg")

    logging.basicConfig(level=logging.INFO)

    # Add all the shapes from the csv file
    shapes = []
    with (open("Helper/shapes.csv", newline="") as csvfile):
        spamreader = csv.reader(csvfile, delimiter=':')
        for row in spamreader:
            for i in range(2):
                straight = array(eval(row[1]))
                if len(straight.shape) == 1:
                    straight = straight.reshape(1, -1)
                shapes.append(Shape(row[0], straight))
                flipped = fliplr(straight)
                if not array_equal(flipped, row[1]):
                    shapes.append(Shape(row[0], flipped))

    ### MODEL ###
    # create the first empty goban or if wanted start with handicap
    # hc = input("Select amount of handicap stones for black: ")
    goban = Goban()  # int(hc)
    goban.start_game()

    ### CONTORLLER ###
    go_controller = Controller(goban, None, shapes=shapes)

    ### VIEW ###
    go_view = GobanView(go_controller, start_goban=goban.goban, board_size=19)

    go_controller.setView(go_view)

    go_controller.on_start()
