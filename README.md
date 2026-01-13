# K=4 Resonance Singularity: Algebraic Invariance in Collatz Dynamics

**Current Version:** Golden Standard (V3.1)

## Abstract
This repository contains the rigorous verification of a singular arithmetic resonance in a fiber-coupled skew-product extension of the Collatz map ($3x+1$) with expansion factor $K=4$.

We demonstrate that the system admits a nontrivial invariant set supported on the primary $1 \to 4 \to 2$ cycle. This invariance is enforced by an algebraically invariant **Carry Gate**.

For $K \neq 4$, this gate is not invariant under the return map; survival requires repeated satisfaction of a **Sieve Constraint**. In our computations, no such trajectories are observed, resulting in extinction.

## Key Claims

### 1. Strict Invariance (Proven)
For $K=4$, the gate condition $n \le (p-1)/4$ is preserved at every return to the base state $w=1$. This guarantees the existence of a non-trivial invariant set (proved via the Identity Return Map theorem).

### 2. Sieve Mechanism (Observed)
For $K \neq 4$, the return map is a non-identity permutation. The "Safe Window" is not invariant in general. Long-term loop residence requires satisfying a probabilistic sieve constraint. Numerics confirm 0.00% survival for tested $K \in \{2, 3, 5, 6, 8, 16\}$.

## Repository Contents

* **`SUPPLEMENTARY_NOTE_K4_INVARIANCE.tex`**: The formal LaTeX manuscript defining the Lemma structure (Carry Gate & Conditional Return Map) and proving the K=4 Singularity.
* **`theorem_verifier.py`**: The V3.1 Python script that strictly tests the theorem. It proves 100% algebraic stability for K=4 and 0% empirical survival for K!=4.

## Reproduction Instructions

### Python Verification
To verify the algebraic proof and sieve extinction:
```bash
python theorem_verifier.py
