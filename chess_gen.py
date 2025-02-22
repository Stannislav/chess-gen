"""Generate chess positions and practise on Lichess."""

from __future__ import annotations

import argparse
import random
import textwrap
from urllib.parse import quote

from chess import BLACK, PIECE_SYMBOLS, WHITE, Board, Piece
from rich import print as rprint
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table

__version__ = "1.1.0"

WHITE_PAWN = Piece.from_symbol("P")
BLACK_PAWN = Piece.from_symbol("p")
WHITE_KING = Piece.from_symbol("K")
BLACK_KING = Piece.from_symbol("k")


class StopExecutionError(Exception):
    """Error indicating that the user chose to quit the program."""


class NeedHelpError(Exception):
    """Error indicating that the user needs usage help."""


class InvalidSelectionError(Exception):
    """Error indicating that the user input was invalid."""


def main() -> None:
    description = "Generate chess positions and practise on Lichess."
    parser = argparse.ArgumentParser(description=description)
    parser.parse_args()
    rprint(description)
    loop()


def init_board() -> Board:
    """Generate a legal board with two kings only."""
    board = Board()
    board.clear()
    board.set_piece_at(random.randint(0, 63), Piece.from_symbol("K"))
    set_randomly([Piece.from_symbol("k")], board, check_game_over=False)

    return board


def set_randomly(pieces: list[Piece], board: Board, *, check_game_over: bool = True) -> bool:
    """Set given pieces on the board randomly, and ensure the resulting position is valid."""
    if not pieces:
        return not (check_game_over and board.is_game_over())

    piece = pieces[0]
    squares = [s for s in range(64) if not board.piece_at(s)]
    random.shuffle(squares)
    for square in squares:
        board.set_piece_at(square, piece)
        if board.is_valid() and set_randomly(pieces[1:], board, check_game_over=check_game_over):
            return True
        board.remove_piece_at(square)

    return False


def parse_pieces(user_input: str) -> tuple[list[Piece], set[str]]:
    """Parse chess pieces from user input.

    Args:
        user_input: A string represented a user input for a custom
          piece configuration. The allowed piece symbols are P, N,
          B, R, Q, K representing white pieces, and the same symbols
          in lower case for black pieces. Commas and spaces may be
          used to separate symbols and are stripped from the input
          prior to parsing.

    Returns:
        This function returns a list of parsed pieces and a set of
        characters that could not be parsed.
    """
    pieces: list[Piece] = []
    bad_symbols: set[str] = set()
    for c in user_input:
        if c in (",", " "):
            continue
        if c.lower() in PIECE_SYMBOLS:
            pieces.append(Piece.from_symbol(c))
        else:
            bad_symbols.add(c)
    return pieces, bad_symbols


def print_help() -> None:
    piece_input = """
    Provide the symbols of the pieces to place on the board. White
    pieces are P, N, B, R, Q, black pieces are p, n, b, r, q. Kings
    are automatically added and must not be part of the input.
    You can separate piece symbols by commas and/or spaces.
    Examples:

    Qr - queen against rook
    R, p, p - rook against two pawns
    N B B q - knight and two bishops against a queen
    """

    cmd_table = Table(show_header=False, box=None)
    cmd_table.add_row("h", "Help")
    cmd_table.add_row("Enter", "Use previous input")
    cmd_table.add_row("Ctrl+D", "Quit")

    columns = Columns(
        [
            Panel(textwrap.dedent(piece_input), title="Piece Input"),
            Panel(cmd_table, title="Commands"),
        ]
    )
    rprint(columns)


def read_user_input(prompt: str) -> list[Piece]:
    """Prompt user for the next position to generate and parse users' input.

    Args:
        prompt: The user prompt to show in the terminal.

    Returns:
        A list of pieces based on user input. If no selection was made, then
        an empty list is returned.
    """
    try:
        user_input = input(prompt)
    except EOFError:
        raise StopExecutionError from None
    if user_input.lower() == "h":
        raise NeedHelpError
    if not user_input:
        return []

    pieces, bad_symbols = parse_pieces(user_input)
    bad_input = False
    if bad_symbols:
        rprint(f"[red]Unknown pieces: {', '.join(sorted(bad_symbols))}.[/red]")
        bad_input = True
    if WHITE_KING in pieces or BLACK_KING in pieces:
        rprint("[red]Kings are added automatically, adding more kings is not possible.")
        bad_input = True
    if sum(piece.color == WHITE for piece in pieces) > 15:
        rprint("[red]There can not be more than 16 white pieces.[/red]")
        bad_input = True
    if sum(piece.color == BLACK for piece in pieces) > 15:
        rprint("[red]There can not be more than 16 black pieces.[/red]")
        bad_input = True
    if sum(piece == WHITE_PAWN for piece in pieces) > 8:
        rprint("[red]There can not be more than 8 white pawns.[/red]")
        bad_input = True
    if sum(piece == BLACK_PAWN for piece in pieces) > 8:
        rprint("[red]There can not be more than 8 black pawns.[/red]")
        bad_input = True
    if bad_input:
        raise InvalidSelectionError
    return pieces


def loop() -> None:
    print_help()
    prev_pieces: list[Piece] = []
    while True:
        if prev_pieces:
            prev_pieces_str = "".join(str(p) for p in prev_pieces)
            prompt = f"Position (enter = {prev_pieces_str}): "
        else:
            prompt = "Position: "
        try:
            pieces = read_user_input(prompt)
        except StopExecutionError:
            rprint("\nBye!")
            return
        except NeedHelpError:
            print_help()
            continue
        except InvalidSelectionError:
            continue

        if not pieces:
            if not prev_pieces:
                continue
            pieces = prev_pieces
        prev_pieces = pieces

        board = init_board()
        if set_randomly(pieces, board):
            rprint(board)
            rprint(f"https://lichess.org/?fen={quote(board.fen())}#ai")
        else:
            rprint(f"Cannot set {', '.join(str(p) for p in pieces)} on the board:\n{board}")


if __name__ == "__main__":
    main()
