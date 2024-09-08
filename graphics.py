from tkinter import Tk, BOTH, Canvas
import time


class Point():
    """
    Point class
        Let's make a little Point class. It should simply store 2 public data members:

        x - the x-coordinate (horizontal) in pixels of the point
        y - the y-coordinate (vertical) in pixels of the point
        x=0 is the left of the screen.

        y=0 is the top of the screen.
    """
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

class Line():
    """
    The line class has a bit more logic in it. Its constructor should take 2 points as input, and save them as data members.
    """

    def __init__(self, start_point: Point, end_point: Point) -> None:
        self.start_point: Point = start_point
        self.end_point: Point = end_point



    def draw(self, canvas: Canvas, fill_color: str) -> None:
        """
        draw() method
        The Line class needs a draw() method that takes a Canvas and a "fill color" as input. The fill_color will just be a string like "black" or "red".
        
        """
        canvas.create_line(self.start_point.x, self.start_point.y, self.end_point.x, self.end_point.y, fill=fill_color, width=2)


class Window:

    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.__root_widget = Tk()
        self.__root_widget.title("Maze Solver")
        self.canvas = Canvas(self.__root_widget, bg="white", height=height, width=width)
        self.canvas.pack(fill=BOTH, expand=1)
        self.window_running: bool = False
        self.__root_widget.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self) -> None:

        """
        The redraw() method on the window class should simply call the root widget's update_idletasks() and update() methods. 
        Each time this is called, the window will redraw itself.
        """
        self.__root_widget.update_idletasks()
        self.__root_widget.update()


    def wait_for_close(self) -> None:
        """
        This method should set the data member we created to track the 'running' state of the window to True. 
        Next, it should call self.redraw() over and over as long as the running state remains True.
        
        """
        self.window_running = True
        while self.window_running:
            self.redraw()
            time.sleep(0.01)  # Avoid CPU overuse by adding a small delay



    def close(self) -> None:
        """
        Lastly, the close() method should simply set the running state to False. 
        You'll also need to add another line to the constructor to call the protocol method on the root widget, to connect your close method to the "delete window" action. 
        This will stop your program from running when you close the graphical window.
        
        """
        self.window_running = False
    
    def draw_line(self, line: Line, fill_color: str,) -> None:
        """
        draw_line method on our Window class. It should take an instance of a Line and a fill_color as inputs, then call the Line's draw() method.
        
        """
        line.draw(self.canvas, fill_color)




class Cell:

    def __init__(self, top_left: Point, bottom_right: Point, window: Window) -> None:
        self.has_left_wall: bool = True
        self.has_right_wall: bool = True
        self.has_top_wall: bool = True
        self.has_bottom_wall: bool = True
        self.top_left: Point = top_left
        self._win: Window = window

        # Calculate width and height
        width = bottom_right.x - top_left.x
        height = bottom_right.y - top_left.y

        # Adjust to ensure it's a square
        # smaller of the two (width or height) to keep it a square.
        side_length = min(width, height)

        # Update bottom_right based on the adjusted side_length
        self.bottom_right: Point = Point(top_left.x + side_length, top_left.y + side_length)
        
        # Calculate other corners
        self.bottom_left: Point = Point(top_left.x, top_left.y + side_length)
        self.top_right: Point = Point(top_left.x + side_length, top_left.y)

        self.middle: Point = Point((self.bottom_right.x + self.top_left.x) // 2, (self.bottom_right.y + self.top_left.y) // 2)


    def draw(self) -> None:
        """
        Draw the walls of the cell.
        """
        if self.has_left_wall:
            self._win.draw_line(Line(self.bottom_left, self.top_left),"green")

        if self.has_top_wall:
            self._win.draw_line(Line(self.top_left, self.top_right),"green")

        if self.has_right_wall:
            self._win.draw_line(Line(self.top_right, self.bottom_right),"green")

        if self.has_bottom_wall:
            self._win.draw_line(Line(self.bottom_right, self.bottom_left),"green")

    
    def draw_move(self, to_cell, undo: bool = False) -> None:

        if not undo:
            line_to_draw = Line(self.middle, to_cell.middle)
            self._win.draw_line(line_to_draw,"red")
        else:
            line_to_draw = Line(self.middle, to_cell.middle)
            self._win.draw_line(line_to_draw, "gray")
