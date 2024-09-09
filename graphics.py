from tkinter import Tk, Canvas, BOTH
from PIL import Image, ImageTk
import time

class Point:
    """
    Represents a point in 2D space with x and y coordinates.
    
    Attributes:
        x (int): The x-coordinate of the point in pixels.
        y (int): The y-coordinate of the point in pixels.
    
    Notes:
        - x=0 refers to the left side of the screen.
        - y=0 refers to the top of the screen.
    """
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y


class Line:
    """
    Represents a line segment between two points in 2D space.
    
    Attributes:
        start_point (Point): The starting point of the line.
        end_point (Point): The ending point of the line.
    """
    def __init__(self, start_point: Point, end_point: Point) -> None:
        self.start_point: Point = start_point
        self.end_point: Point = end_point

    def draw(self, canvas: Canvas, fill_color: str) -> None:
        """
        Draws the line on the provided canvas using the specified color.
        
        Parameters:
        canvas (Canvas): The Tkinter canvas on which to draw the line.
        fill_color (str): The color to use when drawing the line (e.g., "black", "red").
        
        Returns:
        None
        """
        canvas.create_line(
            self.start_point.x, self.start_point.y, 
            self.end_point.x, self.end_point.y, 
            fill=fill_color, width=2
        )



class Window:
    """
    The Window class manages the creation and rendering of a Tkinter window, 
    including the background image, and sprite objects (Link and Zelda).
    
    Attributes:
        width (int): The width of the window in pixels.
        height (int): The height of the window in pixels.
        canvas (Canvas): The drawing area where the maze and sprites are rendered.
        sprite_id_link (int): The ID of the Link sprite on the canvas.
        sprite_id_zelda (int): The ID of the Zelda sprite on the canvas.
        tk_sprite_image_link (PhotoImage): The image object for Link's sprite.
        tk_sprite_image_zelda (PhotoImage): The image object for Zelda's sprite.
    """
    def __init__(self, width: int, height: int, background_image_path: str = None) -> None:
        """
        Initializes the window with the given width and height, optionally loads a background image.
        
        Parameters:
        width (int): Width of the window in pixels.
        height (int): Height of the window in pixels.
        background_image_path (str, optional): Path to the background image. Defaults to None.
        """
        self.width: int = width
        self.height: int = height
        self.__root_widget = Tk()
        self.__root_widget.title("Maze Solver")

        # Create the canvas for drawing
        self.canvas = Canvas(self.__root_widget, bg="white", height=height, width=width)
        self.canvas.pack(fill=BOTH, expand=1)

        # Load background image if provided
        if background_image_path:
            image = Image.open(background_image_path)
            self.background_image = ImageTk.PhotoImage(image)
            self.canvas.create_image(-50, 0, image=self.background_image, anchor='nw')

        # Initialize sprite-related attributes
        self.sprite_id_link = None
        self.sprite_id_zelda = None
        self.tk_sprite_image_link = None
        self.tk_sprite_image_zelda = None

        # Load the sprite images for Link and Zelda
        self.load_sprite_images()

        self.window_running = False
        self.__root_widget.protocol("WM_DELETE_WINDOW", self.close)

    def load_sprite_images(self) -> None:
        """Loads and resizes the sprite images for Link and Zelda."""
        # Load Link's sprite
        sprite_path_link = "images/link_sprite.gif"
        self.sprite_image_link = Image.open(sprite_path_link)
        self.sprite_image_link = self.sprite_image_link.resize((35, 35))  # Resize for consistency
        self.tk_sprite_image_link = ImageTk.PhotoImage(self.sprite_image_link)

        # Load Zelda's sprite
        sprite_path_zelda = "images/zelda_sprite.png"
        self.sprite_image_zelda = Image.open(sprite_path_zelda)
        self.sprite_image_zelda = self.sprite_image_zelda.resize((50, 50))  # Slightly larger Zelda sprite
        self.tk_sprite_image_zelda = ImageTk.PhotoImage(self.sprite_image_zelda)

    def create_link_sprite(self, x: int, y: int) -> None:
        """Creates the Link sprite on the canvas at the given coordinates (x, y)."""
        if self.sprite_id_link is None:
            self.sprite_id_link = self.canvas.create_image(x, y, image=self.tk_sprite_image_link, anchor='center')

    def create_zelda_sprite(self, x: int, y: int) -> None:
        """Creates the Zelda sprite on the canvas at the given coordinates (x, y)."""
        if self.sprite_id_zelda is None:
            self.sprite_id_zelda = self.canvas.create_image(x, y, image=self.tk_sprite_image_zelda, anchor='center')

    def move_link_sprite(self, x: int, y: int) -> None:
        """Moves the Link sprite to a new position on the canvas."""
        if self.sprite_id_link is not None:
            current_coords = self.canvas.coords(self.sprite_id_link)
            x_offset = x - current_coords[0]
            y_offset = y - current_coords[1]

            # Move the sprite using the calculated offsets
            self.canvas.move(self.sprite_id_link, x_offset, y_offset)
            self.canvas.update()  # Update the canvas to reflect the movement

    def redraw(self) -> None:
        """
        Redraws the window by calling the root widget's update methods.
        Ensures the canvas and all elements are refreshed.
        """
        self.__root_widget.update_idletasks()
        self.__root_widget.update()

    def wait_for_close(self) -> None:
        """
        Continuously redraws the window until it is closed by the user.
        Ensures the window remains responsive while running.
        """
        self.window_running = True
        while self.window_running:
            self.redraw()
            time.sleep(0.01)  # Avoid CPU overuse by adding a small delay

    def close(self) -> None:
        """Closes the window by stopping the running state."""
        self.window_running = False

    def draw_line(self, line: Line, fill_color: str) -> None:
        """
        Draws a line on the canvas with the specified color.
        
        Parameters:
        line (Line): The Line object to be drawn.
        fill_color (str): The color to draw the line with (e.g., "black", "red").
        """
        line.draw(self.canvas, fill_color)




