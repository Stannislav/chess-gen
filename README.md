# Chess Gen
[![Latest PyPi version](https://img.shields.io/pypi/v/chess-gen.svg)](https://pypi.org/project/chess-gen/)

Generate chess positions and practise on Lichess.

The generated positions are random, which is different to Lichess' presets.

## Example

```text
$ chessg
Generate chess positions and practise on Lichess.
╭─ Positions ─╮ ╭──────────── Commands ────────────╮
│  1  Q       │ │  h          Help                 │
│  2  R       │ │  enter      Use previous choice  │
│  3  B+B     │ │  q, Ctrl+D  Quit                 │
│  4  B+N     │ ╰──────────────────────────────────╯
│  5  Custom  │                                     
╰─────────────╯                                     
Position: 4
. . K . . . . .
. . . B . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . k . . .
. . . . . . . N
. . . . . . . .
https://lichess.org/?fen=2K5/3B4/8/8/8/4k3/7N/8%20w%20-%20-%200%201#ai
Choice: ^D
Bye!
```

## Installation

```shell
pip install chess-gen
```
