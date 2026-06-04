"""
inputs.py
---------
Handles all user input prompts.
One function per group of inputs — position, velocity, orientation, mass, engine.
"""

from config import (
    DEFAULT_X0, DEFAULT_Y0, DEFAULT_Z0,
    DEFAULT_VX0, DEFAULT_VY0, DEFAULT_VZ0,
    DEFAULT_WX0, DEFAULT_WY0, DEFAULT_WZ0,
    DEFAULT_ELEVATION, DEFAULT_AZIMUTH,
    DEFAULT_DRY_MASS, DEFAULT_FUEL_MASS,
    DEFAULT_LENGTH, DEFAULT_RADIUS,
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


def ask_angular_velocity():
    """Ask for initial angular velocity in rad/s."""
    print("\n── Initial Angular Velocity (rad/s) ──")
    wx0 = ask_float("wx0  (around world x)", DEFAULT_WX0)
    wy0 = ask_float("wy0  (around world y)", DEFAULT_WY0)
    wz0 = ask_float("wz0  (around world z)", DEFAULT_WZ0)
    return wx0, wy0, wz0


def ask_body_orientation():
    """
    Ask for elevation and azimuth angles that define body orientation.

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
    print("\n── Body Orientation ──")
    print("  elevation : 90=straight up | 45=diagonal | 0=horizontal")
    print("  azimuth   : 0=+x | 90=+y | 180=-x | 270=-y")
    elevation = ask_float("elevation angle (degrees)", DEFAULT_ELEVATION)
    azimuth   = ask_float("azimuth   angle (degrees)", DEFAULT_AZIMUTH)
    return elevation, azimuth


def ask_thrust_direction():
    """Backward-compatible name for the body orientation prompt."""
    return ask_body_orientation()


def ask_mass():
    """Ask for dry mass and fuel mass in kg."""
    print("\n── Missile Mass ──")
    m_dry  = ask_float("Dry mass  (kg, missile body without fuel)", DEFAULT_DRY_MASS)
    m_fuel = ask_float("Fuel mass (kg, at launch)",                 DEFAULT_FUEL_MASS)
    return m_dry, m_fuel


def ask_body_shape():
    """Ask for the simplified cylindrical rocket shape."""
    print("\n── Rocket Body Shape ──")
    length = ask_float("Length (m)", DEFAULT_LENGTH)
    radius = ask_float("Radius (m)", DEFAULT_RADIUS)
    return length, radius


def ask_engine():
    """Ask for max thrust and burn rate."""
    print("\n── Engine ──")
    T_max = ask_float("Max thrust at launch (N)",               DEFAULT_MAX_THRUST)
    k     = ask_float("Burn rate k  (higher = faster burnoff)", DEFAULT_BURN_RATE)
    return T_max, k
