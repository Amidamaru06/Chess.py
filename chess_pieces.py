#125304231
"""Chess piece classes: Piece, Bishop, Rook and Queen.
Each piece knows its colour and its position, and can list the squares it
could reach on an otherwise empty board."""

# The board is 8 squares wide and 8 squares tall.
BOARD_SIZE = 8


class ColourError(ValueError):
    """Raised when a colour is not "white" or "black"."""


class PositionError(ValueError):
    """Raised when a position is not a real square on the board."""


class Piece:
    """The parent class: what every chess piece has in common.

    Every piece has a colour and a position. The child classes (Bishop,
    Rook and Queen) get these for free.
    """

    def __init__(self, colour, position):
        """Create a piece, checking the colour and the position.
        Raises ColourError if the colour is not "white" or "black".
        Raises PositionError if the position is not a real square.
        """
        if colour not in ("white", "black"):
            raise ColourError("Colour must be 'white' or 'black'.")

        """The underscore means "protected" other code should not touch
        this attribute directly."""
        self._colour = colour
        self.position = position

    def __str__(self):
        """Return text such as: white Rook at 0, 0."""
        return f"{self._colour} {type(self).__name__} at {self._position}"

    @property
    def colour(self):
        """Return the colour. There is no setter, so it is read-only."""
        return self._colour

    @property
    def position(self):
        """Return the current position as column, row."""
        return self._position

    @position.setter
    def position(self, value):
        """Change the position, but only if the new one is valid."""
        if not isinstance(value, tuple) or len(value) != 2:
            raise PositionError("Position must be a pair like (3, 4).")
        col, row = value

        for number in (col, row):
            if not isinstance(number, int) or isinstance(number, bool):
                raise PositionError("Column and row must be whole numbers.")

        if not self._on_board(col, row):
            raise PositionError("Column and row must be 0 to 7.")

        self._position = value

    def _on_board(self, col, row):
        """Return True if the square is inside the 8 by 8 board."""
        return 0 <= col < BOARD_SIZE and 0 <= row < BOARD_SIZE

    def _slide(self, directions):
        """Return every square reached by sliding in the given directions"""
        squares = []
        for col_step, row_step in directions:
            col = self._position[0] + col_step
            row = self._position[1] + row_step
            while self._on_board(col, row):
                squares.append((col, row))
                col += col_step
                row += row_step
        return squares

    def moves(self):
        """Return reachable squares (each child class defines this)."""
        raise NotImplementedError("Each piece must define moves().")


class Bishop(Piece):
    """A bishop moves any number of squares diagonally."""

    def moves(self):
        """Return all diagonal squares on an empty board"""
        diagonals = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self._slide(diagonals)


class Rook(Piece):
    """A rook moves any number of squares along its row or column."""

    def moves(self):
        """Return all straight line squares on an empty board"""
        lines = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        return self._slide(lines)


class Queen(Bishop, Rook):
    """A queen moves like a bishop and a rook combined.

    Queen inherits from both Bishop and Rook (multiple inheritance).
    Both parents have a moves method and Python would only use the
    first one Bishops"""

    def moves(self):
        """Return the diagonal squares then the straight line squares."""
        return Bishop.moves(self) + Rook.moves(self)


class SquareTakenError(PositionError):
    """Raised when a piece is added to a square that is already taken."""


class Board:
    """A chess board that holds a collection of pieces."""

    def __init__(self):
        """Create an empty board."""
        # Protected list, pieces can only be put in through add.
        self._pieces = []

    def __len__(self):
        """Return how many pieces are on the board"""
        return len(self._pieces)

    def __str__(self):
        """Return text such as: Board with 3 pieces"""
        word = "piece" if len(self._pieces) == 1 else "pieces"
        return f"Board with {len(self._pieces)} {word}"

    @property
    def pieces(self):
        """Return the pieces as a tuple so the list cannot be changed."""
        return tuple(self._pieces)

    def piece_at(self, position):
        """Return the piece on the given square, or None if it is empty"""
        for piece in self._pieces:
            if piece.position == position:
                return piece
        return None

    def add(self, piece):
        """Put a piece on the board.Raises TypeError if piece is not a Piece.
        Raises SquareTakenError if another piece is on that square"""
        if not isinstance(piece, Piece):
            raise TypeError("Only Piece objects can be added to a board.")

        taken_by = self.piece_at(piece.position)
        if taken_by is not None:
            raise SquareTakenError(
                f"Square {piece.position} is already taken by {taken_by}."
            )

        self._pieces.append(piece)