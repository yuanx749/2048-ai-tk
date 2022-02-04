[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/yuanx749/2048-ai-tk.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/yuanx749/2048-ai-tk/context:python)

# 2048-ai-tk
Minimax with alpha–beta pruning and iterative deepening, ~90% win rate.

Tkinter GUI, no additional package required on Windows.
```
sudo apt install python3-tk
python game.py
```

Optimizations:
- Order nodes to maximize pruning.
- Memorization in iterative deepening.

Some heuristics:
- available cells
- potential merging
- average, median, max tile
- difference between adjacent tiles
- score and penalty of ordering across rows, columns

Modules:
- `grid.py`: Contains class that represents the 2048 board.
- `game.py`: Driver that runs the game in GUI.
- `minimax.py`: Minimax implementation, reusable in other games.
- `player_ai.py`: Minimax for 2048.

---
![2048](4096.png)
