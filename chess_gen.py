"""Generate chess positions and practise on Lichess."""

from __future__ import annotations

import argparse
import random
from typing import Final
from urllib.parse import quote

from chess import BLACK, PIECE_SYMBOLS, WHITE, Board, Piece
from rich import print as rprint
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table

__version__ = "1.0.0"

WHITE_PAWN = Piece.from_symbol("P")
BLACK_PAWN = Piece.from_symbol("p")


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


class Program:
    CUSTOM: Final[str] = "Custom"

    def __init__(self) -> None:
        self.positions = {
            "Q": [Piece.from_symbol("Q")],
            "R": [Piece.from_symbol("R")],
            "B+B": [Piece.from_symbol("B"), Piece.from_symbol("B")],
            "B+N": [Piece.from_symbol("B"), Piece.from_symbol("N")],
            self.CUSTOM: [],
        }
        self.choices = {str(i): key for i, key in enumerate(self.positions, 1)}
        self.prev_choice = ""
        self.prev_pieces: list[Piece] = []

    def print_help(self) -> None:
        pos_table = Table(show_header=False, box=None)
        for i, key in self.choices.items():
            pos_table.add_row(i, key)
        cmd_table = Table(show_header=False, box=None)
        cmd_table.add_row("h", "Help")
        cmd_table.add_row("enter", "Use previous choice")
        cmd_table.add_row("q, Ctrl+D", "Quit")
        columns = Columns([Panel(pos_table, title="Positions"), Panel(cmd_table, title="Commands")])
        rprint(columns)

    def loop(self) -> None:
        self.print_help()
        while True:
            try:
                if self.prev_choice:
                    if self.choices[self.prev_choice] == self.CUSTOM and self.prev_pieces:
                        prev_pieces_str = "".join(str(p) for p in self.prev_pieces)
                        prompt = f"Position (enter = {self.CUSTOM} - {prev_pieces_str}): "
                    else:
                        prompt = f"Position (enter = {self.choices[self.prev_choice]}): "
                else:
                    prompt = "Position: "
                choice = input(prompt).lower()
            except EOFError:
                choice = "q"
            if choice == "q":
                rprint("\nBye!")
                return
            if choice == "h":
                self.print_help()
                continue
            if not choice:
                choice = self.prev_choice
            else:
                self.prev_pieces.clear()
            if choice not in self.choices:
                rprint("[red]Please enter a valid choice.[/red]")
                continue
            self.prev_choice = choice

            position_idx = self.choices[choice]
            if position_idx == self.CUSTOM:
                pieces = self.prev_pieces or self.read_custom()
                if not pieces:
                    continue
                self.prev_pieces = pieces
            else:
                pieces = self.positions[self.choices[choice]]

            board = init_board()
            if set_randomly(pieces, board):
                rprint(board)
                rprint(f"https://lichess.org/?fen={quote(board.fen())}#ai")
            else:
                rprint(f"Cannot set {', '.join(str(p) for p in pieces)} on the board:\n{board}")

    @staticmethod
    def read_custom() -> list[Piece]:
        while True:
            # Read input
            prompt = "Enter custom pieces (QRNBPqrnbp, enter = abort):"
            rprint(f"[green]{prompt}[/green] ", end="", flush=True)
            piece_choice = input()
            if not piece_choice:
                return []

            # Parse input
            bad_symbols = set()
            pieces = []
            for symbol in [c for c in piece_choice if c and c != ","]:
                if symbol == "K" or symbol == "k" or symbol.lower() not in PIECE_SYMBOLS:
                    bad_symbols.add(symbol)
                else:
                    pieces.append(Piece.from_symbol(symbol))
            if bad_symbols:
                rprint(f"[red]Unknown pieces: {', '.join(sorted(bad_symbols))}.[/red]")
                continue

            # Validate input
            bad_input = False
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

            return pieces


if __name__ == "__main__":
    main()
