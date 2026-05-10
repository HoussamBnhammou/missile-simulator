"""
physics.py
----------
Pure physics calculations.
No simulation loop, no plotting, no user input here.

Responsibilities:
  - Thrust force magnitude at time t  (exponential decay as fuel burns)
  - Total missile mass at time t      (decreases as fuel depletes)
  - Total acceleration vector         (thrust + gravity combined)
"""

import numpy as np
from config import GRAVITY


def thrust_magnitude(t, T_max, k):
    """
    Thrust force in Newtons at time t.

    Models exponential decay as fuel is consumed:
        T(t) = T_max * e^(-k*t)

    At t=0  → T = T_max     (full thrust at launch)
    As t→∞  → T → 0         (engine burns out)

    k controls how fast it decays:
        small k (0.01) = long slow burn
        large k (0.5)  = short aggressive burn
    """
    return T_max * np.exp(-k * t)


def total_mass(t, m_dry, m_fuel, k):
    """
    Total missile mass in kg at time t.

    Dry mass is constant (the missile body).
    Fuel mass decays at the same rate as thrust:
        m(t) = m_dry + m_fuel * e^(-k*t)

    This matters because: acceleration = thrust / mass
    As fuel burns → mass drops → same thrust gives more acceleration.
    """
    return m_dry + m_fuel * np.exp(-k * t)


def compute_accelerations(t, vx, vy, vz, thrust_vec, T_max, k, m_dry, m_fuel):
    """
    Compute total acceleration vector [ax, ay, az] at a given moment.

    Two forces act on the missile:
      1. Thrust  — in the direction of thrust_vec, magnitude = T(t)/m(t)
      2. Gravity — always pulls straight down (-z direction)

    Steps:
      1. Get thrust magnitude T(t)
      2. Get current mass m(t)
      3. Thrust acceleration = T / m  (Newton's second law: F = ma → a = F/m)
      4. Multiply by thrust unit vector to get direction
      5. Subtract gravity from the vertical (z) component

    Returns ax, ay, az as a tuple.
    """
    T  = thrust_magnitude(t, T_max, k)
    m  = total_mass(t, m_dry, m_fuel, k)
    a  = T / m                              # scalar thrust acceleration

    tx, ty, tz = thrust_vec

    ax = tx * a                             # horizontal x
    ay = ty * a                             # horizontal y
    az = tz * a - GRAVITY                   # vertical — gravity pulls down

    return ax, ay, az
