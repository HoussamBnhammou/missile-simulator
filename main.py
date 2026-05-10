"""
main.py
-------
Entry point. Run this file to start the simulation.

    python main.py

This file only does four things:
    1. Collect inputs from the user
    2. Run the simulation
    3. Print the results
    4. Show the plots (if requested)

All the real work happens in the other modules.
"""

import numpy as np
from inputs    import ask_position, ask_velocity, ask_thrust_direction, ask_mass, ask_engine
from guidance  import angles_to_unit_vector
from simulator import run
from plotting  import plot_all


def print_results(history, x0, y0, z0, elevation, azimuth, T_max, m_dry, thrust_vec):
    """Print a clean summary of the simulation results."""
    h     = history
    speed = np.sqrt(h['vx']**2 + h['vy']**2 + h['vz']**2)
    peak  = h['z'].argmax()
    rng   = np.sqrt((h['x'][-1]-x0)**2 + (h['y'][-1]-y0)**2)

    print("\n" + "="*52)
    print("  RESULTS")
    print("="*52)

    print(f"\n  Launch")
    print(f"    Position      : ({x0:.2f}, {y0:.2f}, {z0:.2f}) m")
    print(f"    Mass          : {h['mass'][0]:.1f} kg")
    print(f"    Thrust        : {T_max:.0f} N")
    print(f"    Thrust dir    : elev={elevation}°  az={azimuth}°")
    print(f"    Thrust vector : ({thrust_vec[0]:.4f}, {thrust_vec[1]:.4f}, {thrust_vec[2]:.4f})")

    print(f"\n  Peak")
    print(f"    Height        : {h['z'][peak]:.2f} m")
    print(f"    Position      : ({h['x'][peak]:.2f}, {h['y'][peak]:.2f}, {h['z'][peak]:.2f}) m")
    print(f"    At time       : {h['t'][peak]:.2f} s")
    print(f"    Speed         : {speed[peak]:.2f} m/s")

    print(f"\n  Impact")
    print(f"    Position      : ({h['x'][-1]:.2f}, {h['y'][-1]:.2f}, 0.00) m")
    print(f"    Time          : {h['t'][-1]:.2f} s")
    print(f"    Speed         : {speed[-1]:.2f} m/s")
    print(f"    Ground range  : {rng:.2f} m from launch")

    print(f"\n  Engine at end")
    print(f"    Thrust        : {h['thrust'][-1]:.2f} N  ({100*h['thrust'][-1]/T_max:.4f}% of max)")
    print(f"    Mass          : {h['mass'][-1]:.2f} kg  (fuel left: {h['mass'][-1]-m_dry:.2f} kg)")

    print("\n" + "="*52 + "\n")


def main():
    print("\n" + "="*52)
    print("   3D Missile Trajectory Simulator")
    print("   Thrust vector recomputed at every dt")
    print("="*52)

    # ── collect all inputs ─────────────────────────────────────────────────
    x0,  y0,  z0         = ask_position()
    vx0, vy0, vz0        = ask_velocity()
    elevation, azimuth   = ask_thrust_direction()
    m_dry, m_fuel        = ask_mass()
    T_max, k             = ask_engine()

    # show the computed thrust vector immediately so the user can verify it
    thrust_vec = angles_to_unit_vector(elevation, azimuth)
    print(f"\n  Thrust unit vector : ({thrust_vec[0]:.4f}, {thrust_vec[1]:.4f}, {thrust_vec[2]:.4f})")
    print(f"  Magnitude check    : {np.linalg.norm(thrust_vec):.6f}  (must be 1.0)")

    # ── run simulation ─────────────────────────────────────────────────────
    print("\nSimulating...")
    history = run(
        x0, y0, z0, vx0, vy0, vz0,
        elevation, azimuth,
        T_max, k, m_dry, m_fuel
    )

    # ── print results ──────────────────────────────────────────────────────
    print_results(history, x0, y0, z0, elevation, azimuth, T_max, m_dry, thrust_vec)

    # ── show plots ─────────────────────────────────────────────────────────
    show = input("Show plots? (y/n): ").strip().lower()
    if show == 'y':
        plot_all(history, x0, y0, z0, elevation, azimuth)


if __name__ == '__main__':
    main()
