import unittest
from maze import Maze  # Import the Maze class that we want to test
from graphics import Point  # Import the Point class for specifying coordinates


# Test cases for the Maze class
class Tests(unittest.TestCase):
    
    def test_maze_create_cells(self):
        """
        Test if the Maze class correctly creates a grid of cells.
        We expect the Maze to create the correct number of columns and rows based on the inputs.
        """
        num_cols = 12  # We expect 12 columns in the maze
        num_rows = 10  # We expect 10 rows in the maze
        m1 = Maze(Point(0, 0), num_rows, num_cols, 10, 10)  # Initialize a Maze object

        # Check if the Maze created the correct number of columns
        self.assertEqual(len(m1._cells), num_cols)
        # Check if the Maze created the correct number of rows in the first column
        self.assertEqual(len(m1._cells[0]), num_rows)

        self.assertEqual(
            m1._cells[0][0].has_top_wall,
            False,
        )
        self.assertEqual(
            m1._cells[num_cols - 1][num_rows - 1].has_bottom_wall,
            False,
        )

        # Checks if all cells "visited" are reset after breaking walls in maze
        for col in m1._cells:
            for cell in col:
                self.assertEqual(
                    cell.visited,
                    False,
                )

    def test_maze_create_cells_large(self):
        """
        Test if the Maze class can handle creating a larger grid of cells.
        This test uses a larger maze with 16 columns and 12 rows, and checks if they are created correctly.
        """
        num_cols = 16  # We expect 16 columns in the maze
        num_rows = 12  # We expect 12 rows in the maze
        m1 = Maze(Point(0, 0), num_rows, num_cols, 10, 10)  # Initialize a larger Maze object

        # Check if the Maze created the correct number of columns
        self.assertEqual(len(m1._cells), num_cols)
        # Check if the Maze created the correct number of rows in the first column
        self.assertEqual(len(m1._cells[0]), num_rows)

        self.assertEqual(
            m1._cells[0][0].has_top_wall,
            False,
        )
        self.assertEqual(
            m1._cells[num_cols - 1][num_rows - 1].has_bottom_wall,
            False,
        )

        # Checks if all cells "visited" are reset after breaking walls in maze
        for col in m1._cells:
            for cell in col:
                self.assertEqual(
                    cell.visited,
                    False,
                )



if __name__ == "__main__":
    unittest.main()  # Run all the tests when the file is executed
