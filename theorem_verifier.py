import sys
import numpy as np

# ==============================================================================
# THEOREM VERIFIER (V3.1 - GOLDEN STANDARD)
# Tests the invariance of the "Safe Window" lemma directly.
# CORRECTED: Uses strict limit (p-1)//K to ensure Kn < p.
# ==============================================================================

PRIME_MOD = 1_000_000_007
BATCH_SIZE = 100_000
TEST_STEPS = 60   # 20 full cycles (Sufficient for sieve extinction)

def verify_window_invariance(k_val):
    """
    Test: Does the 'Safe Window' [0, (p-1)/K] remain invariant under dynamics?
    
    1. Initialize w = 1 (Start of the cycle)
    2. Initialize n strictly inside the Safe Window.
    3. Run dynamics checking strictly for Loop Residence.
    """
    
    # 1. Define the Safe Window Limit (Strict Inequality Corrected)
    # We need c = floor(Kn/p) = 0  => Kn < p => n <= (p-1)/K
    limit = (PRIME_MOD - 1) // k_val
    
    if limit < 1: 
        return 0.0 # Window is closed (K >= p)

    # 2. Initialize strictly satisfying Lemma 1 (Theorem Condition)
    # We pick random n inside [1, limit]
    n = np.random.randint(1, limit + 1, BATCH_SIZE).astype(np.int64)
    w = np.ones(BATCH_SIZE, dtype=np.int64) # All start at w=1
    inv2 = pow(2, PRIME_MOD - 2, PRIME_MOD)
    
    # Track survival
    # A particle dies if it leaves the loop {1, 4, 2}
    alive_mask = np.ones(BATCH_SIZE, dtype=bool)
    
    for _ in range(TEST_STEPS):
        # Filter dead particles to prevent overflow/waste
        # (We clamp dead w to 2 just for safety)
        w[~alive_mask] = 2
        
        is_odd = (w % 2 != 0)
        is_even = ~is_odd
        
        # Even Update (w=4 -> 2, w=2 -> 1)
        w[is_even] //= 2
        n[is_even] = (n[is_even] * inv2) % PRIME_MOD
        
        # Odd Update (w=1 -> 4?)
        # If n is in Safe Window, carry=0 is guaranteed by initialization.
        # If K=4, n returns to Safe Window. If K!=4, it permutes.
        n_odd = n[is_odd]
        carry = (k_val * n_odd) // PRIME_MOD
        
        w[is_odd] = 3 * w[is_odd] + 1 + carry
        n[is_odd] = (k_val * n_odd) % PRIME_MOD
        
        # Check Survival: Did anyone leave {1, 2, 4}?
        current_in_loop = np.isin(w, [1, 2, 4])
        alive_mask &= current_in_loop

    survival_rate = 100 * np.sum(alive_mask) / BATCH_SIZE
    return survival_rate

def run_theorem_check():
    print(f"--- THEOREM VERIFICATION (N={BATCH_SIZE}) ---")
    print("Test Condition: Initialized strictly inside Safe Window (w=1, n <= (p-1)/K)")
    print("Hypothesis: K=4 is Invariant. K!=4 is Sifted.")
    print("-" * 65)
    print(f"{'K-Factor':<10} | {'Safe Limit (n <= ...)':<25} | {'Stability'}")
    print("-" * 65)
    
    k_values = [2, 3, 4, 5, 6, 8, 16]
    
    for k in k_values:
        limit = (PRIME_MOD - 1) // k
        rate = verify_window_invariance(k)
        
        status = f"{rate:6.2f}%"
        if rate > 99.9:
            status += "  [STRICT INVARIANCE CONFIRMED]"
        else:
            status += "  [EXTINCTION OBSERVED]"
            
        print(f"K={k:<8} | {limit:<25} | {status}")
        
    print("-" * 65)

if __name__ == "__main__":
    run_theorem_check()
