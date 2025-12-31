import argparse
import time

import numpy as np

from gf2poly import rref_gf2_u64


def make_binary_matrix(rows: int, cols: int, density: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    if density >= 1.0:
        return rng.integers(0, 2, size=(rows, cols), dtype=np.uint8)
    mask = rng.random((rows, cols)) < density
    return mask.astype(np.uint8)


def pack_bits_to_uint64(mat: np.ndarray) -> np.ndarray:
    rows, cols = mat.shape
    nwords = (cols + 63) // 64
    padded_cols = nwords * 64
    if padded_cols != cols:
        pad = np.zeros((rows, padded_cols - cols), dtype=np.uint8)
        mat = np.concatenate([mat, pad], axis=1)

    packed = np.packbits(mat, axis=1, bitorder="little")
    # Ensure contiguous and word-aligned for view to uint64
    packed = np.ascontiguousarray(packed)
    return packed.view(np.uint64)


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark gf2poly bit-packed RREF")
    parser.add_argument("--rows", type=int, default=1024)
    parser.add_argument("--cols", type=int, default=1024)
    parser.add_argument("--density", type=float, default=0.1, help="Fraction of 1s in the matrix")
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    mat = make_binary_matrix(args.rows, args.cols, args.density, args.seed)
    packed = pack_bits_to_uint64(mat)

    start = time.perf_counter()
    rank = rref_gf2_u64(packed)
    elapsed = time.perf_counter() - start

    print(f"gf2poly rref_gf2_u64: {args.rows}x{args.cols}, density={args.density}")
    print(f"rank={rank}, elapsed_s={elapsed:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
