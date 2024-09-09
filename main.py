from graphics import *
from maze import Maze
import sys

def main() -> None:
    num_rows = 12
    num_cols = 16
    screen_x = 800  # Total width of the window
    screen_y = 600  # Total height of the window

    # Calculate the available width and height for the maze
    available_width = screen_x - 100  # Total space for the maze, accounting for horizontal margins
    available_height = screen_y - 100  # Total space for the maze, accounting for vertical margins

    # Calculate cell sizes and make sure they're integers (to avoid floating-point errors)
    cell_size_x = int(available_width / num_cols)
    cell_size_y = int(available_height / num_rows)

    # Recalculate total width and height of the maze
    total_maze_width = cell_size_x * num_cols
    total_maze_height = cell_size_y * num_rows

    # Adjust the margins to center the maze
    margin_x = (screen_x - total_maze_width) // 2  # Center the maze horizontally
    margin_y = (screen_y - total_maze_height) // 2  # Center the maze vertically

    margin_point = Point(margin_x, margin_y)  # Create new margin point

    # Path to the background image in the 'images' folder
    image_path = "images/background.png"

    sys.setrecursionlimit(10000)
    # Create the window and pass the background image path
    win = Window(screen_x, screen_y, image_path)

    # Create the maze with integer cell sizes
    maze = Maze(margin_point, num_rows, num_cols, cell_size_x, cell_size_y, win)
    print("maze created")
    is_solveable = maze.solve(0,0)
    if not is_solveable:
        print("maze can not be solved!")
    else:
        print("maze solved!")
    win.wait_for_close()

if __name__ == "__main__":
    main()




