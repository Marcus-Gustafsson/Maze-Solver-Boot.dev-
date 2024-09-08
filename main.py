from graphics import *

def main() -> None:
    win = Window(800, 600)
    win.draw_line(Line(Point(10,25), Point(50,65)), "red")
    win.draw_line(Line(Point(35,75), Point(120,65)), "green")
    win.draw_line(Line(Point(45,25), Point(250,150)), "purple")
    win.wait_for_close()

if __name__ == "__main__":
    main()

