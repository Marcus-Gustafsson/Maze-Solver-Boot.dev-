from graphics import Cell, Point
import time
import random

class Maze:
    def __init__(
        self,
        top_left: Point,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None,
        seed = None
    ):
        # Store parameters as attributes
        self._x1 = top_left.x  # x-coordinate of top-left corner of the maze
        self._y1 = top_left.y  # y-coordinate of top-left corner of the maze
        self._num_rows = num_rows  # Number of rows in the maze
        self._num_cols = num_cols  # Number of columns in the maze
        self._cell_size_x = cell_size_x  # Width of each cell
        self._cell_size_y = cell_size_y  # Height of each cell
        self._win = win  # Window to draw on
        if seed != None:
            random.seed(seed)

        self.cell_creation_delay = 0.01  # Fast creation of cells
        self.wall_breaking_delay = 0.02  # Slightly slower wall-breaking
        self.pathfinding_delay = 0.3     # Slower pathfinding


        # Initialize the 2D list of cells
        self._cells = []

        # Create the maze's cells
        self._create_cells()

        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()

    def _create_cells(self):
        """
        This method populates self._cells with rows and columns of Cell objects.
        Each cell is created with its top-left and bottom-right points.
        """
        # Loop over columns
        for i in range(self._num_cols):
            col_cells = []  # Create a new list for this column
            # Loop over rows
            for j in range(self._num_rows):
                # Calculate the top-left and bottom-right points for each cell
                top_left_x = self._x1 + i * self._cell_size_x
                top_left_y = self._y1 + j * self._cell_size_y
                bottom_right_x = top_left_x + self._cell_size_x
                bottom_right_y = top_left_y + self._cell_size_y
                
                # Create a new Point object for top-left and bottom-right
                top_left = Point(top_left_x, top_left_y)
                bottom_right = Point(bottom_right_x, bottom_right_y)

                # Create the new Cell and add it to the column
                cell = Cell(top_left, bottom_right, self._win)
                col_cells.append(cell)
            
            # Add the column of cells to the main list of cells
            self._cells.append(col_cells)

        # Draw all the cells
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j) -> None:
        """
        This method simply draws the cell at position (i, j).
        """
        if self._win is None:
            return
        # Retrieve the cell from the list
        cell = self._cells[i][j]
        # Draw the cell
        cell.draw()
        # Animate the drawing process
        self._animate(self.cell_creation_delay)

    def _animate(self, delay: float = 0.1) -> None:
        """
        This method redraws the window and adds a small delay to create a visible animation.
        The delay can be passed as a parameter to control the animation speed.
        """
        if self._win is None:
            return
        self._win.redraw()  # Update the window
        time.sleep(delay)  # Pause based on the provided delay


    
    def _break_entrance_and_exit(self) -> None:
        """
        Breaks down the entrance wall and exit wall to the maze (top top-left = entrance, bottom bottom-right = exit)
        """
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        """
        Depth-first traversal through the cells, breaking down walls as it goes.
        """
        # 1. Mark the current cell as visited
        current_cell = self._cells[i][j]
        current_cell.visited = True  # Add a 'visited' attribute to the Cell class

        # 2. Infinite loop to keep exploring until we can't go any further
        while True:
            to_visit = []  # Create a list to hold neighboring cells that are valid to visit

            # 3. Check neighboring cells (up, down, left, right) if they're within bounds and not visited

            # Move Up: Check the cell above (i, j-1)
            if j > 0 and not self._cells[i][j - 1].visited:
                to_visit.append(("up", i, j - 1))

            # Move Down: Check the cell below (i, j+1)
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                to_visit.append(("down", i, j + 1))

            # Move Left: Check the cell to the left (i-1, j)
            if i > 0 and not self._cells[i - 1][j].visited:
                to_visit.append(("left", i - 1, j))

            # Move Right: Check the cell to the right (i+1, j)
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                to_visit.append(("right", i + 1, j))

            # 4. If there are no cells to visit, return to stop the recursion
            if len(to_visit) == 0:
                self._draw_cell(i, j)  # Draw the current cell
                return

            # 5. Pick a random direction from the possible directions
            direction, ni, nj = random.choice(to_visit)

            # 6. Knock down the wall between the current cell and the chosen cell
            if direction == "up":
                # Remove the top wall of the current cell and the bottom wall of the above cell
                current_cell.has_top_wall = False
                self._cells[ni][nj].has_bottom_wall = False

            elif direction == "down":
                # Remove the bottom wall of the current cell and the top wall of the below cell
                current_cell.has_bottom_wall = False
                self._cells[ni][nj].has_top_wall = False

            elif direction == "left":
                # Remove the left wall of the current cell and the right wall of the left cell
                current_cell.has_left_wall = False
                self._cells[ni][nj].has_right_wall = False

            elif direction == "right":
                # Remove the right wall of the current cell and the left wall of the right cell
                current_cell.has_right_wall = False
                self._cells[ni][nj].has_left_wall = False

            # 7. Move to the chosen neighboring cell and recursively call _break_walls_r
            self._break_walls_r(ni, nj)

    
    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    

    def solve(self, i: int, j: int) -> None:
        """
        The solve() method starts the maze-solving process from the given (i, j) coordinates.
        It calls the _solve_r method recursively to explore the maze.
        """
        return self._solve_r(i, j)


    def _solve_r(self, i: int, j: int) -> bool:
        """
        Depth-first solution to the maze.
        Returns True if the current cell leads to the exit, False if it is a dead end.
        """
        # 1. Animate the movement by redrawing the window.
        self._animate(self.pathfinding_delay)

        # 2. Mark the current cell as visited.
        current_cell = self._cells[i][j]
        current_cell.visited = True

        # 3. Check if this is the "end" cell (bottom-right corner of the maze).
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True  # Found the exit!

        # 4. Explore neighboring cells (DFS).

        # Move Up: Check the cell above (i, j-1) if there is no wall and it is not visited.
        if j > 0 and not current_cell.has_top_wall and not self._cells[i][j - 1].visited:
            current_cell.draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                current_cell.draw_move(self._cells[i][j - 1], undo=True)

        # Move Down: Check the cell below (i, j+1) if there is no wall and it is not visited.
        if j < self._num_rows - 1 and not current_cell.has_bottom_wall and not self._cells[i][j + 1].visited:
            current_cell.draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                current_cell.draw_move(self._cells[i][j + 1], undo=True)

        # Move Left: Check the cell to the left (i-1, j) if there is no wall and it is not visited.
        if i > 0 and not current_cell.has_left_wall and not self._cells[i - 1][j].visited:
            current_cell.draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                current_cell.draw_move(self._cells[i - 1][j], undo=True)

        # Move Right: Check the cell to the right (i+1, j) if there is no wall and it is not visited.
        if i < self._num_cols - 1 and not current_cell.has_right_wall and not self._cells[i + 1][j].visited:
            current_cell.draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                current_cell.draw_move(self._cells[i + 1][j], undo=True)

        # If no valid moves were found, this is a dead end, so return False.
        return False



