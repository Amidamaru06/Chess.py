#125304231
from chess_pieces import (Bishop,Board,ColourError,Piece,PositionError,Queen,Rook,SquareTakenError,)


def show(piece):
    """Print how many squares the piece can reach on an empty board."""
    print(f"{piece} can reach {len(piece.moves())} squares.")


def main():
    """Create some pieces, use them, and show the error handling."""
    rook = Rook("white", (0, 0))
    bishop = Bishop("black", (2, 0))
    queen = Queen("white", (3, 3))

    print("Moves on an empty board")
    for piece in (rook, bishop, queen):
        show(piece)
    print("\nSquares the bishop can reach")
    print(bishop.moves())

    """Inheritance, Queen inherits from Bishop and Rook"""
    print("\nInheritance")
    print("Queen is a Bishop:", isinstance(queen, Bishop))
    print("Queen is a Rook:", isinstance(queen, Rook))
    print("Queen is a Piece:", isinstance(queen, Piece))

    """Encapsulation, the position can change, but only to a real square"""
    print("\nChanging the position")
    queen.position = (7, 7)
    show(queen)

    """Error handling, bad values are caught and the piece stays valid"""
    print("\nError handling")
    try:
        Rook("red", (0, 0))
    except ColourError as err:
        print("Caught ColourError:", err)

    try:
        queen.position = (8, 8)
    except PositionError as err:
        print("Caught PositionError:", err)
    print("The queen is still at", queen.position)

    """Other kinds of bad position are rejected too"""
    for bad in ((1, 2, 3), "a1", (1.5, 2), (True, 0)):
        try:
            queen.position = bad
        except PositionError as err:
            print(f"Rejected {bad}: {err}")

    try:
        queen.colour = "black"
    except AttributeError:
        print("Caught AttributeError: the colour cannot be changed.")

    try:
        Piece("white", (0, 0)).moves()
    except NotImplementedError as err:
        print("Caught NotImplementedError:", err)


def demo_board():
    """Show a Board that holds pieces, and show its error handling."""

    #the board has pieces. They are given to it with add.
    board = Board()
    board.add(Rook("white", (0, 0)))
    board.add(Bishop("black", (2, 0)))
    board.add(Queen("white", (3, 3)))

    print("\nPieces on the board")
    print(board)
    for piece in board.pieces:
        show(piece)

    #Look up a square, a piece is returned, or None for an empty square.
    print("\nLooking at squares")
    print("Square (3, 3) holds:", board.piece_at((3, 3)))
    print("Square (5, 5) holds:", board.piece_at((5, 5)))

    #Error handling, the board refuses things that would break it.
    print("\nBoard error handling")
    try:
        board.add(Rook("black", (3, 3)))
    except SquareTakenError as err:
        print("Caught SquareTakenError:", err)

    try:
        board.add("not a piece")
    except TypeError as err:
        print("Caught TypeError:", err)
    print("After the errors,", board)

    try:
        board.pieces = ()
    except AttributeError:
        print("Caught AttributeError: the pieces cannot be replaced.")


if __name__ == "__main__":
    main()
    demo_board()