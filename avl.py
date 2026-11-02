"""Part B: AVL tree (self-balancing BST).

Same public interface as bst.BST (insert / search / delete / inorder /
height / is_bst / comparisons) plus:
    rotations     total number of single rotations performed
    is_balanced() every node: stored height correct and balance factor in {-1,0,+1}

Balance factor of a node = height(left subtree) - height(right subtree).

Rebalancing cases (n = first unbalanced node):
    Left-Left    bf(n) > +1 and bf(n.left)  >= 0 -> right rotation at n
    Left-Right   bf(n) > +1 and bf(n.left)  <  0 -> left rotation at n.left, then right at n
    Right-Right  bf(n) < -1 and bf(n.right) <= 0 -> left rotation at n
    Right-Left   bf(n) < -1 and bf(n.right) >  0 -> right rotation at n.right, then left at n

A double rotation counts as TWO rotations (two single rotations are performed).
Rebalancing runs on the way back up after BOTH insert and delete.

Recursion is safe here: an AVL tree with 10^7 nodes is under ~35 levels deep.
"""
from bst import BST


class AVLNode:
    __slots__ = ("key", "value", "left", "right", "height")

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1          # a leaf has height 1 (nodes convention)


def _h(node):
    return node.height if node is not None else 0


def _update(node):
    node.height = 1 + max(_h(node.left), _h(node.right))


def _balance_factor(node):
    return _h(node.left) - _h(node.right) if node is not None else 0


class AVLTree(BST):
    """AVL tree. Inherits search / inorder / is_bst / counters from BST
    (nodes have the same key/value/left/right fields)."""

    # ------------------------------------------------------------- rotations
    def _rotate_right(self, y):
        """      y            x
                / \\          / \\
               x   C  --->  A   y
              / \\              / \\
             A   B            B   C        """
        x = y.left
        y.left = x.right
        x.right = y
        _update(y)
        _update(x)
        self.rotations += 1
        return x

    def _rotate_left(self, x):
        """    x                y
              / \\              / \\
             A   y    --->    x   C
                / \\          / \\
               B   C        A   B          """
        y = x.right
        x.right = y.left
        y.left = x
        _update(x)
        _update(y)
        self.rotations += 1
        return y

    def _rebalance(self, node):
        """Refresh height, then fix an imbalance at node (if any). Returns the
        new root of this subtree."""
        _update(node)
        bf = _balance_factor(node)
        if bf > 1:                                   # left heavy
            if _balance_factor(node.left) < 0:       # Left-Right case
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)          # Left-Left (or after LR fix)
        if bf < -1:                                  # right heavy
            if _balance_factor(node.right) > 0:      # Right-Left case
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)           # Right-Right (or after RL fix)
        return node

    # ---------------------------------------------------------------- insert
    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if node is None:
            self._size += 1
            return AVLNode(key, value)
        self.comparisons += 1
        if key == node.key:
            node.value = value
            return node
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        else:
            node.right = self._insert(node.right, key, value)
        return self._rebalance(node)

    # ---------------------------------------------------------------- delete
    def delete(self, key):
        self._found = False
        self.root = self._delete(self.root, key)
        if self._found:
            self._size -= 1
        return self._found

    def _delete(self, node, key):
        if node is None:
            return None
        self.comparisons += 1
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            self._found = True
            if node.left is None:                    # leaf or only right child
                return node.right
            if node.right is None:                   # only left child
                return node.left
            succ = node.right                        # two children: in-order successor
            while succ.left is not None:
                succ = succ.left
            node.key, node.value = succ.key, succ.value
            node.right = self._delete(node.right, succ.key)
        return self._rebalance(node)

    # ---------------------------------------------------------------- height
    def height(self):
        """O(1): the root stores the height of the whole tree."""
        return _h(self.root)

    # ---------------------------------------------------------------- checks
    def is_balanced(self):
        """True iff every node's stored height is correct and its balance
        factor is in {-1, 0, +1}."""
        def check(node):                 # returns real height, or -1 if violated
            if node is None:
                return 0
            lh = check(node.left)
            if lh < 0:
                return -1
            rh = check(node.right)
            if rh < 0:
                return -1
            if abs(lh - rh) > 1 or node.height != 1 + max(lh, rh):
                return -1
            return 1 + max(lh, rh)
        return check(self.root) >= 0
