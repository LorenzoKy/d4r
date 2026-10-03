#!/usr/bin/env python3
"""Check the gfx12 K LDS row strides used by 16-byte WMMA loads.

For 16 lanes addressing consecutive rows, each 16-byte load touches four
consecutive 32-bit LDS banks. RDNA4 exposes 64 four-byte LDS banks. The
gfx1200 candidate uses 40/72 half-element strides so consecutive rows advance
20/36 banks; these phases produce no pairwise bank-set overlap across the 16
lanes in this access pattern, unlike the original 32/64 strides.
"""
from __future__ import annotations

from itertools import combinations


BANKS = 64
WORDS_PER_LOAD = 4
LANES = 16


def bank_set(stride_halves: int, lane: int) -> set[int]:
    words = (stride_halves * 2) // 4
    base = (lane * words) % BANKS
    return {(base + i) % BANKS for i in range(WORDS_PER_LOAD)}


def overlap_count(stride_halves: int) -> int:
    sets = [bank_set(stride_halves, lane) for lane in range(LANES)]
    return sum(len(a & b) for a, b in combinations(sets, 2))


def run() -> int:
    checks = {
        32: 96,  # Original K/V row stride: heavy aliasing.
        40: 0,   # gfx1200 KL candidate.
        64: 224, # Original VT row stride: extreme aliasing.
        72: 0,   # gfx1200 VT candidate.
    }
    for stride, expected in checks.items():
        actual = overlap_count(stride)
        if actual != expected:
            raise SystemExit(
                f"stride={stride}: expected overlap={expected}, got {actual}"
            )
    print("PASS gfx12 K LDS bank model: stride 40 and 72 have zero pairwise overlap.")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
