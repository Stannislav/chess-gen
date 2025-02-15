"""Generate chess positions and practise on Lichess."""
from __future__ import annotations

import argparse
import random
from urllib.parse import quote

from chess import BLACK, Board, Piece, WHITE
from rich import print
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table

__version__ = "1.0.0"


def main() -> None:
    description = "Generate chess positions and practise on Lichess."
    parser = argparse.ArgumentParser(description=description)
    parser.parse_args()
    print(description)

    Program().loop()


def init_board() -> Board:
    """Generate a legal board with two kings only."""
    board = Board()
    board.clear()
    board.set_piece_at(random.randint(0, 63), Piece.from_symbol("K"))
    set_randomly([Piece.from_symbol("k")], board, check_game_over=False)

    return board


def set_randomly(pieces: list[Piece], board: Board, check_game_over: bool = True) -> bool:
    """Set the piece on a random legal square on the board."""
    if not pieces:
        return not (check_game_over and board.is_game_over())

    piece = pieces[0]
    squares = [s for s in range(64) if not board.piece_at(s)]
    random.shuffle(squares)
    for square in squares:
        board.set_piece_at(square, piece)
        if board.is_valid() and set_randomly(pieces[1:], board, check_game_over):
            return True
        board.remove_piece_at(square)

    return False


class Program:
    CUSTOM = "Custom"

    def __init__(self):
        self.positions = {
            "Q": [Piece.from_symbol("Q")],
            "R": [Piece.from_symbol("R")],
            "B+B": [Piece.from_symbol("B"), Piece.from_symbol("B")],
            "B+N": [Piece.from_symbol("B"), Piece.from_symbol("N")],
            self.CUSTOM: [],
        }
        self.choices = {str(i): key for i, key in enumerate(self.positions, 1)}
        self.prev_choice = ""
        self.prev_pieces = []

    def print_help(self) -> None:
        pos_table = Table(show_header=False, box=None)
        for i, key in self.choices.items():
            pos_table.add_row(i, key)
        cmd_table = Table(show_header=False, box=None)
        cmd_table.add_row("h", "Help")
        cmd_table.add_row("enter", "Use previous choice")
        cmd_table.add_row("q, Ctrl+D", "Quit")
        columns = Columns([
            Panel(pos_table, title="Positions"),
            Panel(cmd_table, title="Commands")
        ])
        print(columns)

    def loop(self) -> None:
        self.print_help()
        while True:
            try:
                if self.prev_choice:
                    if self.choices[self.prev_choice] == self.CUSTOM and self.prev_pieces:
                        prompt = f"Position (enter = {self.CUSTOM} - {''.join(str(p) for p in self.prev_pieces)}): "
                    else:
                        prompt = f"Position (enter = {self.choices[self.prev_choice]}): "
                else:
                    prompt = "Position: "
                choice = input(prompt).lower()
            except EOFError:
                choice = "q"
            if choice == "q":
                print("\nBye!")
                return
            if choice == "h":
                self.print_help()
                continue
            if not choice:
                choice = self.prev_choice
            if choice not in self.choices:
                print("[red]Please enter a valid choice.[/red]")
                continue

            position_idx = self.choices[choice]
            self.prev_choice = choice

            if position_idx == "Custom":
                pieces = self.read_custom()
                if pieces is None:
                    continue
                if len(pieces) == 0:
                    print(f"[red]No pieces selected.")
                    continue
                self.prev_pieces = pieces
            else:
                pieces = self.positions[self.choices[choice]]

            board = init_board()
            if set_randomly(pieces, board):
                print(board)
                print(f"https://lichess.org/?fen={quote(board.fen())}#ai")
            else:
                print(f"Cannot set {', '.join(str(p) for p in pieces)} on the board:\n{board}")

    @staticmethod
    def read_custom() -> list[Piece] | None:
        # Get input
        print("[green]Enter custom pieces. White: QRNBP, black: qrnbp.[/green]")
        piece_choice = input("Pieces: ")

        # Parse input
        bad_symbols = []
        pieces = []
        for symbol in [c for c in piece_choice if c and c != ","]:
            if symbol == "K" or symbol == "k":
                bad_symbols.append(symbol)
            try:
                piece = Piece.from_symbol(symbol)
            except ValueError:
                bad_symbols.append(symbol)
            else:
                pieces.append(piece)
        if bad_symbols:
            print(f"[red]Unknown piece(s): {', '.join(bad_symbols)}.[/red]")
            return None

        # Validate input
        bad_input = False
        if sum(piece.color == WHITE for piece in pieces) > 15:
            print(f"[red]There can not be more than 16 white pieces.[/red]")
            bad_input = True
        if sum(piece.color == BLACK for piece in pieces) > 15:
            print(f"[red]There can not be more than 16 black pieces.[/red]")
            bad_input = True
        if sum(piece.color == BLACK for piece in pieces) > 15:
            print(f"[red]There can not be more than 16 black pieces.[/red]")
            bad_input = True
        if sum(piece == Piece.from_symbol("P") for piece in pieces) > 8:
            print(f"[red]There can not be more than 8 white pawns.[/red]")
            bad_input = True
        if sum(piece == Piece.from_symbol("p") for piece in pieces) > 8:
            print(f"[red]There can not be more than 8 black pawns.[/red]")
            bad_input = True
        if bad_input:
            return None

        return pieces


if __name__ == "__main__":
    main()
