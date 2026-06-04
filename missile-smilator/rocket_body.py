"""
rocket_body.py
--------------
Rigid-body geometry for the simplified rocket shape.

The rocket is modeled as a cylinder:
  - body axis points along local +x
  - center of mass is at the local origin
  - thrust is applied at the center of the rear circular face
"""

from dataclasses import dataclass

import numpy as np

from vectors import rotate_vector


LOCAL_NOSE_AXIS = np.array([1.0, 0.0, 0.0])


@dataclass(frozen=True)
class RocketBody:
    """Simple cylindrical rocket body."""
    length: float
    radius: float

    @property
    def reference_area(self):
        """Frontal area used by the simple drag/lift model."""
        return np.pi * self.radius**2


def center_of_mass_offset():
    """For now, all center-of-mass forces apply at the body origin."""
    return np.zeros(3)


def nose_axis_world(orientation):
    """Return the body/nose axis in world coordinates."""
    return rotate_vector(orientation, LOCAL_NOSE_AXIS)


def rear_thrust_offset_world(body, orientation):
    """Vector from center of mass to the center of the rear circular face."""
    return -0.5 * body.length * nose_axis_world(orientation)


def inertia_tensor_body(body, mass):
    """Return the cylinder inertia tensor in body coordinates."""
    axial = 0.5 * mass * body.radius**2
    lateral = (1.0 / 12.0) * mass * body.length**2 + 0.25 * mass * body.radius**2
    return np.diag([axial, lateral, lateral])


def rotation_matrix_from_quaternion(orientation):
    """Build a world-from-body rotation matrix from the current orientation."""
    x_axis = rotate_vector(orientation, np.array([1.0, 0.0, 0.0]))
    y_axis = rotate_vector(orientation, np.array([0.0, 1.0, 0.0]))
    z_axis = rotate_vector(orientation, np.array([0.0, 0.0, 1.0]))
    return np.column_stack((x_axis, y_axis, z_axis))


def inertia_tensor_world(body, mass, orientation):
    """Return the inertia tensor rotated into world coordinates."""
    rotation = rotation_matrix_from_quaternion(orientation)
    return rotation @ inertia_tensor_body(body, mass) @ rotation.T
