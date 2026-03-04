"""
Experiment 04 — Mini Attention Simulator (No ML Libraries)
============================================================
Implements Scaled Dot-Product Attention and a 2-head Multi-Head
Attention from first principles using only NumPy.

Covers:
  - Single-head attention (raw and scaled)
  - Why the attention matrix is n×n
  - Memory and compute complexity: O(n²)
  - Multi-head attention with head splitting and projection
  - Practical scaling demo: tokens = 8, 64, 512, 2048

Usage:
    python 01_prompt_playground/experiment_04_attention_math.py

Outputs:
    - Formatted console walkthrough
    - experiment_04_attention_results.md (auto-generated)
"""

from __future__ import annotations

import time
from pathlib import Path

import numpy as np

np.random.seed(42)      # reproducible weight initialisation

# ── Helpers ────────────────────────────────────────────────────────────────────

def softmax(x: np.ndarray) -> np.ndarray:
    """Row-wise numerically stable softmax."""
    shifted = x - x.max(axis=-1, keepdims=True)   # subtract max for numerical stability
    exp_x   = np.exp(shifted)
    return exp_x / exp_x.sum(axis=-1, keepdims=True)


def scaled_dot_product_attention(
    Q: np.ndarray,
    K: np.ndarray,
    V: np.ndarray,
    mask: np.ndarray | None = None,
    verbose: bool = False,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Scaled Dot-Product Attention — the core of every Transformer.

    Formula: Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) · V

    Args:
        Q: Query matrix  [n_tokens, d_k]
        K: Key matrix    [n_tokens, d_k]
        V: Value matrix  [n_tokens, d_v]
        mask: Optional boolean mask [n_tokens, n_tokens] — True = ignore
        verbose: Print intermediate matrices

    Returns:
        output:           [n_tokens, d_v]
        attention_weights:[n_tokens, n_tokens]  ← the n×n matrix
    """
    d_k = Q.shape[-1]
    scale = np.sqrt(d_k)

    # Step 1 — raw scores: shape [n, n]
    scores = Q @ K.T                     # each token attends to every other token
    scaled_scores = scores / scale       # prevent softmax saturation in high dimensions

    if mask is not None:
        scaled_scores = np.where(mask, -1e9, scaled_scores)

    # Step 2 — softmax over last axis: still [n, n]
    attention_weights = softmax(scaled_scores)

    # Step 3 — weighted sum of values: [n, n] × [n, d_v] → [n, d_v]
    output = attention_weights @ V

    if verbose:
        print(f"\n    d_k          = {d_k}  →  scale = √{d_k} = {scale:.4f}")
        print(f"    Raw scores   shape: {scores.shape}")
        print(f"    Attn weights shape: {attention_weights.shape}  (the n×n matrix)")
        print(f"    Output       shape: {output.shape}")

    return output, attention_weights


# ── Multi-Head Attention ────────────────────────────────────────────────────────

def multi_head_attention(
    X: np.ndarray,
    Wq: np.ndarray,
    Wk: np.ndarray,
    Wv: np.ndarray,
    Wo: np.ndarray,
    num_heads: int,
) -> tuple[np.ndarray, list[np.ndarray]]:
    """
    Multi-Head Attention from scratch.

    Splits d_model into num_heads sub-spaces, runs independent attention
    in each, concatenates, and projects back.

    Args:
        X:         Input token embeddings [n_tokens, d_model]
        Wq/Wk/Wv: Projection matrices    [d_model, d_model]
        Wo:        Output projection      [d_model, d_model]
        num_heads: Number of attention heads

    Returns:
        output:      [n_tokens, d_model]
        head_weights: list of [n_tokens, n_tokens] per head
    """
    n_tokens, d_model = X.shape
    assert d_model % num_heads == 0, "d_model must be divisible by num_heads"
    d_head = d_model // num_heads

    # Project once into full space
    Q_full = X @ Wq     # [n, d_model]
    K_full = X @ Wk
    V_full = X @ Wv

    head_outputs: list[np.ndarray]    = []
    head_weights: list[np.ndarray]    = []

    for h in range(num_heads):
        start = h * d_head
        end   = start + d_head
        # Each head sees a different slice of the projected space
        Q_h = Q_full[:, start:end]   # [n, d_head]
        K_h = K_full[:, start:end]
        V_h = V_full[:, start:end]

        out_h, w_h = scaled_dot_product_attention(Q_h, K_h, V_h)
        head_outputs.append(out_h)
        head_weights.append(w_h)

    # Concatenate all heads → [n, d_model], then project
    concat = np.concatenate(head_outputs, axis=-1)   # [n, d_model]
    output = concat @ Wo                              # [n, d_model]

    return output, head_weights


# ── Complexity Analyser ────────────────────────────────────────────────────────

def measure_attention_complexity(token_counts: list[int], d_model: int = 64) -> list[dict]:
    """
    Measures actual wall-clock time and memory footprint of the n×n
    attention matrix across token sequence lengths.
    """
    results = []
    for n in token_counts:
        X  = np.random.randn(n, d_model).astype(np.float32)
        Wq = np.random.randn(d_model, d_model).astype(np.float32)
        Wk = np.random.randn(d_model, d_model).astype(np.float32)
        Wv = np.random.randn(d_model, d_model).astype(np.float32)

        Q = X @ Wq
        K = X @ Wk
        V = X @ Wv

        t0 = time.perf_counter()
        _, attn = scaled_dot_product_attention(Q, K, V)
        elapsed_ms = (time.perf_counter() - t0) * 1000

        # Memory: the attention matrix itself is n×n float32 (4 bytes each)
        attn_matrix_bytes = n * n * 4
        results.append({
            "n_tokens": n,
            "attn_shape": f"{n}×{n}",
            "attn_cells": n * n,
            "mem_bytes": attn_matrix_bytes,
            "mem_mb": attn_matrix_bytes / (1024 ** 2),
            "elapsed_ms": elapsed_ms,
        })
    return results


# ── Console Report ─────────────────────────────────────────────────────────────

def print_report(
    X: np.ndarray,
    weights_single: np.ndarray,
    output_single: np.ndarray,
    weights_heads: list[np.ndarray],
    output_mha: np.ndarray,
    complexity: list[dict],
) -> None:
    sep  = "=" * 72
    dash = "─" * 72

    # ── Section 1: single-head
    print(f"\n{sep}")
    print("  SECTION 1 — Scaled Single-Head Attention")
    print(sep)
    print(f"\n  Input X (3 tokens, 4-dim):\n{X}")
    print(f"\n  Attention Weight Matrix  [{weights_single.shape[0]}×{weights_single.shape[1]}]:")
    print(f"  (row i = how much token i attends to each other token)")
    print(np.array2string(weights_single, precision=4, suppress_small=True, prefix="  "))
    print(f"\n  Row sums (must all be 1.0): {weights_single.sum(axis=1).round(6)}")
    print(f"\n  Output (weighted context per token):\n"
          f"{np.array2string(output_single, precision=4, suppress_small=True)}")

    # ── Section 2: Why n×n?
    print(f"\n{sep}")
    print("  SECTION 2 — Why Is the Attention Matrix n×n?")
    print(sep)
    n = X.shape[0]
    print(f"""
  With {n} input tokens:
    Q shape : [{n}, d_k]
    K shape : [{n}, d_k]
    Q @ K^T : [{n}, d_k] × [d_k, {n}] → [{n}, {n}]  ← every token × every token

  The matrix entry [i, j] answers:
    "How much should token {'{i}'} attend to token {'{j}'}?"

  Every token must score against every other token simultaneously.
  That's n tokens × n tokens = n² values — unavoidable with full attention.
    """)

    # ── Section 3: Multi-Head
    print(f"\n{sep}")
    print("  SECTION 3 — Multi-Head Attention (2 heads)")
    print(sep)
    for i, w in enumerate(weights_heads):
        print(f"\n  Head {i + 1} attention weights [{w.shape[0]}×{w.shape[1]}]:")
        print(np.array2string(w, precision=4, suppress_small=True, prefix="  "))
    print(f"\n  MHA output shape: {output_mha.shape}")
    print("  (heads capture different relationship patterns in parallel)")

    # ── Section 4: O(n²) complexity
    print(f"\n{sep}")
    print("  SECTION 4 — Memory & Compute: O(n²) Complexity")
    print(sep)
    print(f"\n  {'n_tokens':<12} {'Matrix':<10} {'Cells':>12} {'Memory':>12} {'Time (ms)':>12}")
    print(f"  {dash[:65]}")
    for r in complexity:
        mem_str = (f"{r['mem_mb']:.1f} MB" if r['mem_mb'] >= 1
                   else f"{r['mem_bytes'] / 1024:.1f} KB")
        print(f"  {r['n_tokens']:<12} {r['attn_shape']:<10} "
              f"{r['attn_cells']:>12,} {mem_str:>12} {r['elapsed_ms']:>11.2f}")

    print(f"""
  Observation:
    n=8    →  64 cells      →  negligible
    n=512  →  262,144 cells →  ~1 MB
    n=2048 →  4,194,304 cells → ~16 MB  (just the attention matrix)

  For n=10,000 (hypothetical):
    Attention matrix = 10,000 × 10,000 = 100,000,000 cells
    Memory at float32 = 100M × 4 bytes = ~381 MB  (per layer, per head)
    A 32-layer model would need ~12 GB just for attention matrices.

  This is WHY transformers have context window limits — not model quality,
  but quadratic memory growth in n (sequence length).
    """)

    print(sep)
    print("  KEY INSIGHT: Attention is O(n²) in memory and O(n²·d) in compute.")
    print("  This drove the research behind FlashAttention, Longformer,")
    print("  Mamba (SSM), and other sub-quadratic architectures.")
    print(sep)


# ── Markdown Writer ────────────────────────────────────────────────────────────

def write_markdown(
    X: np.ndarray,
    weights_single: np.ndarray,
    output_single: np.ndarray,
    weights_heads: list[np.ndarray],
    complexity: list[dict],
    out_path: Path,
) -> None:
    lines: list[str] = []
    a = lines.append

    a("# Experiment 04 — Mini Attention Simulator Results\n\n")
    a("> Built from scratch with NumPy only. No PyTorch, no TensorFlow.\n\n")
    a("---\n\n")

    a("## Input\n\n")
    a("```\n")
    a("X = 3 tokens, 4-dimensional embeddings\n")
    for i, row in enumerate(X):
        a(f"  token {i + 1}: {row.tolist()}\n")
    a("```\n\n")

    a("## Single-Head Scaled Attention\n\n")
    a(f"### Attention Weight Matrix `[{weights_single.shape[0]}×{weights_single.shape[1]}]`\n\n")
    a("| | token 1 | token 2 | token 3 |\n")
    a("|---|---------|---------|----------|\n")
    for i, row in enumerate(weights_single):
        a(f"| **token {i + 1}** | {row[0]:.4f} | {row[1]:.4f} | {row[2]:.4f} |\n")
    a("\n*Each row sums to 1.0 (softmax output).*\n\n")

    a("### Output\n\n")
    a("```\n")
    for i, row in enumerate(output_single):
        a(f"token {i + 1}: [{', '.join(f'{v:.4f}' for v in row)}]\n")
    a("```\n\n---\n\n")

    a("## Multi-Head Attention (2 heads)\n\n")
    for i, w in enumerate(weights_heads):
        a(f"### Head {i + 1} Attention Weights\n\n")
        a("| | token 1 | token 2 | token 3 |\n")
        a("|---|---------|---------|----------|\n")
        for j, row in enumerate(w):
            a(f"| **token {j + 1}** | {row[0]:.4f} | {row[1]:.4f} | {row[2]:.4f} |\n")
        a("\n")
    a("---\n\n")

    a("## O(n²) Complexity Analysis\n\n")
    a("| n_tokens | Matrix | Cells | Memory | Time (ms) |\n")
    a("|----------|--------|-------|--------|----------|\n")
    for r in complexity:
        mem_str = (f"{r['mem_mb']:.1f} MB" if r['mem_mb'] >= 1
                   else f"{r['mem_bytes'] / 1024:.1f} KB")
        a(f"| {r['n_tokens']} | `{r['attn_shape']}` | {r['attn_cells']:,} | {mem_str} | {r['elapsed_ms']:.2f} |\n")

    out_path.write_text("".join(lines), encoding="utf-8")
    print(f"\n  Results written → {out_path}")


# ── Entry Point ────────────────────────────────────────────────────────────────

def main() -> None:
    print(f"\n{'=' * 72}")
    print("  Experiment 04 — Mini Attention Simulator (NumPy only)")
    print(f"{'=' * 72}")

    # ── Inputs
    X = np.array([
        [1, 0, 1, 0],
        [0, 2, 0, 1],
        [1, 1, 0, 1],
    ], dtype=float)

    d_model = X.shape[1]   # 4
    num_heads = 2

    Wq = np.random.rand(d_model, d_model)
    Wk = np.random.rand(d_model, d_model)
    Wv = np.random.rand(d_model, d_model)
    Wo = np.random.rand(d_model, d_model)

    # ── Single-head
    print("\n  [1/3] Running scaled single-head attention ...", end=" ", flush=True)
    Q, K, V = X @ Wq, X @ Wk, X @ Wv
    output_single, weights_single = scaled_dot_product_attention(Q, K, V, verbose=True)
    print("done")

    # ── Multi-head
    print("  [2/3] Running 2-head multi-head attention  ...", end=" ", flush=True)
    output_mha, weights_heads = multi_head_attention(X, Wq, Wk, Wv, Wo, num_heads)
    print("done")

    # ── Complexity sweep
    print("  [3/3] Measuring O(n²) complexity sweep     ...", end=" ", flush=True)
    complexity = measure_attention_complexity([8, 64, 256, 512, 1024, 2048])
    print("done")

    # ── Report
    print_report(X, weights_single, output_single, weights_heads, output_mha, complexity)

    out = Path(__file__).parent / "experiment_04_attention_results.md"
    write_markdown(X, weights_single, output_single, weights_heads, complexity, out)


if __name__ == "__main__":
    main()
