"""
fragmenter.py
Utilities for splitting and reassembling ciphertext fragments
for use in RL-based steganography.
"""

import math
import random
from typing import List


def split_ciphertext(ciphertext: bytes, num_fragments: int) -> List[bytes]:
    """
    Split ciphertext into N fragments of (almost) equal size.

    Args:
        ciphertext (bytes): The ciphertext to split.
        num_fragments (int): Number of fragments.

    Returns:
        List[bytes]: A list of ciphertext fragments.
    """
    if num_fragments <= 0:
        raise ValueError("num_fragments must be > 0")

    length = len(ciphertext)
    chunk_size = math.ceil(length / num_fragments)

    fragments = [
        ciphertext[i:i + chunk_size]
        for i in range(0, length, chunk_size)
    ]
    return fragments


def reassemble_fragments(fragments: List[bytes]) -> bytes:
    """
    Reassemble ciphertext from fragments.
    """
    return b"".join(fragments)


def random_fragmentation(ciphertext: bytes, min_size: int = 32, max_size: int = 128) -> List[bytes]:
    """
    Split ciphertext into random-sized fragments between [min_size, max_size].

    Args:
        ciphertext (bytes): Ciphertext to split.
        min_size (int): Minimum fragment size.
        max_size (int): Maximum fragment size.

    Returns:
        List[bytes]: A list of variable-sized ciphertext fragments.
    """
    fragments = []
    i = 0
    while i < len(ciphertext):
        frag_size = random.randint(min_size, max_size)
        fragments.append(ciphertext[i:i + frag_size])
        i += frag_size
    return fragments


# ============
# Simple Test
# ============
if __name__ == "__main__":
    # Fake ciphertext
    fake_ct = b"0123456789ABCDEF" * 10  # 160 bytes

    # Fixed split
    frags = split_ciphertext(fake_ct, 5)
    print(f"Fixed split: {[len(f) for f in frags]}")
    print("Reassembled OK:", reassemble_fragments(frags) == fake_ct)

    # Random split
    rand_frags = random_fragmentation(fake_ct, min_size=20, max_size=40)
    print(f"Random split: {[len(f) for f in rand_frags]}")
    print("Reassembled OK:", reassemble_fragments(rand_frags) == fake_ct)
