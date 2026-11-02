# Lab 6: Self-Balancing BST (AVL) vs Plain BST, MediQueue

Python 3, standard library only (matplotlib needed only for the graphs).
No built-in tree classes are used; all node structures are hand-written.

## Files

| File | Purpose |
|---|---|
| `bst.py` | Part A: plain BST (iterative insert/search/delete/inorder/height, comparison counter) |
| `avl.py` | Part B: AVL tree (height field, balance factor, LL/RR/LR/RL rotations, rotation counter, `is_balanced()`) |
| `workload.py` | Part C: seeded sequential / random / nearly-sorted datasets (seed = 42) |
| `experiments.py` | Part D: runs every tree x dataset x size, prints the table, writes `results.csv` |
| `plots.py` | Part D: graphs (`graph1/2/3_*.png`) from `results.csv` |
| `rbtree.py` | Section 6 self-learning: Red-Black tree |
| `tests.py` | Assertions (all delete cases, 4 rotation cases, random stress tests vs a dict) |
| `demo.py` | Live demo: the lab sheet's sample, or the examiner's own IDs |
| `ANALYSIS.md` | Part E analysis |
| `SELF_LEARNING.md` | Section 6 note (Red-Black tree) |

## How to run

```
python tests.py                 # 11 tests, should print "All 11 tests passed."
python demo.py                  # sample: 10 20 30 40 50 25
python demo.py 5 4 3 2 1 6      # examiner's input
python experiments.py           # full comparison table + results.csv (about 30 s)
pip install matplotlib          # only if missing
python plots.py                 # writes the 3 PNG graphs
```

Captured output of my own runs: `demo_output.txt`, `experiment_output.txt`, `results.csv`.

## Design decisions (be ready to explain these in the viva)

* **Iterative plain BST.** insert, delete, height and traversal are loops, not recursion,
  because a sequential N = 10,000 gives a 10,000-level tree (Python's limit is ~1000).
  AVL/Red-Black recursion is safe: their depth is only about 15-25.
* **Height is counted in nodes** (empty = 0, one node = 1), matching the lab sheet's sample
  (a chain of 5 nodes has height 5). The sheet's "floor(log2 N)" minimum is the same bound
  counted in edges, so the table's `min_height_nodes` column = floor(log2 N) + 1.
  Both columns are in `results.csv`.
* **Comparison counter:** one comparison per node whose key is examined (less / equal /
  greater is one three-way decision). A successful search for a node at depth d costs d.
* **Rotations:** each single rotation counts 1, so a double rotation (LR / RL) counts 2.
  This reproduces the sample (4 rotations for 10, 20, 30, 40, 50, 25).
* **Nearly sorted:** ascending IDs, then N x 5% / 2 random pair swaps, so about 5% of positions move.
* **Timing:** best of 2 fresh builds; absolute times depend on the machine, the
  height / comparison / rotation counts do not.
* **Search workload:** 1,000 random existing IDs (all N when N = 1,000).
  **Deletes:** a random 20% of keys. After every phase each tree is validated
  (BST property, AVL balance, Red-Black invariants, in-order list equals the expected sorted keys).
