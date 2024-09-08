from graphics import Cell, Point
import time

class Maze:
    def __init__(
        self,
        top_left: Point,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win,
    ):
        # Store parameters as attributes
        self._x1 = top_left.x  # x-coordinate of top-left corner of the maze
        self._y1 = top_left.y  # y-coordinate of top-left corner of the maze
        self._num_rows = num_rows  # Number of rows in the maze
        self._num_cols = num_cols  # Number of columns in the maze
        self._cell_size_x = cell_size_x  # Width of each cell
        self._cell_size_y = cell_size_y  # Height of each cell
        self._win = win  # Window to draw on

        # Initialize the 2D list of cells
        self._cells = []

        # Create the maze's cells
        self._create_cells()

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

    def _draw_cell(self, i, j):
        """
        This method simply draws the cell at position (i, j).
        """
        # Retrieve the cell from the list
        cell = self._cells[i][j]
        # Draw the cell
        cell.draw()
        # Animate the drawing process
        self._animate()

    def _animate(self):
        """
        This method redraws the window and adds a small delay to create a visible animation.
        """
        self._win.redraw()  # Update the window
        time.sleep(0.05)    # Pause for 0.05 seconds to slow down the animation