from tkinter import Canvas
from typing import Self


class Point:
    x: float
    y: float

    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y


class Line:
    __start: Point
    __end: Point

    def __init__(self, start: Point, end: Point):
        self.__start = start
        self.__end = end

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.__start.x,
            self.__start.y,
            self.__end.x,
            self.__end.y,
            fill=fill_color,
            width=2,
        )


class Cell:
    __walls: list[Line]
    connections: list[tuple[int, int]]
    __corners: tuple[Point, Point, Point, Point]
    __top_left: int = 0
    __top_right: int = 1
    __bottom_left: int = 2
    __bottom_right: int = 3

    def __init__(
        self, top_left_corner: Point, bottom_right_corner: Point, **kwargs: bool
    ):
        self.connections = []
        self.__walls = []
        self.__corners = (
            top_left_corner,
            Point(bottom_right_corner.x, top_left_corner.y),
            Point(top_left_corner.x, bottom_right_corner.y),
            bottom_right_corner,
        )

        if kwargs.get("left", True):
            self.__walls.append(
                Line(
                    self.__corners[self.__top_left], self.__corners[self.__bottom_left]
                )
            )
        else:
            self.connections.append((0, -1))
        if kwargs.get("right", True):
            self.__walls.append(
                Line(
                    self.__corners[self.__top_right],
                    self.__corners[self.__bottom_right],
                )
            )
        else:
            self.connections.append((0, 1))
        if kwargs.get("top", True):
            self.__walls.append(
                Line(self.__corners[self.__top_left], self.__corners[self.__top_right])
            )
        else:
            self.connections.append((-1, 0))
        if kwargs.get("bottom", True):
            self.__walls.append(
                Line(
                    self.__corners[self.__bottom_left],
                    self.__corners[self.__bottom_right],
                )
            )
        else:
            self.connections.append((1, 0))

    def draw(self, canvas: Canvas, fill_color: str):
        for wall in self.__walls:
            wall.draw(canvas, fill_color)

    def __get_center(self) -> Point:
        return Point(
            (self.__corners[self.__top_left].x + self.__corners[self.__top_right].x)
            / 2,
            (self.__corners[self.__top_left].y + self.__corners[self.__bottom_left].y)
            / 2,
        )

    def draw_move(self, to_cell: Self, canvas: Canvas, final: bool = False):
        move: Line = Line(self.__get_center(), to_cell.__get_center())
        move.draw(canvas, "red" if final else "cyan")
