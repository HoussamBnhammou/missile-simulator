"""
inputs.py
---------
Handles all user input prompts.
One function per group of inputs — position, velocity, direction, mass, engine.
"""

from config import (
    DEFAULT_X0, DEFAULT_Y0, DEFAULT_Z0,
    DEFAULT_VX0, DEFAULT_VY0, DEFAULT_VZ0,
    DEFAULT_ELEVATION, DEFAULT_AZIMUTH,
    DEFAULT_DRY_MASS, DEFAULT_FUEL_MASS,
    DEFAULT_MAX_THRUST, DEFAULT_BURN_RATE
)


def ask_float(prompt, default=None):
    """
    Ask the user for a number.
    If they just press enter, use the default value.
    Keeps asking until a valid number is entered.
    """
    while True:
        hint = f" [{default}]" if default is not None else ""
        raw  = input(f"  {prompt}{hint}: ").strip()
        if raw == "" and default is not None:
            return float(default)
        try:
            return float(raw)
        except ValueError:
            print("    Please enter a valid number.")


def ask_position():
    """Ask for initial x, y, z launch position in metres."""
    print("\n── Initial Position (metres) ──")
    x0 = ask_float("x0", DEFAULT_X0)
    y0 = ask_float("y0", DEFAULT_Y0)
    z0 = ask_float("z0 (height above ground)", DEFAULT_Z0)
    return x0, y0, z0


def ask_velocity():
    """Ask for initial vx, vy, vz launch velocity in m/s."""
    print("\n── Initial Velocity (m/s) ──")
    vx0 = ask_float("vx0", DEFAULT_VX0)
    vy0 = ask_float("vy0", DEFAULT_VY0)
    vz0 = ask_float("vz0  (positive = upward)", DEFAULT_VZ0)
    return vx0, vy0, vz0


def ask_thrust_direction():
    """
    Ask for elevation and azimuth angles that define thrust direction.

    elevation — angle above horizontal
        90 = straight up
        45 = diagonal
         0 = purely horizontal

    azimuth — horizontal compass direction
          0 = along +x axis
         90 = along +y axis
        180 = along -x axis
        270 = along -y axis
    """
    print("\n── Thrust Direction ──")
    print("  elevation : 90=straight up | 45=diagonal | 0=horizontal")
    print("  azimuth   : 0=+x | 90=+y | 180=-x | 270=-y")
    elevation = ask_float("elevation angle (degrees)", DEFAULT_ELEVATION)
    azimuth   = ask_float("azimuth   angle (degrees)", DEFAULT_AZIMUTH)
    return elevation, azimuth


def ask_mass():
    """Ask for dry mass and fuel mass in kg."""
    print("\n── Missile Mass ──")
    m_dry  = ask_float("Dry mass  (kg, missile body without fuel)", DEFAULT_DRY_MASS)
    m_fuel = ask_float("Fuel mass (kg, at launch)",                 DEFAULT_FUEL_MASS)
    return m_dry, m_fuel


def ask_engine():
    """Ask for max thrust and burn rate."""
    print("\n── Engine ──")
    T_max = ask_float("Max thrust at launch (N)",               DEFAULT_MAX_THRUST)
    k     = ask_float("Burn rate k  (higher = faster burnoff)", DEFAULT_BURN_RATE)
    return T_max, k
