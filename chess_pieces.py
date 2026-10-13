# The board is 8 squares wide and 8 squares tall.
BOARD_SIZE = 8


class InvalidColourError(ValueError):
    """Raised when a colour is not "white" or "black"."""


class InvalidPositionError(ValueError):
    """Raised when a position is not a real square on the board."""


class Piece:
    """The parent class: what every chess piece has in common.

    Every piece has a colour and a position. The child classes (Bishop,
    Rook, ...) get these for free and only add their own way of moving.
    """

    def __init__(self, colour, position):
        """Create a piece, checking the colour and position first.

        Args:
            colour: "white" or "black".
            position: a pair (column, row), for example (3, 4).

        Raises:
            InvalidColourError: if the colour is not white or black.
            InvalidPositionError: if the position is not on the board.
        """
        if colour not in ("white", "black"):
            raise InvalidColourError("Colour must be 'white' or 'black'.")

        # The leading underscore means "protected": other code should not
        # touch this directly. It can only be read through the property.
        self._colour = colour

        # This line uses the position setter below, so the position is
        # checked in exactly one place.
        self.position = position

    @property
    def colour(self):
        """Return the colour. There is no setter, so it cannot be changed."""
        return self._colour

    @property
    def position(self):
        """Return the current position as (column, row)."""
        return self._position

    @position.setter
    def position(self, new_position):
        """Change the position, but only if the new one is valid."""
        # It must be a pair, like (3, 4).
        if not isinstance(new_position, tuple) or len(new_position) != 2:
            raise InvalidPositionError("Position must be a pair like (3, 4).")

        column, row = new_position

        # Both numbers must be whole numbers.
        if not isinstance(column, int) or not isinstance(row, int):
            raise InvalidPositionError("Column and row must be whole numbers.")

        # Both numbers must be inside the board (0 to 7).
        if not self._on_board(column, row):
            raise InvalidPositionError("Column and row must be 0 to 7.")

        self._position = new_position

    def _on_board(self, column, row):
        """Return True if the square is inside the 8x8 board."""
        return 0 <= column < BOARD_SIZE and 0 <= row < BOARD_SIZE

    def _slide(self, directions):
        """Return every square reached by sliding in the given directions.

        A direction is a pair like (1, 0), meaning "one column to the
        right, same row". We keep taking steps in that direction until we
        fall off the edge of the board.
        """
        moves = []
        for column_step, row_step in directions:
            # Start one step away from where the piece is standing.
            column = self._position[0] + column_step
            row = self._position[1] + row_step

            # Keep going while we are still on the board.
            while self._on_board(column, row):
                moves.append((column, row))
                column = column + column_step
                row = row + row_step
        return moves

    def get_moves(self):
        """Return the squares this piece can move to.

        The parent does not know how a generic piece moves, so every
        child class must replace (override) this method.
        """
        raise NotImplementedError("Each piece must define get_moves().")


class Bishop(Piece):
    """A bishop moves any number of squares diagonally."""

    def get_moves(self):
        """Return all diagonal squares (on an empty board)."""
        diagonals = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self._slide(diagonals)


class Rook(Piece):
    """A rook moves any number of squares along its row or column."""

    def get_moves(self):
        """Return all squares in the same row or column (empty board)."""
        straight_lines = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        return self._slide(straight_lines)


class Queen(Bishop, Rook):
    """A queen moves like a bishop and a rook combined.

    Both parents have a get_moves method. Python would only use the first
    one (Bishop's), so we call each parent by name and join the two lists.
    """

    def get_moves(self):
        """Return the diagonal moves plus the straight-line moves."""
        diagonal_moves = Bishop.get_moves(self)
        straight_moves = Rook.get_moves(self)
        return diagonal_moves + straight_moves