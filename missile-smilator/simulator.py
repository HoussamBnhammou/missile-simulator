"""
simulator.py
------------
The main simulation loop.

Responsibility:
    Run the missile from launch until it hits the ground.
    At every timestep dt it does three things:
        1. Ask integrator.py — advance the rigid-body state by one dt
        2. Physics computes net force, net torque, and accelerations
        3. Record everything into history

This file does NOT know how forces work (that is physics.py).
This file only uses guidance.py to build the initial launch orientation.
This file does NOT know how to integrate (that is integrator.py).
It only orchestrates the loop.
"""

import numpy as np
from physics    import angle_of_attack, compute_dynamics, thrust_magnitude, total_mass
from guidance   import get_orientation_vector, initial_orientation_quaternion
from integrator import rk4_step
from config     import DEFAULT_LENGTH, DEFAULT_RADIUS, TIME_STEP, MAX_TIME
from rocket_body import RocketBody
from vectors    import velocity_direction


def split_translational_state(state):
    """Return position and velocity vectors from [x, y, z, vx, vy, vz]."""
    return state[0:3], state[3:6]


def split_rotational_state(state):
    """Return orientation quaternion and angular velocity from rigid-body state."""
    return state[6:10], state[10:13]


def append_vector(history, prefix, vector):
    """Append vector components using keys like ox, oy, oz or vdx, vdy, vdz."""
    history[f'{prefix}x'].append(vector[0])
    history[f'{prefix}y'].append(vector[1])
    history[f'{prefix}z'].append(vector[2])


def record_step(history, t, state, body, T_max, k, m_dry, m_fuel):
    """Record one simulation step into the history dictionary."""
    position_vec, velocity_vec = split_translational_state(state)
    orientation, angular_velocity = split_rotational_state(state)
    orientation_vec = get_orientation_vector(t, state, None, None)
    path_vec = velocity_direction(velocity_vec)
    dynamics = compute_dynamics(
        t, velocity_vec, orientation, angular_velocity,
        body, T_max, k, m_dry, m_fuel
    )

    history['t'].append(t)
    history['x'].append(position_vec[0])
    history['y'].append(position_vec[1])
    history['z'].append(max(position_vec[2], 0.0))
    history['vx'].append(velocity_vec[0])
    history['vy'].append(velocity_vec[1])
    history['vz'].append(velocity_vec[2])
    history['thrust'].append(thrust_magnitude(t, T_max, k))
    history['mass'].append(total_mass(t, m_dry, m_fuel, k))
    history['aoa'].append(angle_of_attack(velocity_vec, orientation_vec))
    history['length'].append(body.length)
    history['radius'].append(body.radius)
    history['q0'].append(orientation[0])
    history['q1'].append(orientation[1])
    history['q2'].append(orientation[2])
    history['q3'].append(orientation[3])

    append_vector(history, 'o', orientation_vec)
    append_vector(history, 'vd', path_vec)
    append_vector(history, 'w', angular_velocity)
    append_vector(history, 'torque_', dynamics['torque'])
    append_vector(history, 'force_', dynamics['force'])

    # Keep old thrust-vector keys as aliases for existing plotting/user code.
    append_vector(history, 't', orientation_vec)


def run(x0, y0, z0, vx0, vy0, vz0,
        elevation_deg, azimuth_deg,
        T_max, k, m_dry, m_fuel,
        length=DEFAULT_LENGTH, radius=DEFAULT_RADIUS,
        wx0=0.0, wy0=0.0, wz0=0.0):
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
        ox,oy,oz — missile orientation/body unit vector components
        vdx,vdy,vdz — velocity/path unit vector components
        aoa     — angle of attack in radians
        q0..q3  — orientation quaternion
        wx,wy,wz — angular velocity (rad/s)
        torque_x,torque_y,torque_z — net torque around center of mass
    """
    body = RocketBody(length=length, radius=radius)
    orientation0 = initial_orientation_quaternion(elevation_deg, azimuth_deg)
    state = np.array([
        x0, y0, z0,
        vx0, vy0, vz0,
        orientation0[0], orientation0[1], orientation0[2], orientation0[3],
        wx0, wy0, wz0,
    ], dtype=float)
    t     = 0.0

    # record the initial state
    orientation_vec0 = get_orientation_vector(t, state, elevation_deg, azimuth_deg)
    path0 = velocity_direction(state[3:6])
    dynamics0 = compute_dynamics(
        t, state[3:6], state[6:10], state[10:13],
        body, T_max, k, m_dry, m_fuel
    )

    history = {
        't':      [0.0],
        'x':      [x0],  'y':  [y0],  'z':  [z0],
        'vx':     [vx0], 'vy': [vy0], 'vz': [vz0],
        'thrust': [thrust_magnitude(0, T_max, k)],
        'mass':   [total_mass(0, m_dry, m_fuel, k)],
        'ox':     [orientation_vec0[0]],
        'oy':     [orientation_vec0[1]],
        'oz':     [orientation_vec0[2]],
        'vdx':    [path0[0]],
        'vdy':    [path0[1]],
        'vdz':    [path0[2]],
        'aoa':    [angle_of_attack(state[3:6], orientation_vec0)],
        'q0':     [orientation0[0]],
        'q1':     [orientation0[1]],
        'q2':     [orientation0[2]],
        'q3':     [orientation0[3]],
        'wx':     [wx0], 'wy': [wy0], 'wz': [wz0],
        'torque_x': [dynamics0['torque'][0]],
        'torque_y': [dynamics0['torque'][1]],
        'torque_z': [dynamics0['torque'][2]],
        'force_x':  [dynamics0['force'][0]],
        'force_y':  [dynamics0['force'][1]],
        'force_z':  [dynamics0['force'][2]],
        'length': [body.length],
        'radius': [body.radius],
        'tx':     [orientation_vec0[0]],
        'ty':     [orientation_vec0[1]],
        'tz':     [orientation_vec0[2]],
    }

    while True:

        # ── 1. INTEGRATE — advance rigid-body state by one dt ──────────────
        state = rk4_step(state, t, TIME_STEP, body, T_max, k, m_dry, m_fuel)
        t    += TIME_STEP

        z = state[2]

        # ── 2. RECORD — save everything at this timestep ───────────────────
        record_step(history, t, state, body, T_max, k, m_dry, m_fuel)

        # ── stop conditions ────────────────────────────────────────────────
        if z <= 0 and t > 0.1:
            # missile has returned to ground after launch
            break

        if t > MAX_TIME:
            print(f"  Warning: simulation capped at {MAX_TIME}s.")
            break

    # convert all lists to numpy arrays for easy math and plotting
    return {key: np.array(val) for key, val in history.items()}
