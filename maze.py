from graphics import Cell, Point
import time
import random

class Maze:
    """
    The Maze class manages the creation, drawing, and solving of a maze.
    
    Attributes:
        _x1 (int): The x-coordinate of the top-left corner of the maze.
        _y1 (int): The y-coordinate of the top-left corner of the maze.
        _num_rows (int): The number of rows in the maze.
        _num_cols (int): The number of columns in the maze.
        _cell_size_x (int): The width of each cell.
        _cell_size_y (int): The height of each cell.
        _win (Window): The window object to draw the maze on.
        _cells (list): A 2D list holding the maze's cells.
    """
    
    def __init__(self, top_left: Point, num_rows: int, num_cols: int, 
                 cell_size_x: int, cell_size_y: int, win=None, seed=None) -> None:
        """
        Initializes a maze with the given parameters, creates the cells, and breaks the entrance and exit walls.

        Args:
            top_left (Point): The top-left corner of the maze.
            num_rows (int): The number of rows in the maze.
            num_cols (int): The number of columns in the maze.
            cell_size_x (int): The width of each cell.
            cell_size_y (int): The height of each cell.
            win (Window, optional): The window object where the maze will be drawn. Defaults to None.
            seed (int, optional): Seed for randomizing the maze generation. Defaults to None.
        """
        self._x1 = top_left.x
        self._y1 = top_left.y
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed is not None:
            random.seed(seed)

        self.cell_creation_delay = 0.01  # Fast creation of cells
        self.wall_breaking_delay = 0.02  # Slightly slower wall-breaking
        self.pathfinding_delay = 0.08    # Slower pathfinding

        # Initialize the 2D list of cells
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self) -> None:
        """
        Populates the maze with cells based on the number of rows and columns. 
        Each cell is initialized with its top-left and bottom-right coordinates.
        """
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                # Calculate cell coordinates
                top_left_x = self._x1 + i * self._cell_size_x
                top_left_y = self._y1 + j * self._cell_size_y
                bottom_right_x = top_left_x + self._cell_size_x
                bottom_right_y = top_left_y + self._cell_size_y

                # Create the cell and append it to the column list
                top_left = Point(top_left_x, top_left_y)
                bottom_right = Point(bottom_right_x, bottom_right_y)
                cell = Cell(top_left, bottom_right, self._win)
                col_cells.append(cell)
            # Add the column of cells to the main cell list
            self._cells.append(col_cells)

        # Draw all cells
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i: int, j: int) -> None:
        """
        Draws the cell at position (i, j) and animates the drawing process.

        Args:
            i (int): The column index of the cell.
            j (int): The row index of the cell.
        """
        if self._win is None:
            return
        cell = self._cells[i][j]
        cell.draw()
        self._animate(self.cell_creation_delay)

    def _animate(self, delay: float = 0.1) -> None:
        """
        Redraws the window with a given delay for animation.

        Args:
            delay (float, optional): The time to pause for animation. Defaults to 0.1 seconds.
        """
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(delay)

    def _break_entrance_and_exit(self) -> None:
        """
        Breaks down the entrance (top-left) and exit (bottom-right) walls. 
        Places Zelda at the exit.
        """
        # Break the entrance (top-left corner)
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)

        # Break the exit (bottom-right corner)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

        # Position Zelda at the midpoint of the bottom wall
        exit_cell = self._cells[self._num_cols - 1][self._num_rows - 1]
        midpoint_x = (exit_cell.bottom_left.x + exit_cell.bottom_right.x) // 2
        midpoint_y = exit_cell.bottom_right.y
        self._win.create_zelda_sprite(midpoint_x, midpoint_y + 15)

    def _break_walls_r(self, i: int, j: int) -> None:
        """
        Recursively breaks walls using depth-first traversal.

        Args:
            i (int): The column index of the current cell.
            j (int): The row index of the current cell.
        """
        current_cell = self._cells[i][j]
        current_cell.visited = True

        while True:
            to_visit = []
            # Check all valid neighboring cells that haven't been visited
            if j > 0 and not self._cells[i][j - 1].visited:
                to_visit.append(("up", i, j - 1))
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                to_visit.append(("down", i, j + 1))
            if i > 0 and not self._cells[i - 1][j].visited:
                to_visit.append(("left", i - 1, j))
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                to_visit.append(("right", i + 1, j))

            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return

            direction, ni, nj = random.choice(to_visit)

            # Break down walls between current cell and selected neighboring cell
            if direction == "up":
                current_cell.has_top_wall = False
                self._cells[ni][nj].has_bottom_wall = False
            elif direction == "down":
                current_cell.has_bottom_wall = False
                self._cells[ni][nj].has_top_wall = False
            elif direction == "left":
                current_cell.has_left_wall = False
                self._cells[ni][nj].has_right_wall = False
            elif direction == "right":
                current_cell.has_right_wall = False
                self._cells[ni][nj].has_left_wall = False

            self._break_walls_r(ni, nj)

    def _reset_cells_visited(self) -> None:
        """Resets the visited status of all cells."""
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self, i: int, j: int) -> bool:
        """
        Starts the maze-solving process from the given (i, j) coordinates.

        Args:
            i (int): The starting column index.
            j (int): The starting row index.

        Returns:
            bool: True if the maze is solved, False otherwise.
        """
        return self._solve_r(i, j)

    def _solve_r(self, i: int, j: int) -> bool:
        """
        Recursively solves the maze using depth-first search.

        Args:
            i (int): The column index of the current cell.
            j (int): The row index of the current cell.

        Returns:
            bool: True if the maze is solved, False otherwise.
        """
        # Animate the pathfinding process to make it visible to the user (slow it down by the defined delay)
        self._animate(self.pathfinding_delay)

        # Retrieve the current cell at position (i, j)
        current_cell = self._cells[i][j]
        
        # Mark this cell as visited to avoid revisiting it
        current_cell.visited = True

        # Check if the current cell is the exit (bottom-right corner of the maze)
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            # If we're at the exit, return True indicating the maze has been solved
            return True

        # Prepare to explore neighboring cells in all four directions: up, down, left, right
        # The 'valid' flag indicates whether there is no wall blocking the movement in that direction
        directions = [
            ("up", i, j - 1, not current_cell.has_top_wall),    # Move up, if no top wall
            ("down", i, j + 1, not current_cell.has_bottom_wall), # Move down, if no bottom wall
            ("left", i - 1, j, not current_cell.has_left_wall),   # Move left, if no left wall
            ("right", i + 1, j, not current_cell.has_right_wall)  # Move right, if no right wall
        ]

        # Iterate over each direction (up, down, left, right)
        for direction, ni, nj, valid in directions:
            # Check if the direction is valid (i.e., no wall) and if the target cell is within maze bounds and not visited
            if valid and 0 <= ni < self._num_cols and 0 <= nj < self._num_rows and not self._cells[ni][nj].visited:
                # Move to the neighboring cell and visually draw the movement
                current_cell.draw_move(self._cells[ni][nj])

                # Recursively attempt to solve the maze from the neighboring cell
                if self._solve_r(ni, nj):
                    # If a solution is found, return True (to propagate the success back through the recursion)
                    return True
                else:
                    # If the neighboring path is a dead end, backtrack by undoing the move visually
                    current_cell.draw_move(self._cells[ni][nj], undo=True)

        # If no valid moves are found from the current cell, return False indicating a dead end
        return False




