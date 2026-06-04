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
from inputs    import (
    ask_angular_velocity,
    ask_body_orientation,
    ask_body_shape,
    ask_engine,
    ask_mass,
    ask_position,
    ask_velocity,
)
from guidance  import angles_to_unit_vector
from rocket_body import RocketBody, inertia_tensor_body
from simulator import run
from vectors   import velocity_direction


def print_results(history, x0, y0, z0, elevation, azimuth, T_max, m_dry, orientation_vec):
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
    print(f"    Body shape    : length={h['length'][0]:.2f} m  radius={h['radius'][0]:.2f} m")
    print(f"    Thrust        : {T_max:.0f} N")
    print(f"    Body dir      : elev={elevation}°  az={azimuth}°")
    print(f"    Body vector   : ({orientation_vec[0]:.4f}, {orientation_vec[1]:.4f}, {orientation_vec[2]:.4f})")
    print(f"    Path vector   : ({h['vdx'][0]:.4f}, {h['vdy'][0]:.4f}, {h['vdz'][0]:.4f})")
    print(f"    Initial AoA   : {np.degrees(h['aoa'][0]):.2f}°")

    print(f"\n  Peak")
    print(f"    Height        : {h['z'][peak]:.2f} m")
    print(f"    Position      : ({h['x'][peak]:.2f}, {h['y'][peak]:.2f}, {h['z'][peak]:.2f}) m")
    print(f"    At time       : {h['t'][peak]:.2f} s")
    print(f"    Speed         : {speed[peak]:.2f} m/s")
    print(f"    AoA           : {np.degrees(h['aoa'][peak]):.2f}°")
    print(f"    Angular speed : {np.linalg.norm([h['wx'][peak], h['wy'][peak], h['wz'][peak]]):.4f} rad/s")

    print(f"\n  Impact")
    print(f"    Position      : ({h['x'][-1]:.2f}, {h['y'][-1]:.2f}, 0.00) m")
    print(f"    Time          : {h['t'][-1]:.2f} s")
    print(f"    Speed         : {speed[-1]:.2f} m/s")
    print(f"    Ground range  : {rng:.2f} m from launch")
    print(f"    AoA           : {np.degrees(h['aoa'][-1]):.2f}°")
    print(f"    Torque        : ({h['torque_x'][-1]:.4f}, {h['torque_y'][-1]:.4f}, {h['torque_z'][-1]:.4f}) N·m")

    print(f"\n  Engine at end")
    print(f"    Thrust        : {h['thrust'][-1]:.2f} N  ({100*h['thrust'][-1]/T_max:.4f}% of max)")
    print(f"    Mass          : {h['mass'][-1]:.2f} kg  (fuel left: {h['mass'][-1]-m_dry:.2f} kg)")

    print("\n" + "="*52 + "\n")


def main():
    print("\n" + "="*52)
    print("   3D Missile Trajectory Simulator")
    print("   Body orientation and velocity path tracked separately")
    print("="*52)

    # ── collect all inputs ─────────────────────────────────────────────────
    x0,  y0,  z0         = ask_position()
    vx0, vy0, vz0        = ask_velocity()
    wx0, wy0, wz0        = ask_angular_velocity()
    elevation, azimuth   = ask_body_orientation()
    m_dry, m_fuel        = ask_mass()
    length, radius       = ask_body_shape()
    T_max, k             = ask_engine()

    # show the two direction concepts immediately so the user can verify them
    orientation_vec = angles_to_unit_vector(elevation, azimuth)
    initial_path_vec = velocity_direction(np.array([vx0, vy0, vz0], dtype=float))
    print(f"\n  Body orientation vector : ({orientation_vec[0]:.4f}, {orientation_vec[1]:.4f}, {orientation_vec[2]:.4f})")
    print(f"  Initial path vector     : ({initial_path_vec[0]:.4f}, {initial_path_vec[1]:.4f}, {initial_path_vec[2]:.4f})")
    print(f"  Orientation magnitude   : {np.linalg.norm(orientation_vec):.6f}  (must be 1.0)")
    inertia = inertia_tensor_body(RocketBody(length, radius), m_dry + m_fuel)
    print(f"  Inertia axial/lateral   : {inertia[0,0]:.2f} / {inertia[1,1]:.2f} kg·m²")

    # ── run simulation ─────────────────────────────────────────────────────
    print("\nSimulating...")
    history = run(
        x0, y0, z0, vx0, vy0, vz0,
        elevation, azimuth,
        T_max, k, m_dry, m_fuel,
        length, radius,
        wx0, wy0, wz0
    )

    # ── print results ──────────────────────────────────────────────────────
    print_results(history, x0, y0, z0, elevation, azimuth, T_max, m_dry, orientation_vec)

    # ── show plots ─────────────────────────────────────────────────────────
    show = input("Show plots? (y/n): ").strip().lower()
    if show == 'y':
        from plotting import plot_all
        plot_all(history, x0, y0, z0, elevation, azimuth)


if __name__ == '__main__':
    main()
