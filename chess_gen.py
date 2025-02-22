"""Generate chess positions and practise on Lichess."""

from __future__ import annotations

import argparse
import random
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


def main() -> None:
    description = "Generate chess positions and practise on Lichess."
    parser = argparse.ArgumentParser(description=description)
    parser.parse_args()
    rprint(description)
    Program().loop()


def init_board() -> Board:
    """Generate a legal board with two kings only."""
    board = Board()
    board.clear()
    board.set_piece_at(random.randint(0, 63), Piece.from_symbol("K"))
    set_randomly([Piece.from_symbol("k")], board, check_game_over=False)

    return board


def set_randomly(pieces: list[Piece], board: Board, *, check_game_over: bool = True) -> bool:
    """Set the piece on a random legal square on the board."""
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


class Program:
    def __init__(self) -> None:
        self.presets = {
            "Q": [Piece.from_symbol("Q")],
            "R": [Piece.from_symbol("R")],
            "B+B": [Piece.from_symbol("B"), Piece.from_symbol("B")],
            "B+N": [Piece.from_symbol("B"), Piece.from_symbol("N")],
        }
        self.preset_choices = {str(i): key for i, key in enumerate(self.presets, 1)}
        self.prev_pieces: list[Piece] = []

    def print_help(self) -> None:
        pos_table = Table(show_header=False, box=None)
        for i, key in self.preset_choices.items():
            pos_table.add_row(i, key)
        cmd_table = Table(show_header=False, box=None)
        cmd_table.add_row("h", "Help")
        cmd_table.add_row("enter", "Use previous choice")
        cmd_table.add_row("Ctrl+D", "Quit")
        columns = Columns([Panel(pos_table, title="Presets"), Panel(cmd_table, title="Commands")])
        rprint(columns)

    def loop(self) -> None:
        self.print_help()
        while True:
            if self.prev_pieces:
                prev_pieces_str = "".join(str(p) for p in self.prev_pieces)
                prompt = f"Position (enter = {prev_pieces_str}): "
            else:
                prompt = "Position: "
            try:
                choice = input(prompt)
            except EOFError:
                rprint("\nBye!")
                return
            if choice.lower() == "h":
                self.print_help()
                continue
            if choice:
                if choice.isdecimal():
                    if choice not in self.preset_choices:
                        rprint(
                            f"[red]Not a valid preset choice: {choice}. "
                            "Please choose one of the following: "
                            f"{', '.join(sorted(self.preset_choices))}.[/red]"
                        )
                        continue
                    pieces = self.presets[self.preset_choices[choice]]
                else:
                    pieces, bad_symbols = parse_pieces(choice)
                    bad_input = False
                    if bad_symbols:
                        rprint(f"[red]Unknown pieces: {', '.join(sorted(bad_symbols))}.[/red]")
                        bad_input = True
                    if WHITE_KING in pieces or BLACK_KING in pieces:
                        rprint(
                            "[red]Kings are added automatically, adding more kings is not possible."
                        )
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
                        continue
            else:
                if not self.prev_pieces:
                    continue
                pieces = self.prev_pieces

            self.prev_pieces = pieces

            board = init_board()
            if set_randomly(pieces, board):
                rprint(board)
                rprint(f"https://lichess.org/?fen={quote(board.fen())}#ai")
            else:
                rprint(f"Cannot set {', '.join(str(p) for p in pieces)} on the board:\n{board}")


if __name__ == "__main__":
    main()
