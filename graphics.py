from tkinter import Tk, Canvas, BOTH
from PIL import Image, ImageTk  # Import Image and ImageTk from Pillow to handle image scaling
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

    def __init__(self, width: int, height: int, image_path: str = None) -> None:
        self.width: int = width
        self.height: int = height
        self.__root_widget = Tk()
        self.__root_widget.title("Maze Solver")

        # Create the canvas
        self.canvas = Canvas(self.__root_widget, bg="white", height=height, width=width)
        self.canvas.pack(fill=BOTH, expand=1)

        # Load, scale, and display background image if an image path is provided
        if image_path:
            image = Image.open(image_path)
            self.background_image = ImageTk.PhotoImage(image)
            self.canvas.create_image(-50, 0, image=self.background_image, anchor='nw')

        # Initialize sprite-related attributes
        self.sprite_id = None
        self.sprite_image = None
        self.load_sprite_image()  # Load the sprite image once

        self.window_running = False
        self.__root_widget.protocol("WM_DELETE_WINDOW", self.close)

    def load_sprite_image(self):
        """Load the sprite (Link) image."""
        sprite_path = "images/link_sprite.gif"  # Path to your sprite image
        self.sprite_image = Image.open(sprite_path)
        self.sprite_image = self.sprite_image.resize((25, 25))  # Resize to 20x20 pixels
        self.tk_sprite_image = ImageTk.PhotoImage(self.sprite_image)  # Convert to Tkinter format

    def create_sprite(self, x, y):
        """Create the sprite at the initial position (x, y)."""
        if self.sprite_id is None:
            self.sprite_id = self.canvas.create_image(x, y, image=self.tk_sprite_image, anchor='center')

    def move_sprite(self, x, y):
        """Move the sprite to a new position (x, y)."""
        if self.sprite_id is not None:
            current_coords = self.canvas.coords(self.sprite_id)
            x_offset = x - current_coords[0]
            y_offset = y - current_coords[1]

            # Move the sprite using the calculated offsets
            self.canvas.move(self.sprite_id, x_offset, y_offset)
            self.canvas.update()  # Update the canvas to reflect the movement

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
        """ Stop the window running state. """
        self.window_running = False
    
    def draw_line(self, line: Line, fill_color: str,) -> None:
        """
        draw_line method on our Window class. It should take an instance of a Line and a fill_color as inputs, then call the Line's draw() method.
        
        """
        line.draw(self.canvas, fill_color)




class Cell:

    def __init__(self, top_left: Point, bottom_right: Point, window: Window = None) -> None:
        self.has_left_wall: bool = True
        self.has_right_wall: bool = True
        self.has_top_wall: bool = True
        self.has_bottom_wall: bool = True
        self.top_left: Point = top_left
        self._win: Window = window
        self.visited: bool = False

        # Store the line IDs for each wall (so we can delete them later)
        self.left_wall_id = None
        self.right_wall_id = None
        self.top_wall_id = None
        self.bottom_wall_id = None

        width = bottom_right.x - top_left.x
        height = bottom_right.y - top_left.y

        # Adjust to ensure it's a square
        side_length = min(width, height)

        # Update bottom_right based on the adjusted side_length
        self.bottom_right: Point = Point(top_left.x + side_length, top_left.y + side_length)
        
        # Calculate other corners
        self.bottom_left: Point = Point(top_left.x, top_left.y + side_length)
        self.top_right: Point = Point(top_left.x + side_length, top_left.y)

        self.middle: Point = Point((self.bottom_right.x + self.top_left.x) // 2, (self.bottom_right.y + self.top_left.y) // 2)


    def draw(self) -> None:
        """
        Draw the walls of the cell. If the wall has already been removed, make sure the line is deleted.
        """
        wall_color = "#228B22"
        
        if self._win is None:
            return

        # Draw or remove the left wall
        if self.has_left_wall:
            if self.left_wall_id is None:  # Only draw if it hasn't been drawn yet
                self.left_wall_id = self._win.canvas.create_line(self.bottom_left.x, self.bottom_left.y, self.top_left.x, self.top_left.y, fill=wall_color, width=2)
        else:
            if self.left_wall_id is not None:  # Remove the line if it exists
                self._win.canvas.delete(self.left_wall_id)
                self.left_wall_id = None

        # Draw or remove the top wall
        if self.has_top_wall:
            if self.top_wall_id is None:  # Only draw if it hasn't been drawn yet
                self.top_wall_id = self._win.canvas.create_line(self.top_left.x, self.top_left.y, self.top_right.x, self.top_right.y, fill=wall_color, width=2)
        else:
            if self.top_wall_id is not None:  # Remove the line if it exists
                self._win.canvas.delete(self.top_wall_id)
                self.top_wall_id = None

        # Draw or remove the right wall
        if self.has_right_wall:
            if self.right_wall_id is None:  # Only draw if it hasn't been drawn yet
                self.right_wall_id = self._win.canvas.create_line(self.top_right.x, self.top_right.y, self.bottom_right.x, self.bottom_right.y, fill=wall_color, width=2)
        else:
            if self.right_wall_id is not None:  # Remove the line if it exists
                self._win.canvas.delete(self.right_wall_id)
                self.right_wall_id = None

        # Draw or remove the bottom wall
        if self.has_bottom_wall:
            if self.bottom_wall_id is None:  # Only draw if it hasn't been drawn yet
                self.bottom_wall_id = self._win.canvas.create_line(self.bottom_right.x, self.bottom_right.y, self.bottom_left.x, self.bottom_left.y, fill=wall_color, width=2)
        else:
            if self.bottom_wall_id is not None:  # Remove the line if it exists
                self._win.canvas.delete(self.bottom_wall_id)
                self.bottom_wall_id = None

    
    def draw_move(self, to_cell, undo: bool = False):
        """Move the sprite and draw the movement between cells."""
        line_to_draw = Line(self.middle, to_cell.middle)
        triforce_gold = "#FFD700"

        if not undo:
            # Draw the movement line in triforce gold color
            self._win.draw_line(line_to_draw, triforce_gold)

            # Ensure the sprite is created once and then moved
            if self._win.sprite_id is None:
                # Create the sprite at the initial position
                self._win.create_sprite(self.middle.x, self.middle.y)
            else:
                # Move the sprite to the new position
                self._win.move_sprite(to_cell.middle.x, to_cell.middle.y)

        else:
            # Draw the undo movement line in gray
            self._win.draw_line(line_to_draw, "#708090")



        

