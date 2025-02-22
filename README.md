# Chess Gen
[![Latest PyPi version](https://img.shields.io/pypi/v/chess-gen.svg)](https://pypi.org/project/chess-gen/)

Generate chess positions and practise on Lichess.

The generated positions are random, which is different to Lichess' presets.

## Example

```text
$ chessg
╭────────────────────────── Piece Input ──────────────────────────╮ ╭────────── Commands ──────────╮
│ Generate chess positions and practise on Lichess.               │ │  h       Help                │
│                                                                 │ │  Enter   Use previous input  │
│ Provide the symbols of the pieces to place on the board. White  │ │  Ctrl+D  Quit                │
│ pieces are P, N, B, R, Q, black pieces are p, n, b, r, q. Kings │ ╰──────────────────────────────╯
│ are automatically added and must not be part of the input.      │                                 
│ You can separate piece symbols by commas and/or spaces.         │                                 
│                                                                 │                                 
│ Examples:                                                       │                                 
│                                                                 │                                 
│ Qr - queen against rook                                         │                                 
│ R, p, p - rook against two pawns                                │                                 
│ N B B q - knight and two bishops against a queen                │                                 
│                                                                 │                                 
╰─────────────────────────────────────────────────────────────────╯                                 
Position: BN 
. . . k . . . .
. . . . . . . .
. . . . . . . .
. N . . . . . .
. . . . . . . .
B . . . . . . .
. . . . K . . .
. . . . . . . .
https://lichess.org/?fen=3k4/8/8/1N6/8/B7/4K3/8%20w%20-%20-%200%201#ai
Position (enter = BN): ^D
Bye!
```

## Installation

```shell
pip install chess-gen
```
