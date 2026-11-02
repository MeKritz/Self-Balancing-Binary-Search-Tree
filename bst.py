"""Part A: plain (unbalanced) Binary Search Tree.

Stores a Patient ID (int key) and a Patient Name (str value).

Design choices
--------------
* insert, search, delete, in-order traversal and height are all ITERATIVE.
  This is the "iterative insert" option from the lab sheet: a sequential
  workload with N = 10,000 gives a tree 10,000 levels deep, which would
  blow Python's default recursion limit (1000) if we used recursion.
* Height is counted in NODES (empty tree = 0, single node = 1), which is
  the convention used in the lab sheet's sample output (chain of 5 -> 5).
* Comparison counting: one comparison is counted for every node whose key
  is examined (a three-way "less / equal / greater" decision = 1 comparison).
  A successful search for a node at depth d (root = depth 1) therefore costs
  exactly d comparisons.
"""


class BSTNode:
    """A single tree node. __slots__ keeps memory small and measurable."""
    __slots__ = ("key", "value", "left", "right")

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class BST:
    """Plain binary search tree with no rebalancing."""

    def __init__(self):
        self.root = None
        self._size = 0
        self.comparisons = 0   # key comparisons made since last reset
        self.rotations = 0     # always 0 for a plain BST (kept for a common interface)

    # ------------------------------------------------------------------ utils
    def __len__(self):
        return self._size

    def reset_counters(self):
        self.comparisons = 0
        self.rotations = 0

    # ----------------------------------------------------------------- insert
    def insert(self, key, value):
        """Insert (key, value). If the key already exists, update its value."""
        new = BSTNode(key, value)
        if self.root is None:
            self.root = new
            self._size = 1
            return
        cur = self.root
        while True:
            self.comparisons += 1
            if key == cur.key:            # duplicate ID: overwrite name
                cur.value = value
                return
            if key < cur.key:
                if cur.left is None:
                    cur.left = new
                    break
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = new
                    break
                cur = cur.right
        self._size += 1

    # ----------------------------------------------------------------- search
    def search(self, key):
        """Return the value stored for key, or None if the key is absent."""
        cur = self.root
        while cur is not None:
            self.comparisons += 1
            if key == cur.key:
                return cur.value
            cur = cur.left if key < cur.key else cur.right
        return None

    # ----------------------------------------------------------------- delete
    def delete(self, key):
        """Delete key. Returns True if it was present, False otherwise.

        Handles the three classic cases:
          1. leaf            -> just unlink it
          2. one child       -> replace it by its child
          3. two children    -> copy in-order successor (smallest key of the
                                right subtree) into this node, then delete
                                the successor (which has at most one child).
        """
        parent, cur = None, self.root
        while cur is not None and cur.key != key:
            self.comparisons += 1
            parent = cur
            cur = cur.left if key < cur.key else cur.right
        if cur is None:
            return False
        self.comparisons += 1              # the successful equality test

        if cur.left is not None and cur.right is not None:       # case 3
            succ_parent, succ = cur, cur.right
            while succ.left is not None:
                succ_parent, succ = succ, succ.left
            cur.key, cur.value = succ.key, succ.value
            parent, cur = succ_parent, succ                        # now remove succ

        child = cur.left if cur.left is not None else cur.right   # cases 1 & 2
        if parent is None:
            self.root = child
        elif parent.left is cur:
            parent.left = child
        else:
            parent.right = child
        self._size -= 1
        return True

    # -------------------------------------------------------------- traversal
    def inorder(self):
        """Return the list of keys in ascending order (iterative)."""
        out, stack, cur = [], [], self.root
        while stack or cur is not None:
            while cur is not None:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            out.append(cur.key)
            cur = cur.right
        return out

    # ----------------------------------------------------------------- height
    def height(self):
        """Height in nodes, computed iteratively (works on 10,000-deep trees)."""
        if self.root is None:
            return 0
        best, stack = 0, [(self.root, 1)]
        while stack:
            node, depth = stack.pop()
            best = max(best, depth)
            if node.left is not None:
                stack.append((node.left, depth + 1))
            if node.right is not None:
                stack.append((node.right, depth + 1))
        return best

    # ------------------------------------------------------------------ check
    def is_bst(self):
        """BST-property check: in-order keys strictly increase and count matches."""
        keys = self.inorder()
        return len(keys) == self._size and all(a < b for a, b in zip(keys, keys[1:]))
