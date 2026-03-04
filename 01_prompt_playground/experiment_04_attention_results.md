# Experiment 04 — Mini Attention Simulator Results

> Built from scratch with NumPy only. No PyTorch, no TensorFlow.

---

## Input

```
X = 3 tokens, 4-dimensional embeddings
  token 1: [1.0, 0.0, 1.0, 0.0]
  token 2: [0.0, 2.0, 0.0, 1.0]
  token 3: [1.0, 1.0, 0.0, 1.0]
```

## Single-Head Scaled Attention

### Attention Weight Matrix `[3×3]`

| | token 1 | token 2 | token 3 |
|---|---------|---------|----------|
| **token 1** | 0.3178 | 0.3134 | 0.3689 |
| **token 2** | 0.2395 | 0.4042 | 0.3563 |
| **token 3** | 0.2420 | 0.3694 | 0.3886 |

*Each row sums to 1.0 (softmax output).*

### Output

```
token 1: [0.5633, 1.3581, 1.5679, 1.6371]
token 2: [0.6196, 1.3015, 1.6175, 1.6076]
token 3: [0.6101, 1.3305, 1.6249, 1.6203]
```

---

## Multi-Head Attention (2 heads)

### Head 1 Attention Weights

| | token 1 | token 2 | token 3 |
|---|---------|---------|----------|
| **token 1** | 0.4028 | 0.2630 | 0.3342 |
| **token 2** | 0.2440 | 0.3980 | 0.3580 |
| **token 3** | 0.3048 | 0.3367 | 0.3585 |

### Head 2 Attention Weights

| | token 1 | token 2 | token 3 |
|---|---------|---------|----------|
| **token 1** | 0.2506 | 0.3764 | 0.3730 |
| **token 2** | 0.2874 | 0.3692 | 0.3434 |
| **token 3** | 0.2321 | 0.3823 | 0.3856 |

---

## O(n²) Complexity Analysis

| n_tokens | Matrix | Cells | Memory | Time (ms) |
|----------|--------|-------|--------|----------|
| 8 | `8×8` | 64 | 0.2 KB | 1.44 |
| 64 | `64×64` | 4,096 | 16.0 KB | 0.28 |
| 256 | `256×256` | 65,536 | 256.0 KB | 1.75 |
| 512 | `512×512` | 262,144 | 1.0 MB | 3.97 |
| 1024 | `1024×1024` | 1,048,576 | 4.0 MB | 11.38 |
| 2048 | `2048×2048` | 4,194,304 | 16.0 MB | 59.36 |
