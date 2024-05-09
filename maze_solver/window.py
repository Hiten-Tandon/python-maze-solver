from tkinter import Tk, Canvas, Button, PanedWindow, VERTICAL, StringVar
from tkinter.font import Font
from tkinter.ttk import Button, Label, PanedWindow, Style
from tkinter.constants import BOTH, HORIZONTAL
from geometry import *
from maze import Maze

dfs_description = """
DFS or Depth-First Search is a path finding algorithm that basically explores one direction till it can't anymore.
When it can't travel in the same direction anymore, it goes to last cell which has more choices and picks one direction from there.
Then it explores that direction till it can't anymore.

This process goes on until either the maze is solved or it runs out of options.
"""


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
        master_pane = PanedWindow(self.__root, orient=HORIZONTAL)
        master_pane.pack(fill=BOTH, expand=True)
        self.__canvas = Canvas(
            master_pane, width=self.__width, height=self.__height, bg="#2e2e2e", bd=0
        )
        master_pane.add(self.__canvas)
        self.__is_active = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__maze = Maze(row_count, col_count, row_size, col_size, **padding)
        self.__maze.draw(self.__canvas)

        button_pane = PanedWindow(master_pane, orient=VERTICAL)
        master_pane.add(button_pane)

        def reset_canvas():
            self.__canvas.delete("all")
            self.__maze.draw(self.__canvas)

        def create_maze():
            self.__maze = Maze(row_count, col_count, row_size, col_size, **padding)

        t = Label(
            button_pane,
            text=dfs_description,
            foreground="white",
            state="readonly",
            borderwidth=2.0,
        )

        buttons = [
            Button(
                button_pane,
                text="DFS",
                command=lambda: (
                    reset_canvas(),
                    disable_buttons(),
                    self.__maze.animate_dfs(self.__canvas, self.redraw),
                    enable_buttons(),
                ),
            ),
            Button(
                button_pane,
                text="BFS",
                command=lambda: (
                    reset_canvas(),
                    disable_buttons(),
                    self.__maze.animate_bfs(self.__canvas, self.redraw),
                    enable_buttons(),
                ),
            ),
            Button(
                button_pane,
                text="Greedy Best First",
                command=lambda: (
                    reset_canvas(),
                    disable_buttons(),
                    self.__maze.animate_gbfs(self.__canvas, self.redraw),
                    enable_buttons(),
                ),
            ),
            Button(
                button_pane,
                text="A*",
                command=lambda: (
                    reset_canvas(),
                    disable_buttons(),
                    self.__maze.animate_astar(self.__canvas, self.redraw),
                    enable_buttons(),
                ),
            ),
            Button(
                button_pane,
                text="Reset",
                command=lambda: (create_maze(), reset_canvas()),
                padding={"top": 50, "left": 50},
            ),
        ]

        def disable_buttons():
            for b in buttons:
                b.configure(state="disabled")

        def enable_buttons():
            for b in buttons:
                b.configure(state="normal")

        for b in buttons:
            b.pack(padx=10, pady=10, anchor="center")

        s = Style(self.__root)
        s.configure(
            ".",
            foreground=[("!disabled", "white"), ("disabled", "grey")],
            background=[("!disabled", "#7e7e7e"), ("disabled", "#7e7e7e")],
            font=Font(family="JetBrains Mono NF", size=12),
        )
        s.map("TLabel", foreground=[("!disabled", "white"), ("disabled", "grey")])
        s.map(
            "TButton",
            foreground=[("!disabled", "white"), ("disabled", "grey")],
            background=[("!disabled", "purple"), ("disabled", "purple")],
            borderwidth=[("!disabled", 0), ("disabled", 0)],
        )

        t.pack(padx=10, pady=10, fill=BOTH)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def close(self):
        self.__is_active = False

    def wait_for_close(self):
        self.__is_active = True
        while self.__is_active:
            self.redraw()
