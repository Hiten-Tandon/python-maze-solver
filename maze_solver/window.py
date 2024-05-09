from collections.abc import Callable
from tkinter import Tk, Canvas, Button, PanedWindow, VERTICAL
from tkinter.ttk import *
from tkinter.constants import BOTH, HORIZONTAL
from geometry import *
from maze import Maze


class MazeWindow:
    __width: float
    __height: float
    __root: Tk
    __canvas: Canvas
    __is_active: bool
    __maze: Maze

    def __init__(
        self,
        row_count: int,
        col_count: int,
        row_size: float,
        col_size: float,
        **padding: float
    ):
        self.__width = (
            col_count * col_size + padding.get("left", 0.0) + padding.get("right", 0.0)
        )
        self.__height = (
            row_count * row_size + padding.get("top", 0.0) + padding.get("bottom", 0.0)
        )
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__master_pane = PanedWindow(self.__root, orient=HORIZONTAL)
        self.__master_pane.pack(fill=BOTH, expand=True)
        self.__canvas = Canvas(
            self.__master_pane,
            width=self.__width,
            height=self.__height,
        )
        self.__master_pane.add(self.__canvas)
        self.__is_active = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__maze = Maze(row_count, col_count, row_size, col_size, **padding)
        self.__maze.draw(self.__canvas)

        self.__button_pane = PanedWindow(self.__master_pane, orient=VERTICAL)
        self.__master_pane.add(self.__button_pane)

        def reset_canvas():
            self.__canvas.delete("all")
            self.__maze.draw(self.__canvas)

        def create_maze():
            self.__maze = Maze(row_count, col_count, row_size, col_size, **padding)

        self.__buttons = [
            Button(
                self.__button_pane,
                text="DFS",
                command=lambda: (
                    reset_canvas(),
                    disable_buttons(),
                    self.__maze.animate_dfs(self.__canvas, self.redraw),
                    enable_buttons(),
                ),
            ),
            Button(
                self.__button_pane,
                text="BFS",
                command=lambda: (
                    reset_canvas(),
                    disable_buttons(),
                    self.__maze.animate_bfs(self.__canvas, self.redraw),
                    enable_buttons(),
                ),
            ),
            Button(
                self.__button_pane,
                text="Greedy Best First",
                command=lambda: (
                    reset_canvas(),
                    disable_buttons(),
                    self.__maze.animate_gbfs(self.__canvas, self.redraw),
                    enable_buttons(),
                ),
            ),
            Button(
                self.__button_pane,
                text="A*",
                command=lambda: (
                    reset_canvas(),
                    disable_buttons(),
                    self.__maze.animate_astar(self.__canvas, self.redraw),
                    enable_buttons(),
                ),
            ),
            Button(
                self.__button_pane,
                text="Reset",
                command=lambda: (create_maze(), reset_canvas()),
            ),
        ]

        def disable_buttons():
            for b in self.__buttons:
                b.configure(state="disabled")

        def enable_buttons():
            for b in self.__buttons:
                b.configure(state="normal")

        for b in self.__buttons:
            b.pack()

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def close(self):
        self.__is_active = False

    def wait_for_close(self):
        self.__is_active = True
        while self.__is_active:
            self.redraw()
