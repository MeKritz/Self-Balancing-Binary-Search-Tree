"""Part C: workload generation (all functions are seeded => reproducible)."""
import random

SEED = 42
SIZES = (1000, 5000, 10000)
DATASETS = ("sequential", "random", "nearly_sorted")


def sequential(n, seed=SEED):
    """Dataset 1: IDs 1..n ascending (the MediQueue production pattern)."""
    return list(range(1, n + 1))


def random_permutation(n, seed=SEED):
    """Dataset 2: random permutation of 1..n."""
    ids = list(range(1, n + 1))
    random.Random(seed).shuffle(ids)
    return ids


def nearly_sorted(n, seed=SEED, fraction=0.05):
    """Dataset 3: ascending IDs, then random pairs of positions are swapped
    until about `fraction` (5%) of all positions have been touched.
    Each swap touches 2 positions, so we do n*fraction/2 swaps."""
    ids = list(range(1, n + 1))
    rng = random.Random(seed)
    for _ in range(int(n * fraction / 2)):
        i, j = rng.randrange(n), rng.randrange(n)
        ids[i], ids[j] = ids[j], ids[i]
    return ids


GENERATORS = {
    "sequential": sequential,
    "random": random_permutation,
    "nearly_sorted": nearly_sorted,
}


def make_dataset(name, n, seed=SEED):
    return GENERATORS[name](n, seed)


def pick_search_keys(keys, count=1000, seed=SEED):
    """`count` randomly chosen EXISTING ids (all of them if n < count)."""
    return random.Random(seed + 1).sample(keys, min(count, len(keys)))


def pick_delete_keys(keys, fraction=0.20, seed=SEED):
    """A random 20% of the keys, to be deleted."""
    return random.Random(seed + 2).sample(keys, int(len(keys) * fraction))


def patient_name(pid):
    """Deterministic fake patient name for an ID."""
    return f"Patient_{pid}"
