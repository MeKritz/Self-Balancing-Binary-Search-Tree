"""Correctness tests for BST, AVL and Red-Black trees.

Run:  python tests.py        (plain asserts, no external libraries needed)
"""
import random

from bst import BST
from avl import AVLTree
from rbtree import RedBlackTree
from workload import patient_name


def build(tree, keys):
    for k in keys:
        tree.insert(k, patient_name(k))
    return tree


# ------------------------------------------------------------------ BST (A)
def test_bst_sample():
    t = build(BST(), [10, 20, 30, 40, 50, 25])
    assert t.root.key == 10 and t.height() == 5 and t.rotations == 0
    assert t.inorder() == [10, 20, 25, 30, 40, 50]
    assert t.search(25) == "Patient_25" and t.search(99) is None


def test_bst_delete_all_cases():
    t = build(BST(), [50, 30, 70, 20, 40, 60, 80, 35, 45, 65])
    assert t.delete(20) and t.inorder() == [30, 35, 40, 45, 50, 60, 65, 70, 80]   # leaf
    assert t.delete(60) and t.search(65) is not None and t.is_bst()               # one child (right)
    assert t.delete(30) and t.search(35) is not None and t.is_bst()               # one child (left)
    assert t.delete(50) and t.root.key == 65 and t.is_bst()                       # root, two children
    assert t.delete(70) and t.is_bst()                                             # two children
    assert not t.delete(1234)                                                      # absent key
    assert len(t) == len(t.inorder())


def test_bst_delete_down_to_empty():
    t = build(BST(), [2, 1, 3])
    for k in (2, 1, 3):
        assert t.delete(k)
    assert t.root is None and t.height() == 0 and len(t) == 0


def test_bst_degenerates_but_does_not_recurse():
    t = build(BST(), range(1, 10001))        # sequential 10,000 -> 10,000 levels
    assert t.height() == 10000 and t.is_bst()
    t.reset_counters()
    t.search(10000)
    assert t.comparisons == 10000


# ------------------------------------------------------------------ AVL (B)
def test_avl_sample():
    t = build(AVLTree(), [10, 20, 30, 40, 50, 25])
    assert t.root.key == 30 and t.height() == 3 and t.rotations == 4
    assert t.inorder() == [10, 20, 25, 30, 40, 50]
    assert t.is_balanced() and t.is_bst()


def test_avl_four_rotation_cases():
    cases = {                       # name: (insertion order, rotations expected)
        "LL": ([30, 20, 10], 1),
        "RR": ([10, 20, 30], 1),
        "LR": ([30, 10, 20], 2),
        "RL": ([10, 30, 20], 2),
    }
    for name, (keys, rots) in cases.items():
        t = build(AVLTree(), keys)
        assert t.root.key == 20 and t.height() == 2, name
        assert t.rotations == rots, name
        assert t.is_balanced() and t.is_bst(), name


def test_avl_delete_rebalances():
    t = build(AVLTree(), range(1, 16))              # perfect tree, height 4
    assert t.height() == 4
    before = t.rotations
    for k in (8, 9, 10, 11, 12, 13, 14, 15):        # strip the right side
        assert t.delete(k)
        assert t.is_balanced() and t.is_bst()
    assert t.rotations > before                      # deletes triggered rotations
    assert t.inorder() == [1, 2, 3, 4, 5, 6, 7]
    assert t.height() == 3


def test_avl_sequential_height_is_logarithmic():
    t = build(AVLTree(), range(1, 10001))
    assert t.is_balanced() and t.height() <= 15       # 1.44*log2(10001) ~ 19 bound; actual 14
    assert t.rotations > 0


# -------------------------------------------------------- random stress tests
def stress(make_tree, check, seed, ops=3000, universe=400):
    """Random inserts/deletes compared against a Python dict as the oracle,
    validating the tree invariants after EVERY operation."""
    rng = random.Random(seed)
    t, model = make_tree(), {}
    for _ in range(ops):
        k = rng.randrange(universe)
        if rng.random() < 0.55:
            t.insert(k, patient_name(k))
            model[k] = patient_name(k)
        else:
            assert t.delete(k) == (k in model)
            model.pop(k, None)
        assert check(t)
        assert len(t) == len(model)
    assert t.inorder() == sorted(model)
    for k in range(universe):
        assert (t.search(k) is not None) == (k in model)


def test_stress_all_trees():
    stress(BST, lambda t: t.is_bst(), seed=1)
    stress(AVLTree, lambda t: t.is_balanced() and t.is_bst(), seed=2)
    stress(RedBlackTree, lambda t: t.is_valid(), seed=3)


def test_duplicate_insert_updates_value():
    for cls in (BST, AVLTree, RedBlackTree):
        t = cls()
        t.insert(5, "Old")
        t.insert(5, "New")
        assert len(t) == 1 and t.search(5) == "New"


# --------------------------------------------------------------- Red-Black
def test_rb_sample_and_bound():
    t = build(RedBlackTree(), [10, 20, 30, 40, 50, 25])
    assert t.is_valid() and t.inorder() == [10, 20, 25, 30, 40, 50]
    t = build(RedBlackTree(), range(1, 10001))
    assert t.is_valid() and t.height() <= 2 * 14      # 2*log2(n+1) ~ 26.6


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    for name, fn in tests:
        fn()
        print(f"PASS  {name}")
    print(f"\nAll {len(tests)} tests passed.")
