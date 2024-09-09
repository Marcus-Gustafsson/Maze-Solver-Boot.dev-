import unittest
from graphics import Point, Line, Window, Cell
from unittest.mock import Mock  # Mock allows us to simulate objects, like Canvas or Window, for testing

# Test cases for the Point class
class TestPoint(unittest.TestCase):
    def test_point_initialization(self):
        """
        Test the initialization of a Point object.
        We create a Point with x = 10 and y = 20, then check if it is initialized correctly.
        """
        p = Point(10, 20)
        # Check if x and y attributes are correctly set
        self.assertEqual(p.x, 10)
        self.assertEqual(p.y, 20)


# Test cases for the Line class
class TestLine(unittest.TestCase):
    def test_line_initialization(self):
        """
        Test the initialization of a Line object.
        We create a Line between two Point objects and check if the start and end points are set correctly.
        """
        start = Point(0, 0)
        end = Point(10, 10)
        line = Line(start, end)
        # Check if the start and end points are correctly assigned
        self.assertEqual(line.start_point.x, 0)
        self.assertEqual(line.end_point.x, 10)

    def test_draw_line(self):
        """
        Test the draw method of the Line class using a mock Canvas.
        We mock the Canvas object, call the draw method, and check if the Canvas's create_line method is called correctly.
        """
        mock_canvas = Mock()  # Create a mock object for Canvas
        start = Point(0, 0)
        end = Point(10, 10)
        line = Line(start, end)
        
        # Call the draw method on the mock canvas, simulating drawing the line
        line.draw(mock_canvas, "green")
        
        # Check if the mock Canvas's create_line method was called with the right parameters
        mock_canvas.create_line.assert_called_with(0, 0, 10, 10, fill="green", width=2)


# Test cases for the Cell class
class TestCell(unittest.TestCase):
    
    def test_cell_initialization(self):
        """
        Test the initialization of a Cell object.
        We create a Cell with a top-left and bottom-right point and check if the walls and points are initialized correctly.
        """
        top_left = Point(0, 0)
        bottom_right = Point(10, 10)
        cell = Cell(top_left, bottom_right)
        
        # Check if the walls are initialized as True
        self.assertTrue(cell.has_left_wall)
        self.assertTrue(cell.has_right_wall)
        # Check if the top-left corner is correctly assigned
        self.assertEqual(cell.top_left.x, 0)


class TestCell(unittest.TestCase):
    
    def test_cell_draw(self):
        """
        Test the draw method of the Cell class using a mock Window.
        We mock the Window object and check if the create_line method is called for each wall.
        Initially, four walls should be drawn. After removing walls, those walls should not be redrawn.
        """
        top_left = Point(0, 0)
        bottom_right = Point(10, 10)

        # Create a mock window object with a mock canvas
        mock_window = Mock()
        mock_window.canvas = Mock()

        # Create the cell
        cell = Cell(top_left, bottom_right, window=mock_window)
        
        # Draw the cell initially (all walls should be drawn)
        cell.draw()

        # Check that create_line was called exactly four times (once for each wall)
        self.assertEqual(mock_window.canvas.create_line.call_count, 4)



if __name__ == "__main__":
    unittest.main()
