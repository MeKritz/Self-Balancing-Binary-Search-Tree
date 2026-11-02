"""Small helpers shared by all tree implementations."""


def tree_lines(node, depth=0, out=None):
    """Return a sideways picture of a tree (right subtree on top).

    Works for BST/AVL nodes (None children) and for the Red-Black tree
    (sentinel node whose key is None). Recursive, so only use it for the
    small demo trees, not for 10,000-node degenerate trees.
    """
    if out is None:
        out = []
    if node is None or node.key is None:
        return out
    tree_lines(node.right, depth + 1, out)
    out.append("    " * depth + str(node.key))
    tree_lines(node.left, depth + 1, out)
    return out


def print_tree(root):
    print("\n".join(tree_lines(root)) or "(empty)")
