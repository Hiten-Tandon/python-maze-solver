import heapq
from typing import Callable
from geometry import *
from collections import deque
import random


class Maze:
    __matrix: list[list[Cell]]
    __start: tuple[int, int]
    __end: tuple[int, int]

    def __init__(
        self,
        row_count: int,
        col_count: int,
        row_width: float,
        col_width: float,
        **padding: float
    ):
        self.__matrix = [[] for _ in range(row_count)]

        start_row, start_col = random.choice(
            [(r, 0) for r in range(1, row_count - 1)]
            + [(0, c) for c in range(1, col_count - 1)]
        )
        end_row, end_col = random.choice(
            [(r, col_count - 1) for r in range(1, row_count - 1)]
            + [(row_count - 1, c) for c in range(1, col_count - 1)]
        )
        self.__start = start_row, start_col
        self.__end = end_row, end_col

        top_factors = [True] * col_count
        for row in range(row_count):
            left_factor = True
            for col in range(col_count):
                top_left = Point(
                    col * col_width + padding.get("left", 0),
                    row * row_width + padding.get("top", 0),
                )
                bottom_right = Point(top_left.x + col_width, top_left.y + row_width)
                bottom_factor = random.random()
                right_factor = random.random()
                self.__matrix[row].append(
                    Cell(
                        top_left,
                        bottom_right,
                        left=left_factor,
                        right=(right_factor > 0.5625 or col == col_count - 1),
                        top=top_factors[col],
                        bottom=(bottom_factor > 0.5625 or row == row_count - 1),
                    )
                )
                top_factors[col] = bottom_factor > 0.5625
                left_factor = right_factor > 0.5625

    def __animate_solution(self, canvas: Canvas, path: list[tuple[int, int]]):
        r, c = path.pop()

        while len(path) != 0:
            nr, nc = path.pop()
            self.__matrix[r][c].draw_move(self.__matrix[nr][nc], canvas, final=True)
            r, c = nr, nc

    def animate_dfs(self, canvas: Canvas, fn: Callable):
        frontier = [(self.__start, [])]
        vis = [[False] * len(self.__matrix[0]) for _ in self.__matrix]
        alt = []

        while len(frontier) != 0:
            pos, path = frontier.pop()
            if pos in path or vis[pos[0]][pos[1]]:
                continue

            path.append(pos)
            if pos == self.__end:
                self.__animate_solution(canvas, path)
                fn()
                return
            row, col = pos

            vis[row][col] = True
            if len(self.__matrix[row][col].connections) == 0:
                alt.append(path)
            for dr, dc in self.__matrix[row][col].connections:
                if row + dr < 0 or col + dc < 0:
                    continue
                self.__matrix[row][col].draw_move(
                    self.__matrix[row + dr][col + dc], canvas
                )
                frontier.append(((row + dr, col + dc), [(a, b) for a, b in path]))
            fn()

        for path in alt:
            self.__animate_solution(canvas, path)

    def animate_bfs(self, canvas: Canvas, fn: Callable):
        frontier = deque([(self.__start, [])])
        vis = [[False] * len(self.__matrix[0]) for _ in self.__matrix]
        alt = []

        while len(frontier) != 0:
            pos, path = frontier.popleft()
            if pos in path or vis[pos[0]][pos[1]]:
                continue

            path.append(pos)
            if pos == self.__end:
                self.__animate_solution(canvas, path)
                fn()
                return
            row, col = pos

            vis[row][col] = True
            if len(self.__matrix[row][col].connections) == 0:
                alt.append(path)
            for dr, dc in self.__matrix[row][col].connections:
                if row + dr < 0 or col + dc < 0:
                    continue
                self.__matrix[row][col].draw_move(
                    self.__matrix[row + dr][col + dc], canvas
                )
                frontier.append(((row + dr, col + dc), [(a, b) for a, b in path]))
            fn()

        for path in alt:
            self.__animate_solution(canvas, path)

    def animate_gbfs(self, canvas: Canvas, fn: Callable):
        frontier = [
            (
                abs(self.__start[0] - self.__end[0])
                + abs(self.__start[1] - self.__end[1]),
                self.__start,
                [],
            )
        ]
        vis = [[False] * len(self.__matrix[0]) for _ in self.__matrix]
        alt = []

        while len(frontier) != 0:
            _, pos, path = heapq.heappop(frontier)
            if pos in path or vis[pos[0]][pos[1]]:
                continue

            path.append(pos)
            if pos == self.__end:
                self.__animate_solution(canvas, path)
                fn()
                return
            row, col = pos

            vis[row][col] = True
            if len(self.__matrix[row][col].connections) == 0:
                alt.append(path)
            for dr, dc in self.__matrix[row][col].connections:
                if row + dr < 0 or col + dc < 0:
                    continue
                self.__matrix[row][col].draw_move(
                    self.__matrix[row + dr][col + dc], canvas
                )
                heapq.heappush(
                    frontier,
                    (
                        abs(row - self.__end[0]) + abs(col - self.__end[1]),
                        (row + dr, col + dc),
                        [(a, b) for a, b in path],
                    ),
                )
            fn()

        for path in alt:
            self.__animate_solution(canvas, path)

    def animate_astar(self, canvas: Canvas, fn: Callable):
        frontier = [
            (
                abs(self.__start[0] - self.__end[0])
                + abs(self.__start[1] - self.__end[1]),
                self.__start,
                [],
            )
        ]
        vis = [[False] * len(self.__matrix[0]) for _ in self.__matrix]
        alt = []

        while len(frontier) != 0:
            p, pos, path = heapq.heappop(frontier)
            if pos in path or vis[pos[0]][pos[1]]:
                continue

            path.append(pos)
            if pos == self.__end:
                self.__animate_solution(canvas, path)
                fn()
                return
            row, col = pos

            vis[row][col] = True
            if len(self.__matrix[row][col].connections) == 0:
                alt.append(path)
            for dr, dc in self.__matrix[row][col].connections:
                if row + dr < 0 or col + dc < 0:
                    continue
                self.__matrix[row][col].draw_move(
                    self.__matrix[row + dr][col + dc], canvas
                )
                heapq.heappush(
                    frontier,
                    (
                        abs(row - self.__end[0]) + abs(col - self.__end[1]) + len(path),
                        (row + dr, col + dc),
                        [(a, b) for a, b in path],
                    ),
                )
            fn()

        for path in alt:
            self.__animate_solution(canvas, path)

    def draw(self, canvas: Canvas):
        for row in self.__matrix:
            for cell in row:
                cell.draw(canvas, "black")