class Cell:
    """
    The Cell class represents a single cell in the maze. 
    It manages the walls of the cell, tracks visited status, and handles sprite movement.

    Attributes:
        top_left (Point): The top-left corner of the cell.
        bottom_right (Point): The bottom-right corner of the cell.
        middle (Point): The midpoint of the cell used for sprite movement.
        _win (Window): Reference to the window where the maze is drawn.
        has_left_wall (bool): Whether the left wall exists.
        has_right_wall (bool): Whether the right wall exists.
        has_top_wall (bool): Whether the top wall exists.
        has_bottom_wall (bool): Whether the bottom wall exists.
        visited (bool): Marks whether the cell has been visited during maze solving.
    """
    def __init__(self, top_left: Point, bottom_right: Point, window: Window = None) -> None:
        """
        Initializes a cell with given top-left and bottom-right corners. 
        
        Parameters:
        top_left (Point): The top-left corner of the cell.
        bottom_right (Point): The bottom-right corner of the cell.
        window (Window, optional): The window where the maze will be drawn. Defaults to None.
        """
        self.has_left_wall: bool = True
        self.has_right_wall: bool = True
        self.has_top_wall: bool = True
        self.has_bottom_wall: bool = True
        self.top_left: Point = top_left
        self._win: Window = window
        self.visited: bool = False

        # Store line IDs for each wall (helps in deleting them later if needed)
        self.left_wall_id = None
        self.right_wall_id = None
        self.top_wall_id = None
        self.bottom_wall_id = None

        # Calculate width and height of the cell
        width = bottom_right.x - top_left.x
        height = bottom_right.y - top_left.y

        # Ensure cell is square-shaped
        side_length = min(width, height)
        self.bottom_right = Point(top_left.x + side_length, top_left.y + side_length)

        # Calculate other corners of the cell
        self.bottom_left: Point = Point(top_left.x, top_left.y + side_length)
        self.top_right: Point = Point(top_left.x + side_length, top_left.y)

        # Calculate the midpoint for sprite movements
        self.middle: Point = Point(
            (self.bottom_right.x + self.top_left.x) // 2, 
            (self.bottom_right.y + self.top_left.y) // 2
        )

    def draw(self) -> None:
        """
        Draws the walls of the cell based on whether they exist. 
        Walls are drawn with the specified color, or removed if they no longer exist.
        """
        wall_color = "#8B4513"  # Dark brown color resembling Zelda dungeon walls

        if self._win is None:
            return

        # Draw or remove the left wall
        if self.has_left_wall:
            if self.left_wall_id is None:
                self.left_wall_id = self._win.canvas.create_line(
                    self.bottom_left.x, self.bottom_left.y, self.top_left.x, self.top_left.y, 
                    fill=wall_color, width=2
                )
        else:
            if self.left_wall_id is not None:
                self._win.canvas.delete(self.left_wall_id)
                self.left_wall_id = None

        # Draw or remove the top wall
        if self.has_top_wall:
            if self.top_wall_id is None:
                self.top_wall_id = self._win.canvas.create_line(
                    self.top_left.x, self.top_left.y, self.top_right.x, self.top_right.y, 
                    fill=wall_color, width=2
                )
        else:
            if self.top_wall_id is not None:
                self._win.canvas.delete(self.top_wall_id)
                self.top_wall_id = None

        # Draw or remove the right wall
        if self.has_right_wall:
            if self.right_wall_id is None:
                self.right_wall_id = self._win.canvas.create_line(
                    self.top_right.x, self.top_right.y, self.bottom_right.x, self.bottom_right.y, 
                    fill=wall_color, width=2
                )
        else:
            if self.right_wall_id is not None:
                self._win.canvas.delete(self.right_wall_id)
                self.right_wall_id = None

        # Draw or remove the bottom wall
        if self.has_bottom_wall:
            if self.bottom_wall_id is None:
                self.bottom_wall_id = self._win.canvas.create_line(
                    self.bottom_right.x, self.bottom_right.y, self.bottom_left.x, self.bottom_left.y, 
                    fill=wall_color, width=2
                )
        else:
            if self.bottom_wall_id is not None:
                self._win.canvas.delete(self.bottom_wall_id)
                self.bottom_wall_id = None

    def draw_move(self, to_cell: 'Cell', undo: bool = False) -> None:
        """
        Draws the movement line between cells and moves the sprite accordingly. 
        If undo is True, it reverts the movement.
        
        Parameters:
        to_cell (Cell): The destination cell where the sprite will move.
        undo (bool): Whether this is an undo operation (reverting the move). Defaults to False.
        """
        line_to_draw = Line(self.middle, to_cell.middle)
        move_color = "#FFD700"  # Triforce gold for movement lines

        if not undo:
            # Draw the movement line in triforce gold
            self._win.draw_line(line_to_draw, move_color)

            # Ensure the Link sprite is created once, then move it
            if self._win.sprite_id_link is None:
                self._win.create_link_sprite(self.middle.x, self.middle.y)
            else:
                self._win.move_link_sprite(to_cell.middle.x, to_cell.middle.y)
        else:
            # Draw the undo movement line in gray
            self._win.draw_line(line_to_draw, "#708090")