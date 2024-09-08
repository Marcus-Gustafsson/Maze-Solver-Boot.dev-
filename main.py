from graphics import *

def main() -> None:
    win = Window(800, 600)
    test_cell_1 = Cell(Point(30,50), Point(80,100), win)
    test_cell_1.draw()
    test_cell_2 = Cell(Point(150,50), Point(200,100), win)
    test_cell_2.draw()
    test_cell_1.draw_move(test_cell_2, undo=True)
    win.wait_for_close()

if __name__ == "__main__":
    main()

