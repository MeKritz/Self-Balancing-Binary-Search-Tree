import csv
import math
import sys
import time

from bst import BST, BSTNode
from avl import AVLTree, AVLNode
from rbtree import RedBlackTree, RBNode
from workload import (DATASETS, SIZES, make_dataset, patient_name,
                      pick_delete_keys, pick_search_keys)

TREES = {                       # name -> (factory, node class)
    "BST": (BST, lambda: BSTNode(1, "x")),
    "AVL": (AVLTree, lambda: AVLNode(1, "x")),
    "RedBlack": (RedBlackTree, lambda: RBNode(1, "x", True)),
}
REPEATS = 2                     # insertion is timed REPEATS times, best kept
FIELDS = ["tree", "dataset", "N", "height", "min_height_floor_log2N",
          "min_height_nodes", "insert_time_s", "insert_rotations",
          "avg_search_comparisons", "height_after_20pct_delete",
          "delete_rotations", "node_bytes"]


def validate(tree, name, expected_keys):
    """Assertions used after every phase (Part B.4)."""
    assert tree.is_bst(), f"{name}: BST property broken"
    if name == "AVL":
        assert tree.is_balanced(), "AVL: balance factor outside {-1,0,1}"
    if name == "RedBlack":
        assert tree.is_valid(), "RedBlack: invariant broken"
    assert tree.inorder() == expected_keys, f"{name}: in-order mismatch"


def run_one(name, dataset, n):
    factory, node_factory = TREES[name]
    keys = make_dataset(dataset, n)

    # ---- insertion (timed; best of REPEATS fresh builds) --------------------
    best = None
    for _ in range(REPEATS):
        tree = factory()
        t0 = time.perf_counter()
        for k in keys:
            tree.insert(k, patient_name(k))
        elapsed = time.perf_counter() - t0
        best = elapsed if best is None else min(best, elapsed)
    validate(tree, name, sorted(keys))
    height = tree.height()
    ins_rot = tree.rotations if name != "BST" else None

    # ---- search: 1,000 random EXISTING ids ----------------------------------
    search_keys = pick_search_keys(keys)
    tree.reset_counters()
    for k in search_keys:
        assert tree.search(k) == patient_name(k)
    avg_cmp = tree.comparisons / len(search_keys)

    # ---- delete a random 20% -------------------------------------------------
    del_keys = pick_delete_keys(keys)
    tree.reset_counters()
    for k in del_keys:
        assert tree.delete(k)
    del_rot = tree.rotations if name != "BST" else None
    gone = set(del_keys)
    validate(tree, name, sorted(k for k in keys if k not in gone))

    min_h = int(math.floor(math.log2(n)))
    return {
        "tree": name, "dataset": dataset, "N": n, "height": height,
        "min_height_floor_log2N": min_h, "min_height_nodes": min_h + 1,
        "insert_time_s": round(best, 4),
        "insert_rotations": "NA" if ins_rot is None else ins_rot,
        "avg_search_comparisons": round(avg_cmp, 2),
        "height_after_20pct_delete": tree.height(),
        "delete_rotations": "NA" if del_rot is None else del_rot,
        "node_bytes": sys.getsizeof(node_factory()),
    }


def run_all(verbose=True):
    rows = []
    for dataset in DATASETS:
        for n in SIZES:
            for name in TREES:
                if verbose:
                    print(f"  running {name:8s} {dataset:13s} N={n} ...", flush=True)
                rows.append(run_one(name, dataset, n))
    return rows


def print_table(rows):
    heads = ["tree", "dataset", "N", "height", "min_h*", "ins_time_s",
             "ins_rot", "avg_cmp", "h_after_del", "del_rot", "node_B"]
    keys = ["tree", "dataset", "N", "height", "min_height_nodes",
            "insert_time_s", "insert_rotations", "avg_search_comparisons",
            "height_after_20pct_delete", "delete_rotations", "node_bytes"]
    widths = [10, 15, 7, 8, 8, 12, 9, 10, 13, 9, 8]
    print("".join(h.rjust(w) for h, w in zip(heads, widths)))
    for r in rows:
        print("".join(str(r[k]).rjust(w) for k, w in zip(keys, widths)))
    print("* min_h = floor(log2 N) + 1 = minimum possible height counted in nodes "
          "(the lab's floor(log2 N) is the same bound counted in edges).")


def save_csv(rows, path="results.csv"):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    print("Running experiments (plain BST on sequential N=10,000 is slow: be patient)")
    results = run_all()
    print()
    print_table(results)
    save_csv(results)
    print("\nSaved results.csv")
