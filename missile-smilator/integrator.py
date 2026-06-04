"""
integrator.py
-------------
Numerical integration using the Runge-Kutta 4th order method (RK4).

Responsibility:
    Take the current missile state and advance it forward by one time step dt.
    Uses physics.py to compute accelerations at each sample point.

Why RK4 and not simpler Euler?
    Euler takes one straight-line guess per step → accumulates error fast.
    RK4 takes four slope samples within the same step and averages them
    with weights → much more accurate, especially when forces change quickly.

RK4 formula:
    k1 = slope at the START of the step
    k2 = slope at the MIDPOINT using k1
    k3 = slope at the MIDPOINT using k2  (more refined than k2)
    k4 = slope at the END using k3

    new_state = old_state + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)

    Midpoint samples are weighted double because the middle of the
    step carries more information about the curve than the endpoints.
"""

import numpy as np
from physics import compute_dynamics
from vectors import quaternion_derivative, quaternion_normalize


def position_from_state(state):
    """Extract position [x, y, z] from the translational state."""
    return state[0:3]


def velocity_from_state(state):
    """Extract velocity [vx, vy, vz] from the translational state."""
    return state[3:6]


def orientation_from_state(state):
    """Extract quaternion [q0, q1, q2, q3] from the rigid-body state."""
    return quaternion_normalize(state[6:10])


def angular_velocity_from_state(state):
    """Extract angular velocity [wx, wy, wz] from the rigid-body state."""
    return state[10:13]


def normalize_state_orientation(state):
    """Keep the quaternion part of state unit-length after integration."""
    normalized = state.copy()
    normalized[6:10] = quaternion_normalize(normalized[6:10])
    return normalized


def state_derivative(state, t, body, T_max, k, m_dry, m_fuel):
    """
    Compute the rate of change of the full state vector.

    State:
        [x, y, z, vx, vy, vz, q0, q1, q2, q3, wx, wy, wz]

    Derivative:
        [vx, vy, vz, ax, ay, az, q0_dot, q1_dot, q2_dot, q3_dot, ax_rot, ay_rot, az_rot]

    Meaning:
        dx/dt  = vx   (position changes at the rate of velocity)
        dy/dt  = vy
        dz/dt  = vz
        dvx/dt = ax   (velocity changes at the rate of acceleration)
        dvy/dt = ay
        dvz/dt = az
        dq/dt  = quaternion derivative from angular velocity
        dw/dt  = angular acceleration from torque and inertia
    """
    velocity_vec = velocity_from_state(state)
    orientation = orientation_from_state(state)
    angular_velocity = angular_velocity_from_state(state)
    dynamics = compute_dynamics(
        t, velocity_vec, orientation, angular_velocity,
        body, T_max, k, m_dry, m_fuel
    )

    return np.concatenate((
        velocity_vec,
        dynamics['linear_acceleration'],
        quaternion_derivative(orientation, angular_velocity),
        dynamics['angular_acceleration'],
    ))


def rk4_step(state, t, dt, body, T_max, k, m_dry, m_fuel):
    """
    Advance the missile state by one time step dt using RK4.

    Takes four slope samples within this single step:
        k1 — at the start         (t)
        k2 — at the midpoint      (t + dt/2), using k1 to get there
        k3 — at the midpoint      (t + dt/2), using k2 to get there
        k4 — at the end           (t + dt),   using k3 to get there

    Returns the new state after dt seconds.
    """
    args = (body, T_max, k, m_dry, m_fuel)

    k1 = state_derivative(state,               t,           *args)
    k2 = state_derivative(state + 0.5*dt*k1,   t + 0.5*dt,  *args)
    k3 = state_derivative(state + 0.5*dt*k2,   t + 0.5*dt,  *args)
    k4 = state_derivative(state +     dt*k3,   t +     dt,  *args)

    return normalize_state_orientation(
        state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
    )
