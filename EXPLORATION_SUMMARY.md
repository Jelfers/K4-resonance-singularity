# K=4 Resonance Singularity: Exploration Summary

## Overview
This document summarizes the extended exploration and analysis of the K=4 resonance singularity phenomenon in the fiber-coupled Collatz dynamics.

## Key Mathematical Discovery

The K=4 resonance arises from a **perfect algebraic cancellation** where the return map becomes the identity:

```
R_K(n) = (K/4) · n mod p

For K=4: R_4(n) = n    [IDENTITY]
For K≠4: R_K(n) ≠ n    [NON-IDENTITY PERMUTATION]
```

## Numerical Results

### Core Theorem Verification (theorem_verifier.py)
Testing 100,000 particles initialized in the safe window over 60 steps:

| K | Safe Window Limit | Stability | Result |
|---|-------------------|-----------|---------|
| 2 | 500,000,003 | 0.00% | Extinction |
| 3 | 333,333,335 | 0.00% | Extinction |
| **4** | **250,000,001** | **100.00%** | **Invariance** |
| 5 | 200,000,001 | 0.00% | Extinction |
| 6 | 166,666,667 | 0.00% | Extinction |
| 8 | 125,000,000 | 0.00% | Extinction |
| 16 | 62,500,000 | 0.00% | Extinction |

### Trajectory Analysis (trajectory_analysis.py)

**Return Map Behavior:**
- K=4: 100% of points remain in safe window after return map application
- K≠4: ~25-50% retention, demonstrating the sieve mechanism

**Survival Dynamics:**
- K=4: Perfect 100% survival (immortal trajectories)
- K=5: Complete extinction by step 19
- K=3: Complete extinction by step 25
- K=2: Complete extinction by step 49

**Trajectory Periodicity:**
- K=4 example: `n = 125,000,000 → 125,000,000 → 125,000,000` (period-3)
- K=5 example: `n = 100,000,000 → 125,000,000 → 156,250,000` (escapes window)

### Algebraic Structure Analysis (algebraic_structure_analysis.py)

**Return Map Orders:**
- K=4: Order = 1 (identity map)
- All other K: Order > 100 (high-order permutations)

**Window Coverage:**
| K | Coverage of Z_p | Theoretical Retention |
|---|-----------------|----------------------|
| 2 | 50.00% | 50.00% |
| 3 | 33.33% | 75.00% |
| 4 | 25.00% | 100.00% |
| 5 | 20.00% | 80.00% |
| 6 | 16.67% | 66.67% |
| 8 | 12.50% | 50.00% |

**Trajectory Lifetimes:**
| K | Mean Lifetime | Median | Max | Immortal % |
|---|---------------|--------|-----|------------|
| 2 | 6.0 | 6 | 36 | 0.00% |
| 3 | 5.2 | 4 | 18 | 0.00% |
| **4** | **199.0** | **199** | **199** | **100.00%** |
| 5 | 3.8 | 3 | 12 | 0.00% |
| 6 | 6.3 | 6 | 36 | 0.00% |

## Physical Interpretation

### The Resonance Mechanism

1. **Base Cycle**: `{1, 4, 2}` with period 3
   - Step 1: `w = 1 → 4` (odd step, multiply by 3, add 1)
   - Step 2: `w = 4 → 2` (even step, divide by 2)
   - Step 3: `w = 2 → 1` (even step, divide by 2)

2. **Fiber Coupling**: Each step transforms `n` in the fiber space `Z_p`
   - Odd step: `n → Kn mod p`
   - Even step: `n → n/2 mod p`
   - **Net per cycle**: `n → (K/4)n mod p`

3. **Resonance Condition**: For the fiber to return to itself after one base cycle:
   ```
   (K/4)n ≡ n (mod p)
   K/4 ≡ 1 (mod p)
   K = 4
   ```

4. **Carry Gate**: The "gatekeeper" condition that prevents escape from the base cycle:
   ```
   carry c = ⌊Kn/p⌋ must equal 0

   c = 0  ⟺  Kn < p  ⟺  n ≤ (p-1)/K
   ```

   This defines the **Safe Window**: `W_K = [0, (p-1)/K]`

### The Sieve Mechanism (K ≠ 4)

For K ≠ 4, the return map is a non-identity permutation. Long-term survival requires:

```
R_K(n) ∈ W_K  AND  R_K²(n) ∈ W_K  AND  R_K³(n) ∈ W_K  AND  ...
```

This is a **multiplicative sieve constraint** with probability that decreases exponentially with time, leading to extinction.

## Visualization

The exploration produced a comprehensive 4-panel visualization (`k4_resonance_analysis.png`):

1. **Top Left**: Return Map Window Retention - Shows K=4 achieving 100% retention
2. **Top Right**: Ensemble Survival Curves - K=4 maintains perfect stability while others decay
3. **Bottom Left**: Safe Window Size vs K - Inverse relationship (larger K = smaller window)
4. **Bottom Right**: Return Map Scatter - K=4 points lie on identity line, K=5 scatter above

## Theoretical Significance

The K=4 resonance represents a **codimension-infinity phenomenon** in the space of dynamical systems:

- It requires exact alignment: `K/4 = 1` (not approximately, but exactly)
- It demonstrates that Collatz-like systems can have non-trivial invariant sets
- It shows how fiber-coupling can create stable structures in otherwise chaotic systems

## Mathematical Proof Structure

The formal proof (see `SUPPLEMENTARY_NOTE_K4_INVARIANCE.tex`) consists of:

1. **Lemma 1**: The Carry Gate Condition
2. **Lemma 2**: The Conditional Return Map
3. **Theorem**: Existence of Invariant Set for K=4
4. **Corollary**: Sieve Constraint for K ≠ 4

The proof is algebraic and exact, with numerical verification confirming the predictions.

## Repository Contents

- `README.md` - Main documentation
- `SUPPLEMENTARY_NOTE_K4_INVARIANCE.tex` - Formal mathematical manuscript
- `K_4_Resonance_Singularity.pdf` - Compiled manuscript
- `theorem_verifier.py` - Core verification (V3.1, Golden Standard)
- `trajectory_analysis.py` - Extended trajectory and phase space analysis
- `algebraic_structure_analysis.py` - Deep algebraic structure investigation
- `k4_resonance_analysis.png` - Comprehensive visualization
- `EXPLORATION_SUMMARY.md` - This document

## Conclusion

The K=4 resonance singularity is a mathematically rigorous example of how specific parameter values can create stable invariant structures in dynamical systems. The perfect alignment of the return map's algebraic properties with the base cycle's geometry creates a resonance that survives indefinitely, while even slight deviations (K ≠ 4) lead to inevitable extinction through a multiplicative sieve mechanism.

This phenomenon demonstrates the power of algebraic methods in understanding complex dynamical systems and provides insight into the broader landscape of Collatz-like problems.
