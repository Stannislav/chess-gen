"""Generate chess positions and practise on Lichess."""
import argparse
import random
from urllib.parse import quote

from chess import Board, Piece
from rich import print
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table

__version__ = "1.0.0"


def print_help(choices: dict[str, str]) -> None:
    pos_table = Table(show_header=False, box=None)
    for i, key in choices.items():
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


def main() -> None:
    description = "Generate chess positions and practise on Lichess."
    parser = argparse.ArgumentParser(description=description)
    parser.parse_args()
    print(description)
    loop()


def loop() -> None:
    positions = {
        "R": [Piece.from_symbol("R")],
        "Q": [Piece.from_symbol("Q")],
        "B+B": [Piece.from_symbol("B"), Piece.from_symbol("B")],
        "B+N": [Piece.from_symbol("B"), Piece.from_symbol("N")],
        "N+N": [Piece.from_symbol("N"), Piece.from_symbol("N")],
    }
    choices = {str(i): key for i, key in enumerate(positions, 1)}
    prev_choice = ""
    print_help(choices)
    while True:
        try:
            choice = input("Choice: ").lower()
        except EOFError:
            choice = "q"
        if choice == "q":
            print("\nBye!")
            return
        if choice == "h":
            print_help(choices)
            continue
        if not choice:
            choice = prev_choice
        if choice not in choices:
            continue

        board = init_board()
        pieces = positions[choices[choice]]
        if set_randomly(pieces, board):
            print(board)
            print(f"https://lichess.org/?fen={quote(board.fen())}#ai")
        else:
            print(f"Cannot set {', '.join(str(p) for p in pieces)} on the board:\n{board}")
        prev_choice = choice


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


if __name__ == "__main__":
    main()
