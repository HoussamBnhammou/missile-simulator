"""
guidance.py
-----------
Determines the missile body ORIENTATION at every timestep.

This is completely separate from thrust MAGNITUDE (that lives in physics.py).
Orientation and magnitude are two different things:
  - magnitude = how hard the engine pushes  (physics.py)
  - orientation = where the nose points     (this file)

Current mode: FIXED DIRECTION
    The missile points at a fixed elevation and azimuth set at launch.
    Direction never changes during flight.

Future upgrade — GUIDED MODE:
    Replace the internals of get_orientation_vector() with a guidance law.
    The function already receives time and full missile state,
    so a guidance law can use position and velocity to steer toward a target.

    Examples of guidance laws to plug in here later:
        - Proportional Navigation (PN)
        - Augmented Proportional Navigation (APN)
        - Pure Pursuit
        - Optimal Guidance Law (OGL)
"""

import numpy as np
from rocket_body import LOCAL_NOSE_AXIS, nose_axis_world
from vectors import quaternion_from_vectors


def angles_to_unit_vector(elevation_deg, azimuth_deg):
    """
    Convert elevation and azimuth angles into a 3D unit vector.

    Uses aerospace convention — elevation measured UP from horizontal:
        tx = cos(elevation) * cos(azimuth)   ← x component
        ty = cos(elevation) * sin(azimuth)   ← y component
        tz = sin(elevation)                  ← z (vertical) component

    Sanity check:
        elevation=90, any azimuth → vector = (0, 0, 1) = straight up
        elevation=0,  azimuth=0   → vector = (1, 0, 0) = along x-axis
        elevation=0,  azimuth=90  → vector = (0, 1, 0) = along y-axis

    Returned vector always has magnitude = 1.0
    """
    el = np.radians(elevation_deg)
    az = np.radians(azimuth_deg)

    tx = np.cos(el) * np.cos(az)
    ty = np.cos(el) * np.sin(az)
    tz = np.sin(el)

    return np.array([tx, ty, tz])


def initial_orientation_quaternion(elevation_deg, azimuth_deg):
    """Create the launch quaternion from elevation and azimuth angles."""
    return quaternion_from_vectors(
        LOCAL_NOSE_AXIS,
        angles_to_unit_vector(elevation_deg, azimuth_deg),
    )


def get_orientation_vector(t, state, elevation_deg, azimuth_deg):
    """
    Returns the missile orientation unit vector at time t.

    Called at EVERY timestep dt during the simulation loop.
    This is where the missile decides which way to point its nose/body axis.

    Parameters:
        t             — current simulation time (seconds)
        state         — current missile state [x, y, z, vx, vy, vz]
        elevation_deg — launch elevation angle (degrees)
        azimuth_deg   — launch azimuth angle (degrees)

    Returns:
        np.array([ox, oy, oz]) — unit vector, magnitude always = 1.0

    ┌──────────────────────────────────────────────────────────────┐
    │  GUIDANCE HOOK — this is where Project 3 plugs in           │
    │                                                              │
    │  To add proportional navigation guidance:                   │
    │    1. Add target position as a parameter                    │
    │    2. Compute line-of-sight vector from missile to target   │
    │    3. Apply PN law to get steering direction                │
    │    4. Return the new unit vector                            │
    │                                                              │
    │  Everything else in the simulator stays exactly the same.   │
    └──────────────────────────────────────────────────────────────┘
    """
    if len(state) >= 10:
        return nose_axis_world(state[6:10])

    return angles_to_unit_vector(elevation_deg, azimuth_deg)


def get_thrust_vector(t, state, elevation_deg, azimuth_deg):
    """Backward-compatible name for code that still asks for thrust direction."""
    return get_orientation_vector(t, state, elevation_deg, azimuth_deg)
