"""
physics.py
----------
Pure physics calculations.
No simulation loop, no plotting, no user input here.

Responsibilities:
  - Thrust force magnitude at time t  (exponential decay as fuel burns)
  - Total missile mass at time t      (decreases as fuel depletes)
  - Force blocks                      (thrust, gravity, drag, lift)
  - Torque from force application points
  - Linear and angular acceleration
"""

from dataclasses import dataclass

import numpy as np
from config import (
    AIR_DENSITY,
    DRAG_COEFFICIENT,
    GRAVITY,
    LIFT_COEFFICIENT_SLOPE,
)
from rocket_body import (
    center_of_mass_offset,
    inertia_tensor_world,
    nose_axis_world,
    rear_thrust_offset_world,
)
from vectors import angle_between, magnitude, perpendicular_toward, unit_vector, velocity_direction


@dataclass(frozen=True)
class ForceApplication:
    """A force vector applied at an offset from the center of mass."""
    name: str
    force: np.ndarray
    offset: np.ndarray


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


def force_thrust(t, thrust_direction_vec, T_max, k):
    """Engine force. Direction comes from the missile body/nose orientation."""
    return thrust_magnitude(t, T_max, k) * unit_vector(thrust_direction_vec)


def force_gravity(mass):
    """Gravity force. Always straight down in the z axis."""
    return np.array([0.0, 0.0, -mass * GRAVITY])


def dynamic_pressure(speed):
    """Aerodynamic pressure term: q = 0.5 * rho * v²."""
    return 0.5 * AIR_DENSITY * speed**2


def force_drag(velocity_vec, body):
    """Drag force. Always points opposite the velocity/path direction."""
    speed = magnitude(velocity_vec)
    if speed == 0.0:
        return np.zeros(3)

    drag_magnitude = dynamic_pressure(speed) * DRAG_COEFFICIENT * body.reference_area
    return -drag_magnitude * velocity_direction(velocity_vec)


def angle_of_attack(velocity_vec, orientation_vec):
    """Angle between where the missile points and where it is moving."""
    return angle_between(velocity_vec, orientation_vec)


def force_lift(velocity_vec, orientation_vec, body):
    """
    Lift force from angle of attack.

    Direction is perpendicular to the path and points toward the missile body axis.
    Magnitude grows with speed and angle of attack.
    """
    speed = magnitude(velocity_vec)
    if speed == 0.0:
        return np.zeros(3)

    aoa = angle_of_attack(velocity_vec, orientation_vec)
    lift_coefficient = LIFT_COEFFICIENT_SLOPE * aoa
    lift_magnitude = dynamic_pressure(speed) * lift_coefficient * body.reference_area
    lift_direction = perpendicular_toward(velocity_vec, orientation_vec)

    return lift_magnitude * lift_direction


def force_applications(t, velocity_vec, orientation, body, T_max, k, m_dry, m_fuel):
    """
    Build all forces with their application points.

    Gravity, drag, and lift are applied at the center of mass for now.
    Thrust is applied at the center of the rear circular face.
    """
    mass = total_mass(t, m_dry, m_fuel, k)
    orientation_vec = nose_axis_world(orientation)
    cm_offset = center_of_mass_offset()

    return [
        ForceApplication(
            'thrust',
            force_thrust(t, orientation_vec, T_max, k),
            rear_thrust_offset_world(body, orientation),
        ),
        ForceApplication('gravity', force_gravity(mass), cm_offset),
        ForceApplication('drag', force_drag(velocity_vec, body), cm_offset),
        ForceApplication('lift', force_lift(velocity_vec, orientation_vec, body), cm_offset),
    ]


def net_force(applications):
    """Sum all applied force vectors."""
    return sum((application.force for application in applications), np.zeros(3))


def net_torque(applications):
    """Sum torque from each force application using tau = r x F."""
    return sum(
        (np.cross(application.offset, application.force) for application in applications),
        np.zeros(3),
    )


def angular_acceleration(torque, angular_velocity, body, mass, orientation):
    """Compute angular acceleration from torque and the current inertia tensor."""
    inertia = inertia_tensor_world(body, mass, orientation)
    angular_momentum = inertia @ angular_velocity
    gyroscopic_term = np.cross(angular_velocity, angular_momentum)
    return np.linalg.solve(inertia, torque - gyroscopic_term)


def compute_dynamics(t, velocity_vec, orientation, angular_velocity,
                     body, T_max, k, m_dry, m_fuel):
    """Compute force, torque, linear acceleration, and angular acceleration."""
    mass = total_mass(t, m_dry, m_fuel, k)
    applications = force_applications(
        t, velocity_vec, orientation,
        body, T_max, k, m_dry, m_fuel
    )
    force = net_force(applications)
    torque = net_torque(applications)

    return {
        'applications': applications,
        'force': force,
        'torque': torque,
        'linear_acceleration': force / mass,
        'angular_acceleration': angular_acceleration(
            torque, angular_velocity, body, mass, orientation
        ),
    }


def compute_accelerations(t, velocity_vec, orientation, body, T_max, k, m_dry, m_fuel):
    """Backward-compatible linear acceleration helper."""
    dynamics = compute_dynamics(
        t, velocity_vec, orientation, np.zeros(3),
        body, T_max, k, m_dry, m_fuel
    )
    acceleration = dynamics['linear_acceleration']

    return acceleration[0], acceleration[1], acceleration[2]
