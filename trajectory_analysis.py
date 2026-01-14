"""
TRAJECTORY ANALYSIS & VISUALIZATION
Extended analysis of K=4 resonance singularity behavior
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from collections import defaultdict

PRIME_MOD = 1_000_000_007
MAX_STEPS = 100

def analyze_trajectory(k_val, n_init, max_steps=MAX_STEPS):
    """
    Track the full trajectory of a single (w, n) pair.
    Returns: trajectory history, survival status, exit point
    """
    limit = (PRIME_MOD - 1) // k_val
    inv2 = pow(2, PRIME_MOD - 2, PRIME_MOD)

    w = 1
    n = n_init

    trajectory = {
        'w': [w],
        'n': [n],
        'carry': [],
        'in_window': [n <= limit],
        'step_type': []
    }

    for step in range(max_steps):
        if w % 2 == 0:  # Even step
            trajectory['step_type'].append('even')
            trajectory['carry'].append(0)
            w = w // 2
            n = (n * inv2) % PRIME_MOD
        else:  # Odd step
            trajectory['step_type'].append('odd')
            carry = (k_val * n) // PRIME_MOD
            trajectory['carry'].append(carry)
            w = 3 * w + 1 + carry
            n = (k_val * n) % PRIME_MOD

        trajectory['w'].append(w)
        trajectory['n'].append(n)
        trajectory['in_window'].append(n <= limit)

        # Check if expelled from cycle
        if w not in [1, 2, 4]:
            return trajectory, False, step

    return trajectory, True, -1

def analyze_return_map_distribution(k_val, samples=10000):
    """
    Analyze how the return map R_K distributes points from the safe window.
    """
    limit = (PRIME_MOD - 1) // k_val
    inv4 = pow(4, PRIME_MOD - 2, PRIME_MOD)

    # Sample uniformly from the safe window
    n_values = np.random.randint(1, min(limit + 1, 1000000), samples).astype(np.int64)

    # Apply return map R_K(n) = (K/4) * n mod p
    n_returned = (n_values * k_val * inv4) % PRIME_MOD

    # Check what fraction remain in window
    still_in_window = np.sum(n_returned <= limit)

    return {
        'k': k_val,
        'limit': limit,
        'samples': samples,
        'returned_in_window': still_in_window,
        'retention_rate': 100 * still_in_window / samples,
        'n_values': n_values[:100],  # Store sample for visualization
        'n_returned': n_returned[:100]
    }

def generate_survival_curve(k_val, num_particles=1000, max_steps=100):
    """
    Track survival rate over time for ensemble of particles.
    """
    limit = (PRIME_MOD - 1) // k_val
    inv2 = pow(2, PRIME_MOD - 2, PRIME_MOD)

    # Initialize in safe window
    n = np.random.randint(1, min(limit + 1, 1000000), num_particles).astype(np.int64)
    w = np.ones(num_particles, dtype=np.int64)
    alive = np.ones(num_particles, dtype=bool)

    survival_history = [100.0]

    for step in range(max_steps):
        is_odd = (w % 2 != 0) & alive
        is_even = (w % 2 == 0) & alive

        # Even update
        w[is_even] //= 2
        n[is_even] = (n[is_even] * inv2) % PRIME_MOD

        # Odd update
        if np.any(is_odd):
            n_odd = n[is_odd]
            carry = (k_val * n_odd) // PRIME_MOD
            w_new = 3 * w[is_odd] + 1 + carry
            w[is_odd] = w_new
            n[is_odd] = (k_val * n_odd) % PRIME_MOD

        # Check survival
        alive &= np.isin(w, [1, 2, 4])
        survival_rate = 100 * np.sum(alive) / num_particles
        survival_history.append(survival_rate)

        if survival_rate == 0:
            break

    return survival_history

def main():
    print("=" * 70)
    print("K=4 RESONANCE SINGULARITY: TRAJECTORY ANALYSIS")
    print("=" * 70)

    # 1. Return Map Distribution Analysis
    print("\n[1] RETURN MAP DISTRIBUTION ANALYSIS")
    print("-" * 70)
    print(f"{'K':<5} {'Window Size':<15} {'Retention Rate':<20} {'Verdict'}")
    print("-" * 70)

    k_values = [2, 3, 4, 5, 6, 8]
    retention_data = {}

    for k in k_values:
        result = analyze_return_map_distribution(k, samples=10000)
        retention_data[k] = result

        verdict = "INVARIANT" if result['retention_rate'] > 99 else "SIEVE ACTIVE"
        print(f"{k:<5} {result['limit']:<15} {result['retention_rate']:>6.2f}% {verdict:>20}")

    # 2. Single Trajectory Deep Dive
    print("\n[2] SAMPLE TRAJECTORY ANALYSIS (First 30 steps)")
    print("-" * 70)

    for k in [4, 5]:
        limit = (PRIME_MOD - 1) // k
        n_init = limit // 2  # Middle of safe window

        traj, survived, exit_step = analyze_trajectory(k, n_init, max_steps=30)

        print(f"\nK={k}, n_init={n_init} (limit={limit})")
        print(f"Survival: {survived}, Exit at step: {exit_step if not survived else 'N/A'}")

        # Show first few returns to w=1
        returns = [i for i, w in enumerate(traj['w']) if w == 1][:5]
        print(f"Returns to w=1 at steps: {returns}")

        if len(returns) >= 2:
            for ret in returns[:3]:
                n_at_return = traj['n'][ret]
                in_window = n_at_return <= limit
                print(f"  Step {ret}: n={n_at_return}, in_window={in_window}")

    # 3. Survival Curves
    print("\n[3] ENSEMBLE SURVIVAL CURVES")
    print("-" * 70)

    survival_curves = {}
    for k in [2, 3, 4, 5]:
        curve = generate_survival_curve(k, num_particles=1000, max_steps=60)
        survival_curves[k] = curve

        final_survival = curve[-1]
        extinction_step = next((i for i, s in enumerate(curve) if s == 0), -1)

        print(f"K={k}: Final survival={final_survival:.2f}%, Extinct at step {extinction_step if extinction_step > 0 else 'Never'}")

    # 4. Generate Visualization
    print("\n[4] GENERATING VISUALIZATION")
    print("-" * 70)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('K=4 Resonance Singularity: Trajectory Analysis', fontsize=16, fontweight='bold')

    # Plot 1: Retention rates
    ax = axes[0, 0]
    k_list = sorted(retention_data.keys())
    rates = [retention_data[k]['retention_rate'] for k in k_list]
    colors = ['red' if k != 4 else 'green' for k in k_list]

    ax.bar(k_list, rates, color=colors, alpha=0.7, edgecolor='black')
    ax.axhline(100, color='blue', linestyle='--', linewidth=1, label='100% Invariance')
    ax.set_xlabel('K Factor', fontsize=12)
    ax.set_ylabel('Retention Rate (%)', fontsize=12)
    ax.set_title('Return Map Window Retention', fontweight='bold')
    ax.set_ylim([0, 105])
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    # Plot 2: Survival curves
    ax = axes[0, 1]
    for k, curve in survival_curves.items():
        linestyle = '-' if k == 4 else '--'
        linewidth = 2.5 if k == 4 else 1.5
        label = f'K={k}' + (' [INVARIANT]' if k == 4 else '')
        ax.plot(curve, label=label, linestyle=linestyle, linewidth=linewidth)

    ax.set_xlabel('Iteration Step', fontsize=12)
    ax.set_ylabel('Survival Rate (%)', fontsize=12)
    ax.set_title('Ensemble Survival Curves', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim([-5, 105])

    # Plot 3: Window size vs K
    ax = axes[1, 0]
    window_sizes = [(PRIME_MOD - 1) // k for k in k_list]
    ax.plot(k_list, window_sizes, 'o-', color='purple', linewidth=2, markersize=8)
    ax.set_xlabel('K Factor', fontsize=12)
    ax.set_ylabel('Safe Window Limit', fontsize=12)
    ax.set_title('Safe Window Size vs K', fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')

    # Plot 4: Return map illustration for K=4 vs K=5
    ax = axes[1, 1]

    for k in [4, 5]:
        data = retention_data[k]
        n_in = data['n_values'][:50]
        n_out = data['n_returned'][:50]
        limit = data['limit']

        # Normalize to [0, 1] for visualization
        n_in_norm = n_in / limit
        n_out_norm = n_out / limit

        label = f'K={k}'
        marker = 'o' if k == 4 else 'x'
        alpha = 0.6 if k == 4 else 0.4

        ax.scatter(n_in_norm, n_out_norm, label=label, alpha=alpha, s=30, marker=marker)

    ax.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Identity (K=4 behavior)')
    ax.axhline(1, color='red', linestyle=':', linewidth=1, alpha=0.5)
    ax.axvline(1, color='red', linestyle=':', linewidth=1, alpha=0.5)
    ax.fill_between([0, 1], 0, 1, alpha=0.1, color='green', label='Safe Window')

    ax.set_xlabel('n (normalized to window limit)', fontsize=11)
    ax.set_ylabel('R_K(n) (normalized)', fontsize=11)
    ax.set_title('Return Map: n → R_K(n)', fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 1.5])
    ax.set_ylim([0, 2.5])

    plt.tight_layout()
    plt.savefig('k4_resonance_analysis.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: k4_resonance_analysis.png")

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()
