from window import MazeWindow


def main():
    w = MazeWindow(70, 110, 14, 14, left=10.0, right=10.0, top=10.0, bottom=10.0)
    # w = MazeWindow(10, 10, 50, 50, left=10.0, right=10.0, top=10.0, bottom=10.0)
    w.wait_for_close()


if __name__ == "__main__":
    main()
