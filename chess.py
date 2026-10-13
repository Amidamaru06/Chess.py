import unittest

from chess_pieces import (
    Bishop,
    InvalidColourError,
    InvalidPositionError,
    Piece,
    Queen,
    Rook,
)


class TestMoves(unittest.TestCase):
    """Check how many squares each piece can reach on an empty board."""

    def test_rook_in_centre_has_14_moves(self):
        self.assertEqual(len(Rook("white", (3, 3)).get_moves()), 14)

    def test_rook_in_corner_has_14_moves(self):
        self.assertEqual(len(Rook("black", (0, 0)).get_moves()), 14)

    def test_bishop_in_centre_has_13_moves(self):
        self.assertEqual(len(Bishop("white", (3, 3)).get_moves()), 13)

    def test_bishop_in_corner_has_7_moves(self):
        self.assertEqual(len(Bishop("white", (0, 0)).get_moves()), 7)

    def test_queen_in_centre_has_27_moves(self):
        self.assertEqual(len(Queen("white", (3, 3)).get_moves()), 27)

    def test_queen_combines_bishop_and_rook_moves(self):
        queen = Queen("white", (2, 5))
        expected = set(Bishop("white", (2, 5)).get_moves()) | set(
            Rook("white", (2, 5)).get_moves()
        )
        self.assertEqual(set(queen.get_moves()), expected)

    def test_moves_never_include_current_square_or_leave_board(self):
        for piece in (Rook("white", (4, 2)), Bishop("white", (4, 2))):
            for column, row in piece.get_moves():
                self.assertNotEqual((column, row), piece.position)
                self.assertTrue(0 <= column < 8 and 0 <= row < 8)


class TestInheritance(unittest.TestCase):


    def test_queen_is_a_bishop_and_a_rook_and_a_piece(self):
        queen = Queen("black", (0, 0))
        self.assertIsInstance(queen, Bishop)
        self.assertIsInstance(queen, Rook)
        self.assertIsInstance(queen, Piece)

    def test_base_piece_has_no_moves_of_its_own(self):
        with self.assertRaises(NotImplementedError):
            Piece("white", (0, 0)).get_moves()


class TestValidation(unittest.TestCase):
    """Check that invalid values are rejected."""

    def test_bad_colours_are_rejected(self):
        for bad in ("red", "", None, 5, ["white"]):
            with self.assertRaises(InvalidColourError):
                Rook(bad, (0, 0))


if __name__ == "__main__":
    unittest.main()