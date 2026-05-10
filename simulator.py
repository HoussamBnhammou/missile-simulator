"""
simulator.py
------------
The main simulation loop.

Responsibility:
    Run the missile from launch until it hits the ground.
    At every timestep dt it does three things:
        1. Ask guidance.py  — which direction should thrust point right now?
        2. Ask integrator.py — advance the physics by one dt
        3. Record everything into history

This file does NOT know how forces work (that is physics.py).
This file does NOT know how to steer (that is guidance.py).
This file does NOT know how to integrate (that is integrator.py).
It only orchestrates the loop.
"""

import numpy as np
from physics    import thrust_magnitude, total_mass
from guidance   import get_thrust_vector
from integrator import rk4_step
from config     import TIME_STEP, MAX_TIME


def run(x0, y0, z0, vx0, vy0, vz0,
        elevation_deg, azimuth_deg,
        T_max, k, m_dry, m_fuel):
    """
    Run the full 3D missile trajectory simulation.

    Starts at the given initial position and velocity.
    Stops when the missile hits the ground (z <= 0) after launch.

    Returns a dictionary of recorded history arrays:
        t       — time at each step (seconds)
        x,y,z   — position (metres)
        vx,vy,vz — velocity (m/s)
        thrust  — thrust force magnitude (Newtons)
        mass    — total missile mass (kg)
        tx,ty,tz — thrust unit vector components at each step
    """
    state = np.array([x0, y0, z0, vx0, vy0, vz0], dtype=float)
    t     = 0.0

    # record the initial state
    tv0 = get_thrust_vector(t, state, elevation_deg, azimuth_deg)

    history = {
        't':      [0.0],
        'x':      [x0],  'y':  [y0],  'z':  [z0],
        'vx':     [vx0], 'vy': [vy0], 'vz': [vz0],
        'thrust': [thrust_magnitude(0, T_max, k)],
        'mass':   [total_mass(0, m_dry, m_fuel, k)],
        'tx':     [tv0[0]],
        'ty':     [tv0[1]],
        'tz':     [tv0[2]],
    }

    while True:

        # ── 1. GUIDANCE — where does the thrust point this instant? ────────
        thrust_vec = get_thrust_vector(t, state, elevation_deg, azimuth_deg)

        # ── 2. INTEGRATE — advance missile state by one dt ─────────────────
        state = rk4_step(state, t, TIME_STEP, thrust_vec, T_max, k, m_dry, m_fuel)
        t    += TIME_STEP

        x,  y,  z  = state[0], state[1], state[2]
        vx, vy, vz = state[3], state[4], state[5]

        # ── 3. RECORD — save everything at this timestep ───────────────────
        history['t'].append(t)
        history['x'].append(x);   history['y'].append(y)
        history['z'].append(max(z, 0.0))
        history['vx'].append(vx); history['vy'].append(vy); history['vz'].append(vz)
        history['thrust'].append(thrust_magnitude(t, T_max, k))
        history['mass'].append(total_mass(t, m_dry, m_fuel, k))
        history['tx'].append(thrust_vec[0])
        history['ty'].append(thrust_vec[1])
        history['tz'].append(thrust_vec[2])

        # ── stop conditions ────────────────────────────────────────────────
        if z <= 0 and t > 0.1:
            # missile has returned to ground after launch
            break

        if t > MAX_TIME:
            print(f"  Warning: simulation capped at {MAX_TIME}s.")
            break

    # convert all lists to numpy arrays for easy math and plotting
    return {key: np.array(val) for key, val in history.items()}
