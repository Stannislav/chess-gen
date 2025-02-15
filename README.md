# ♟️Chess Gen♟️

Generate chess positions and practise on Lichess.

The generated positions are random, which is different to Lichess' presets.

## Example

```shell
$ chessg
Generate chess positions and practise on Lichess.
╭─ Positions ─╮ ╭──────────── Commands ────────────╮
│  1  R       │ │  h          Help                 │
│  2  Q       │ │  enter      Use previous choice  │
│  3  B+B     │ │  q, Ctrl+D  Quit                 │
│  4  B+N     │ ╰──────────────────────────────────╯
│  5  N+N     │                                     
╰─────────────╯                                     
Choice: 3
. . . . k . . .
. . . . . . . .
. . . . . . . .
. . . . B B . .
. . . . . . . .
. . . . . . . .
. . . . . K . .
. . . . . . . .
https://lichess.org/?fen=4k3/8/8/4BB2/8/8/5K2/8%20w%20-%20-%200%201#ai
Choice: ^D
Bye!
```

## Installation

```shell
pip install chess-gen
```
