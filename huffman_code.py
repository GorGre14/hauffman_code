#!/usr/bin/env python3
# huffman_project.py
# Author: <your-name-here>
# Created: May 2025
"""
Re-implementation of the TOR III Huffman-coding mini-project.

• Alphabet: {a,b,c,d,e,f}
• Tests block lengths k = 1 and 2 (pairs are non-overlapping)
• Prints entropy H, expected code-word length E[L], realised
  average length L̄ on the generated sequence, and the compression
  ratio  log₂|Σᵏ| / L̄
• Repeats the analysis when the source probabilities suddenly change
  to P(a)=0.30, P(f)=0.05 but the *same* codebook is kept.
"""

from __future__ import annotations
import heapq
import itertools
import math
import random
from collections import Counter
from typing import Dict, Iterable, List, Tuple

Symbol = str


# ----------------------------------------------------------------------
# 1. Huffman coding utilities
# ----------------------------------------------------------------------
class _Node:
    """Internal node for the priority queue."""
    def __init__(self, prob: float, sym: Symbol | None, left: "_Node" | None = None,
                 right: "_Node" | None = None):
        self.prob, self.sym, self.left, self.right = prob, sym, left, right

    # heapq uses <  – we reverse to ensure stable ordering on equal prob
    def __lt__(self, other: "_Node"):
        return self.prob < other.prob


def huffman_code(probabilities: Dict[Symbol, float]) -> Dict[Symbol, str]:
    """
    Build a *canonical* Huffman code in O(n log n).
    Returns a dict {symbol: bitstring}.
    """
    pq: List[_Node] = [_Node(p, s) for s, p in probabilities.items() if p > 0.0]
    if len(pq) == 1:                      # trivial one-symbol case
        return {pq[0].sym: "0"}

    heapq.heapify(pq)
    while len(pq) > 1:
        lo, hi = heapq.heappop(pq), heapq.heappop(pq)
        heapq.heappush(pq, _Node(lo.prob + hi.prob, None, lo, hi))

    # traverse tree to assign preliminary codes
    codes: Dict[Symbol, str] = {}

    def _traverse(node: _Node, prefix: str):
        if node.sym is not None:          # leaf
            codes[node.sym] = prefix
            return
        _traverse(node.left,  prefix + "0")
        _traverse(node.right, prefix + "1")

    _traverse(pq[0], "")

    # canonicalise: sort by (length, lexicographic symbol) then re-assign
    lengths = sorted(((len(code), sym) for sym, code in codes.items()))
    code_val = 0
    prev_len = lengths[0][0]
    for length, sym in lengths:
        code_val <<= (length - prev_len)     # shift when length grows
        codes[sym] = f"{code_val:0{length}b}"
        code_val += 1
        prev_len = length
    return codes


# ----------------------------------------------------------------------
# 2. Metrics
# ----------------------------------------------------------------------
def entropy(probabilities: Dict[Symbol, float]) -> float:
    return -sum(p * math.log2(p) for p in probabilities.values() if p > 0.0)


def expected_length(codebook: Dict[Symbol, str],
                    probabilities: Dict[Symbol, float]) -> float:
    return sum(probabilities[s] * len(codebook[s]) for s in probabilities)


def average_realised_length(codebook: Dict[Symbol, str],
                            sequence: Iterable[Symbol]) -> float:
    counts = Counter(sequence)
    total = sum(counts.values())
    return sum(count * len(codebook[s]) for s, count in counts.items()) / total


def compression_ratio(codebook: Dict[Symbol, str],
                      sequence: Iterable[Symbol],
                      k: int) -> float:
    L_bar = average_realised_length(codebook, sequence)
    return math.log2(len(ALPHABET) ** k) / L_bar


# ----------------------------------------------------------------------
# 3. Encoding / decoding helpers
# ----------------------------------------------------------------------
def encode(sequence: Iterable[Symbol], codebook: Dict[Symbol, str]) -> str:
    return "".join(codebook[s] for s in sequence)


