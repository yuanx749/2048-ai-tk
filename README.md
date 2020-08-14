# 2048-ai-tk
Minimax with alpha–beta pruning and iterative deepening, ~90% win rate.

Tkinter GUI, no additional package required on Windows.
```
sudo apt install python3-tk
python Game.py
```
Some heuristics:
- available cells
- potential merging
- average, median, max tile
- difference between adjacent tiles
- score and penalty of ordering across rows, columns
---
![2048](4096.png)