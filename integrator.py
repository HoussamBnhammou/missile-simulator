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
from physics import compute_accelerations


def state_derivative(state, t, thrust_vec, T_max, k, m_dry, m_fuel):
    """
    Compute the rate of change of the full state vector.

    State vector:  [x,  y,  z,  vx,  vy,  vz]
    Derivative:    [vx, vy, vz, ax,  ay,  az]

    Meaning:
        dx/dt  = vx   (position changes at the rate of velocity)
        dy/dt  = vy
        dz/dt  = vz
        dvx/dt = ax   (velocity changes at the rate of acceleration)
        dvy/dt = ay
        dvz/dt = az
    """
    x,  y,  z  = state[0], state[1], state[2]
    vx, vy, vz = state[3], state[4], state[5]

    ax, ay, az = compute_accelerations(
        t, vx, vy, vz, thrust_vec,
        T_max, k, m_dry, m_fuel
    )

    return np.array([vx, vy, vz, ax, ay, az])


def rk4_step(state, t, dt, thrust_vec, T_max, k, m_dry, m_fuel):
    """
    Advance the missile state by one time step dt using RK4.

    Takes four slope samples within this single step:
        k1 — at the start         (t)
        k2 — at the midpoint      (t + dt/2), using k1 to get there
        k3 — at the midpoint      (t + dt/2), using k2 to get there
        k4 — at the end           (t + dt),   using k3 to get there

    Returns the new state after dt seconds.
    """
    args = (thrust_vec, T_max, k, m_dry, m_fuel)

    k1 = state_derivative(state,               t,           *args)
    k2 = state_derivative(state + 0.5*dt*k1,   t + 0.5*dt,  *args)
    k3 = state_derivative(state + 0.5*dt*k2,   t + 0.5*dt,  *args)
    k4 = state_derivative(state +     dt*k3,   t +     dt,  *args)

    return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