def decode(bitstring: str, codebook: Dict[Symbol, str]) -> List[Symbol]:
    # Reverse map for speed
    rev = {v: k for k, v in codebook.items()}
    decoded: List[Symbol] = []
    w = ""
    for bit in bitstring:
        w += bit
        if w in rev:
            decoded.append(rev[w])
            w = ""
    if w:
        raise ValueError("dangling bits – codebook not prefix-free?")
    return decoded


# ----------------------------------------------------------------------
# 4. Experiment runner
# ----------------------------------------------------------------------
def run_experiment(k: int,
                   probs: Dict[Symbol, float],
                   seq: List[Symbol],
                   header: str):
    # Build probability model for blocks of length k
    if k == 1:
        prob_k = probs
        blocks = seq
    else:
        # theoretical i.i.d. product distribution for ALL pairs
        prob_k = {x + y: probs[x] * probs[y]
                  for x, y in itertools.product(ALPHABET, repeat=k)}
        # form non-overlapping blocks for the realised sequence
        blocks = ["".join(seq[i:i + k]) for i in range(0, len(seq), k)]

    code_k = huffman_code(prob_k)

    print(f"\n{header}")
    print("–" * len(header))
    print(f"Alphabet size |Σᵏ|      : {len(prob_k):>3}")
    H = entropy(prob_k)
    E_L = expected_length(code_k, prob_k)
    L_bar = average_realised_length(code_k, blocks)
    ratio = compression_ratio(code_k, blocks, k)
    print(f"Entropy H(Sᵏ)          : {H:.4f} bits")
    print(f"Expected length E[L]   : {E_L:.4f} bits")
    print(f"Average length  L̄     : {L_bar:.4f} bits")
    print(f"Compression ratio log₂|Σᵏ| / L̄ : {ratio:.4f}")
    return code_k, blocks


# ----------------------------------------------------------------------
# 5. Main script
# ----------------------------------------------------------------------
ALPHABET = ["a", "b", "c", "d", "e", "f"]

def main():
    random.seed(0xC0FFEE)                       # deterministic demo
    p_original = dict(zip(ALPHABET,
                          [0.05, 0.10, 0.15, 0.18, 0.22, 0.30]))
    p_shifted  = dict(zip(ALPHABET,
                          [0.30, 0.10, 0.15, 0.18, 0.22, 0.05]))

    # 1 000-symbol test sequence from the *original* distribution
    sequence = random.choices(ALPHABET,
                              weights=[p_original[s] for s in ALPHABET],
                              k=1_000)

    # ---------- block length k = 1 ----------
    code1, _ = run_experiment(1, p_original, sequence,
                              "Block length k = 1 (optimal code)")

    # ---------- block length k = 2 ----------
    code2, blocks2 = run_experiment(2, p_original, sequence,
                                    "Block length k = 2 (optimal code)")

    # ---------- probability shift (still using the old code) ----------
    print("\nProbability shift:  P(a)=0.30, P(f)=0.05  **no re-coding**")
    # single symbols
    E_L1_shift = expected_length(code1, p_shifted)
    ratio1_shift = math.log2(len(ALPHABET)) / E_L1_shift
    print(f"k=1  –  E[L] = {E_L1_shift:.4f} bits   ratio = {ratio1_shift:.4f}")
    # pairs – assume independence for theoretical expectation
    prob2_shift = {x + y: p_shifted[x] * p_shifted[y]
                   for x, y in itertools.product(ALPHABET, repeat=2)}
    E_L2_shift = expected_length(code2, prob2_shift)
    ratio2_shift = math.log2(len(ALPHABET) ** 2) / E_L2_shift
    print(f"k=2  –  E[L] = {E_L2_shift:.4f} bits   ratio = {ratio2_shift:.4f}")


if __name__ == "__main__":
    main()