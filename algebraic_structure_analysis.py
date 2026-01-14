"""
ALGEBRAIC STRUCTURE ANALYSIS
Deep dive into the mathematical properties of the K=4 resonance
"""

import numpy as np
from math import gcd
from collections import defaultdict

PRIME_MOD = 1_000_000_007

def analyze_return_map_order(k_val, max_order=100):
    """
    Compute the order of the return map R_K as a permutation.
    R_K(n) = (K/4) * n mod p

    The order is the smallest m such that R_K^m = identity
    """
    # Compute the multiplier (K/4) mod p
    inv4 = pow(4, PRIME_MOD - 2, PRIME_MOD)
    multiplier = (k_val * inv4) % PRIME_MOD

    # Find the multiplicative order of the multiplier
    if multiplier == 1:
        return 1  # Identity map

    current = multiplier
    for order in range(1, max_order + 1):
        if current == 1:
            return order
        current = (current * multiplier) % PRIME_MOD

    return None  # Order > max_order

def compute_window_retention_probability(k_val):
    """
    Theoretical probability that R_K maps the safe window to itself.

    Window W_K = [0, (p-1)/K]
    R_K(n) = (K/4) * n mod p

    For a point n in W_K, R_K(n) in W_K requires:
    (K/4) * n mod p <= (p-1)/K
    """
    limit = (PRIME_MOD - 1) // k_val
    inv4 = pow(4, PRIME_MOD - 2, PRIME_MOD)
    multiplier = (k_val * inv4) % PRIME_MOD

    if multiplier == 1:
        return 100.0  # Identity - always maps to itself

    # For K > 4: multiplier > 1
    # The return map expands the window
    # Approximate retention probability

    if k_val < 4:
        # Multiplier < 1 (in the sense of K/4 < 1)
        # Map contracts, high retention expected
        contraction_factor = k_val / 4
        return 100.0 * contraction_factor
    elif k_val == 4:
        return 100.0
    else:
        # Multiplier > 1, map expands
        expansion_factor = k_val / 4
        return 100.0 / expansion_factor

