from time import sleep

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button
from math import floor

class GobanView:

    def __init__(self, controller, start_goban: np.array, board_size=19):
        # List to store references to the circles (stones)
        self.preview_stones = []
        self.fix_stones = []
        self.goban = start_goban
        self.controller = controller
        self.board_size = board_size

        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        plt.subplots_adjust(bottom=0.15)

        # axis
        self.ax.set_aspect('equal')
        self.ax.set_xlim(0, board_size - 1)
        self.ax.set_ylim(0, board_size - 1)

        # background
        self._draw_init(start_goban)

        # Register mouse listener
        self.fig.canvas.mpl_connect("button_press_event", self._on_click)
        self.fig.canvas.mpl_connect("motion_notify_event", self._on_mouse)

        self.ax.axis('off')

    def _on_click(self, event):
        (xm, ym), (xM, yM) = self.btn_gen_shape.label.clipbox.get_points()
        if xm < event.x < xM and ym < event.y < yM:
            return
        (xm, ym), (xM, yM) = self.btn_rot_shape.label.clipbox.get_points()
        if xm < event.x < xM and ym < event.y < yM:
            return
        if event.inaxes is not None:
            x, y = int(round(event.xdata)), int(round(event.ydata))
            self.controller.on_place(x, y)

    def _on_mouse(self, event):
        (xm, ym), (xM, yM) = self.btn_gen_shape.label.clipbox.get_points()
        if xm < event.x < xM and ym < event.y < yM:
            return
        (xm, ym), (xM, yM) = self.btn_rot_shape.label.clipbox.get_points()
        if xm < event.x < xM and ym < event.y < yM:
            return
        if event.inaxes is not None:
            x, y = int(round(event.xdata)), abs(int(round(event.ydata)))
            self.controller.preview(x, y)

    def _draw_init(self, start_goban):
        # Board lines
        for i in range(self.board_size):
            self.ax.plot([i, i], [0, self.board_size - 1], color="black")
            self.ax.plot([0, self.board_size - 1], [i, i], color="black")
        # Draw handicap stones
        self.draw_goban(start_goban)
        # place buttons and preview window of the shape
        ax_button = plt.axes((0.05, 0.9, 0.2, 0.075))  # Position for top-left corner
        self.btn_gen_shape = Button(ax_button, "Generate")
        self.btn_gen_shape.on_clicked(self._generate_shape)

        ax_button = plt.axes((0.7, 0.9, 0.2, 0.075))  # Position for top-right corner
        self.btn_rot_shape = Button(ax_button, "Rotate")
        self.btn_rot_shape.on_clicked(self._rotate)

        self.text_shape_name = self.ax.text(7, 19, "What will be your shape?", ha="center", fontsize=12, color="black",
                                            bbox=dict(facecolor="lightgray", edgecolor="black",
                                                      boxstyle="round,pad=0.5"))

    def draw_stone(self, x: int, y: int, color: int):
        # print(f"Drawing a {color} stone @ X:{x} Y:{y}")
        if color:
            self.ax.add_patch(plt.Circle((x, abs(self.board_size - y - 1)), 0.4, color='red'))
        else:
            self.ax.add_patch(plt.Circle((x, abs(self.board_size - y - 1)), 0.4, color='blue'))
        self.update()

    def draw_goban(self, goban: np.ndarray):

        if len(self.fix_stones):
            for stone in self.fix_stones:
                stone.remove()
            self.fix_stones = []

        for i in range(self.board_size):
            for j in range(self.board_size):
                if goban[i, j] == 1:
                    # self.stones.append()
                    self.fix_stones.append(plt.Circle((i, j), 0.4, color='red'))
                if goban[i, j] == 2:
                    # self.stones.append((i, j))
                    self.fix_stones.append(plt.Circle((i, j), 0.4, color='blue'))

        for stone in self.fix_stones:
            self.ax.add_patch(stone)
        self.update()

    def preview_stone(self, x: int, y: int, color: int):
        # print(f"Previewing a {color} stone @ X:{x} Y:{y}")
        plot_y = abs(self.board_size - y - 1)

        if len(self.preview_stones):
            self.preview_stones[0].remove()
            self.preview_stones = []

        circle_color = 'red' if color == 1 else 'blue'
        self.preview_stones.append(plt.Circle((x, plot_y), 0.4, color=circle_color))
        self.ax.add_patch(self.preview_stones[0])
        self.update()

    def preview_shape(self, shape: np.ndarray, start_x: int, start_y: int, color: int):

        row, col = shape.shape  # unfortunate naming...

        if len(self.preview_stones):
            for circle in self.preview_stones:
                circle.remove()  # or set visible?
                self.preview_stones = []

        circle_color = 'red' if color == 1 else 'blue'
        for i in range(row):
            for j in range(col):
                if shape[i, j] != 0:
                    self.preview_stones.append(plt.Circle((start_x + j, start_y - i), 0.4, color=circle_color))

        for circle in self.preview_stones:
            self.ax.add_patch(circle)
        self.update()

    def _generate_shape(self, event):
        self.text_shape_name.set_text("Loading ...")
        self.update()
        sleep(0.5)
        self.controller.on_generate()

    def _rotate(self, event):
        self.controller.on_rotate()

    def update_text(self, shape_name: str):
        self.text_shape_name.set_text("it's a: " + shape_name)
        self.update()

    def update(self):
        plt.draw()

    def start(self):
        plt.show()
