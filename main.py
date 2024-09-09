from graphics import Point, Window
from maze import Maze
import sys

def main() -> None:
    """
    Main function to initialize and run the Maze Solver.
    It creates a window, generates a maze, and attempts to solve it.

    Parameters:
    None

    Returns:
    None
    """
    num_rows: int = 12
    num_cols: int = 16
    window_width: int = 800  # Total width of the window
    window_height: int = 600  # Total height of the window

    # Calculate the available width and height for the maze, accounting for margins
    available_width: int = window_width - 100
    available_height: int = window_height - 100

    cell_width: int = available_width // num_cols
    cell_height: int = available_height // num_rows

    maze_width: int = cell_width * num_cols
    maze_height: int = cell_height * num_rows

    # Adjust margins to center the maze in the window
    horizontal_margin: int = (window_width - maze_width) // 2
    vertical_margin: int = (window_height - maze_height) // 2

    margin_point: Point = Point(horizontal_margin, vertical_margin)

    background_image_path: str = "images/background.png"

    # Increase the recursion limit to handle deep recursion for large mazes
    sys.setrecursionlimit(10000)

    # Create the window with the background image
    win: Window = Window(window_width, window_height, background_image_path)

    # Create and solve the maze
    maze: Maze = Maze(margin_point, num_rows, num_cols, cell_width, cell_height, win)
    print("Maze created")

    # Solve the maze starting from the top-left corner
    maze_solved: bool = maze.solve(0, 0)
    
    if not maze_solved:
        print("Maze cannot be solved!")
    else:
        print("Maze solved!")

    # Keep the window open until manually closed
    win.wait_for_close()

if __name__ == "__main__":
    main()