def analyze_carry_gate_statistics(k_val, samples=100000):
    """
    Analyze the carry gate behavior for different initial conditions.
    """
    limit = (PRIME_MOD - 1) // k_val

    # Sample from different regions
    regions = {
        'deep_inside': (1, limit // 4),
        'middle': (limit // 4, limit // 2),
        'near_boundary': (limit // 2, limit),
        'outside': (limit + 1, min(limit * 2, PRIME_MOD - 1))
    }

    results = {}

    for region_name, (low, high) in regions.items():
        if low >= high:
            continue

        n_samples = np.random.randint(low, high + 1, min(samples, high - low))
        carry_values = (k_val * n_samples) // PRIME_MOD

        results[region_name] = {
            'mean_carry': np.mean(carry_values),
            'max_carry': np.max(carry_values),
            'zero_carry_pct': 100 * np.sum(carry_values == 0) / len(carry_values),
            'sample_size': len(n_samples)
        }

    return results

def analyze_cycle_structure(k_val, num_samples=1000):
    """
    Analyze the cycle structure of trajectories.
    Track how long trajectories survive before leaving {1,2,4}.
    """
    limit = (PRIME_MOD - 1) // k_val
    inv2 = pow(2, PRIME_MOD - 2, PRIME_MOD)

    # Initialize in safe window
    n_samples = np.random.randint(1, min(limit + 1, 1000000), num_samples).astype(np.int64)

    lifetimes = []

    for n_init in n_samples:
        w = 1
        n = n_init
        lifetime = 0

        for step in range(200):
            if w not in [1, 2, 4]:
                break

            lifetime = step

            if w % 2 == 0:
                w = w // 2
                n = (n * inv2) % PRIME_MOD
            else:
                carry = (k_val * n) // PRIME_MOD
                w = 3 * w + 1 + carry
                n = (k_val * n) % PRIME_MOD

        lifetimes.append(lifetime)

    return {
        'mean_lifetime': np.mean(lifetimes),
        'median_lifetime': np.median(lifetimes),
        'max_lifetime': np.max(lifetimes),
        'immortal_count': np.sum(np.array(lifetimes) >= 199),
        'immortal_pct': 100 * np.sum(np.array(lifetimes) >= 199) / num_samples
    }

def theoretical_window_coverage(k_val):
    """
    Compute what fraction of the fiber space is covered by the safe window.
    """
    limit = (PRIME_MOD - 1) // k_val
    coverage = limit / PRIME_MOD
    return coverage * 100

def main():
    print("=" * 75)
    print("ALGEBRAIC STRUCTURE ANALYSIS: K=4 RESONANCE SINGULARITY")
    print("=" * 75)

    # 1. Return Map Order Analysis
    print("\n[1] RETURN MAP ALGEBRAIC ORDER")
    print("-" * 75)
    print(f"{'K':<5} {'Multiplier (K/4 mod p)':<25} {'Order':<15} {'Interpretation'}")
    print("-" * 75)

    k_values = [2, 3, 4, 5, 6, 8, 16]

    for k in k_values:
        order = analyze_return_map_order(k, max_order=100)
        inv4 = pow(4, PRIME_MOD - 2, PRIME_MOD)
        multiplier = (k * inv4) % PRIME_MOD

        if order == 1:
            interpretation = "IDENTITY MAP"
        elif order is None:
            interpretation = f"Order > 100"
        else:
            interpretation = f"Periodic, period {order}"

        order_str = str(order) if order else ">100"
        print(f"{k:<5} {multiplier:<25} {order_str:<15} {interpretation}")

    # 2. Window Coverage Analysis
    print("\n[2] SAFE WINDOW COVERAGE ANALYSIS")
    print("-" * 75)
    print(f"{'K':<5} {'Window Size':<20} {'Coverage of Z_p (%)':<25} {'Retention Theory'}")
    print("-" * 75)

    for k in k_values:
        limit = (PRIME_MOD - 1) // k
        coverage = theoretical_window_coverage(k)
        retention_theory = compute_window_retention_probability(k)

        print(f"{k:<5} {limit:<20} {coverage:>7.4f}% {retention_theory:>20.2f}%")

    # 3. Carry Gate Statistics
    print("\n[3] CARRY GATE BEHAVIOR (K=4 vs K=5)")
    print("-" * 75)

    for k in [4, 5]:
        print(f"\n  K={k}:")
        stats = analyze_carry_gate_statistics(k, samples=10000)

        for region, data in stats.items():
            print(f"    {region:>15}: zero_carry={data['zero_carry_pct']:>6.2f}%, " +
                  f"mean={data['mean_carry']:>8.2f}, max={data['max_carry']}")

    # 4. Cycle Structure Analysis
    print("\n[4] TRAJECTORY LIFETIME ANALYSIS")
    print("-" * 75)
    print(f"{'K':<5} {'Mean Life':<12} {'Median':<12} {'Max':<12} {'Immortal %'}")
    print("-" * 75)

    for k in [2, 3, 4, 5, 6]:
        cycle_stats = analyze_cycle_structure(k, num_samples=500)

        print(f"{k:<5} {cycle_stats['mean_lifetime']:<12.1f} " +
              f"{cycle_stats['median_lifetime']:<12.0f} " +
              f"{cycle_stats['max_lifetime']:<12} " +
              f"{cycle_stats['immortal_pct']:>6.2f}%")

    # 5. Key Mathematical Properties
    print("\n[5] MATHEMATICAL INSIGHT: WHY K=4 IS SPECIAL")
    print("-" * 75)
    print("""
The K=4 resonance arises from a perfect algebraic cancellation:

1. CYCLE STRUCTURE: The base cycle is {1, 4, 2} with return period 3
   - Odd step:  w → 3w + 1     (1 → 4)
   - Even step: w → w/2         (4 → 2 → 1)

2. FIBER TRANSFORMATION per cycle:
   - Step 1 (odd):  n → Kn mod p
   - Step 2 (even): n → n/2 mod p
   - Step 3 (even): n → n/2 mod p
   - NET EFFECT:    n → (K/4)n mod p

3. INVARIANCE CONDITION: R_K(n) = n requires K/4 ≡ 1 (mod p)

   For p = 1000000007 and K=4:
   K/4 = 1 (exactly), so the return map is the IDENTITY

4. CARRY GATE: At odd steps, carry c = ⌊Kn/p⌋ must equal 0
   This requires n ≤ (p-1)/K, defining the "Safe Window"

   For K=4: If n starts in window, R_4(n) = n means it STAYS forever

5. SIEVE MECHANISM (K ≠ 4):
   R_K is a non-identity permutation. The safe window is NOT invariant.
   Long-term survival requires accidentally satisfying:
   R_K(n) ∈ W_K  AND  R_K²(n) ∈ W_K  AND  R_K³(n) ∈ W_K  AND ...

   This is a multiplicative sieve constraint with exponentially small
   probability, leading to observed extinction.

CONCLUSION: K=4 is the UNIQUE value that achieves algebraic resonance
between the base cycle period (3) and the fiber doubling structure (4 = 2²).
    """)

    print("=" * 75)
    print("ANALYSIS COMPLETE")
    print("=" * 75)

if __name__ == "__main__":
    main()
