"""
vectors.py
----------
Small vector helpers used by guidance, physics, and recording.

The simulator keeps two directions separate:
  - orientation vector: where the missile body/nose points
  - velocity direction: where the missile is actually moving
"""

import numpy as np


ZERO_VECTOR = np.array([0.0, 0.0, 0.0])


def magnitude(vector):
    """Return the Euclidean length of a vector."""
    return float(np.linalg.norm(vector))


def unit_vector(vector):
    """Return a normalized copy of vector, or zero when vector has no length."""
    length = magnitude(vector)
    if length == 0.0:
        return ZERO_VECTOR.copy()
    return np.asarray(vector, dtype=float) / length


def velocity_direction(velocity_vec):
    """Return the path direction from the current velocity vector."""
    return unit_vector(velocity_vec)


def angle_between(vec_a, vec_b):
    """Return the unsigned angle between two vectors in radians."""
    a = unit_vector(vec_a)
    b = unit_vector(vec_b)

    if magnitude(a) == 0.0 or magnitude(b) == 0.0:
        return 0.0

    cosine = np.clip(np.dot(a, b), -1.0, 1.0)
    return float(np.arccos(cosine))


def perpendicular_toward(reference_vec, target_vec):
    """
    Return the direction perpendicular to reference_vec that points toward target_vec.

    Used for lift: lift is perpendicular to the path direction, in the plane formed
    by velocity direction and body orientation.
    """
    reference = unit_vector(reference_vec)
    target = unit_vector(target_vec)

    if magnitude(reference) == 0.0 or magnitude(target) == 0.0:
        return ZERO_VECTOR.copy()

    perpendicular = target - np.dot(target, reference) * reference
    return unit_vector(perpendicular)


def quaternion_normalize(quaternion):
    """Return a unit quaternion in [w, x, y, z] order."""
    length = magnitude(quaternion)
    if length == 0.0:
        return np.array([1.0, 0.0, 0.0, 0.0])
    return np.asarray(quaternion, dtype=float) / length


def quaternion_conjugate(quaternion):
    """Return the conjugate of a [w, x, y, z] quaternion."""
    q = np.asarray(quaternion, dtype=float)
    return np.array([q[0], -q[1], -q[2], -q[3]])


def quaternion_multiply(q_left, q_right):
    """Multiply two quaternions in [w, x, y, z] order."""
    w1, x1, y1, z1 = q_left
    w2, x2, y2, z2 = q_right

    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2,
    ])


def quaternion_from_axis_angle(axis, angle):
    """Build a unit quaternion from a rotation axis and angle in radians."""
    axis_unit = unit_vector(axis)
    if magnitude(axis_unit) == 0.0:
        return np.array([1.0, 0.0, 0.0, 0.0])

    half_angle = 0.5 * angle
    return quaternion_normalize(np.array([
        np.cos(half_angle),
        axis_unit[0] * np.sin(half_angle),
        axis_unit[1] * np.sin(half_angle),
        axis_unit[2] * np.sin(half_angle),
    ]))


def quaternion_from_vectors(from_vec, to_vec):
    """Return the shortest rotation that maps from_vec onto to_vec."""
    start = unit_vector(from_vec)
    end = unit_vector(to_vec)

    if magnitude(start) == 0.0 or magnitude(end) == 0.0:
        return np.array([1.0, 0.0, 0.0, 0.0])

    dot = np.clip(np.dot(start, end), -1.0, 1.0)
    if dot > 0.999999:
        return np.array([1.0, 0.0, 0.0, 0.0])

    if dot < -0.999999:
        fallback_axis = np.cross(start, np.array([0.0, 0.0, 1.0]))
        if magnitude(fallback_axis) == 0.0:
            fallback_axis = np.cross(start, np.array([0.0, 1.0, 0.0]))
        return quaternion_from_axis_angle(fallback_axis, np.pi)

    axis = np.cross(start, end)
    return quaternion_normalize(np.array([
        1.0 + dot,
        axis[0],
        axis[1],
        axis[2],
    ]))


def rotate_vector(quaternion, vector):
    """Rotate a 3D vector by a unit quaternion."""
    q = quaternion_normalize(quaternion)
    vector_quaternion = np.array([0.0, vector[0], vector[1], vector[2]])
    rotated = quaternion_multiply(
        quaternion_multiply(q, vector_quaternion),
        quaternion_conjugate(q)
    )
    return rotated[1:4]


def quaternion_derivative(quaternion, angular_velocity):
    """Return q_dot for world-frame angular velocity [wx, wy, wz]."""
    omega_quaternion = np.array([
        0.0,
        angular_velocity[0],
        angular_velocity[1],
        angular_velocity[2],
    ])
    return 0.5 * quaternion_multiply(omega_quaternion, quaternion_normalize(quaternion))
