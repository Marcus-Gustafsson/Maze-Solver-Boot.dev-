from graphics import *

class Maze():

    """
    It initializes data members for all its inputs, then calls its _create_cells() method
    """

    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win: Window,
    ) -> None:
        pass


    def _create_cell(self) -> None:
        """
        This method should fill a self._cells list with lists of cells. 
        Each top-level list is a column of Cell objects. 
        Once the matrix is populated it should call its _draw_cell() method on each Cell.
        
        """
        pass


    def _draw_cell(self, i, j) -> None:
        """
        This method should calculate the x/y position of the Cell based on i, j, the cell_size, 
        and the x/y position of the Maze itself. 
        
        The x/y position of the maze represents how many pixels from the top and left 
        the maze should start from the side of the window.

        Once that's calculated, it should draw the cell and call the maze's _animate() method.
        
        """
        pass

    def _animate(self) -> None:

        """
        The animate method is what allows us to visualize what the algorithms are doing in real time. 
        It should simply call the window's redraw() method, then sleep for a short amount of time so your eyes keep up with each render frame. 
        I slept for 0.05 seconds.
        
        """
        pass