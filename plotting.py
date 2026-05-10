"""
plotting.py
-----------
All visualization lives here.
No physics, no simulation logic — only charts and plots.

Charts produced:
    1. 3D trajectory with launch point, peak, impact, and thrust direction arrow
    2. Thrust magnitude over time  (shows the nonlinear decay)
    3. Thrust vector components over time  (flat now, will curve when guided)
    4. Speed over time
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from guidance import angles_to_unit_vector


def plot_all(history, x0, y0, z0, elevation_deg, azimuth_deg):
    """
    Render all four charts from the simulation history.

    Parameters:
        history       — dictionary of numpy arrays from simulator.run()
        x0, y0, z0   — launch position (for marking on the 3D plot)
        elevation_deg — launch elevation angle (for drawing thrust arrow)
        azimuth_deg   — launch azimuth angle (for drawing thrust arrow)
    """
    fig = plt.figure(figsize=(14, 10))

    _plot_3d_trajectory(fig, history, x0, y0, z0, elevation_deg, azimuth_deg)
    _plot_thrust_magnitude(fig, history)
    _plot_thrust_vector_components(fig, history)
    _plot_speed(fig, history)

    plt.suptitle('3D Missile Trajectory — Per-Timestep Thrust Vector',
                 fontsize=12, y=1.01)
    plt.tight_layout()
    plt.show()


def _plot_3d_trajectory(fig, h, x0, y0, z0, elevation_deg, azimuth_deg):
    """3D flight path with key points marked and thrust direction arrow."""
    ax = fig.add_subplot(221, projection='3d')

    # flight path
    ax.plot(h['x'], h['y'], h['z'],
            color='#378ADD', linewidth=2, label='Trajectory')

    # key points
    peak = h['z'].argmax()
    ax.scatter([x0], [y0], [z0],
               color='#1D9E75', s=70, zorder=5, label='Launch')
    ax.scatter([h['x'][peak]], [h['y'][peak]], [h['z'][peak]],
               color='#EF9F27', s=60, zorder=5,
               label=f"Peak {h['z'][peak]:.0f} m")
    ax.scatter([h['x'][-1]], [h['y'][-1]], [0],
               color='#D85A30', s=70, zorder=5, label='Impact')

    # thrust direction arrow from launch point
    arrow_length = h['z'].max() * 0.3
    tv = angles_to_unit_vector(elevation_deg, azimuth_deg)
    ax.quiver(x0, y0, z0,
              tv[0]*arrow_length, tv[1]*arrow_length, tv[2]*arrow_length,
              color='#D85A30', linewidth=2, label='Thrust dir')

    ax.set_xlabel('X (m)'); ax.set_ylabel('Y (m)'); ax.set_zlabel('Z (m)')
    ax.set_title(f'3D Trajectory  |  elev={elevation_deg}°  az={azimuth_deg}°')
    ax.legend(fontsize=8)


def _plot_thrust_magnitude(fig, h):
    """Thrust force over time — shows the nonlinear exponential decay."""
    ax = fig.add_subplot(222)
    ax.plot(h['t'], h['thrust'], color='#D85A30', linewidth=2)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Thrust (N)')
    ax.set_title('Thrust Magnitude vs Time  (nonlinear decay)')
    ax.grid(True, alpha=0.3)


def _plot_thrust_vector_components(fig, h):
    """
    Thrust vector x, y, z components over time.
    Currently three flat lines — direction is fixed.
    When guidance is added in Project 3, these will curve dynamically.
    """
    ax = fig.add_subplot(223)
    ax.plot(h['t'], h['tx'], color='#378ADD', linewidth=2, label='tx')
    ax.plot(h['t'], h['ty'], color='#1D9E75', linewidth=2, label='ty')
    ax.plot(h['t'], h['tz'], color='#EF9F27', linewidth=2, label='tz')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Component value')
    ax.set_title('Thrust Vector Components vs Time\n'
                 '(flat now — will curve dynamically with guidance)')
    ax.legend()
    ax.grid(True, alpha=0.3)


def _plot_speed(fig, h):
    """Total missile speed over time."""
    speed = np.sqrt(h['vx']**2 + h['vy']**2 + h['vz']**2)
    ax = fig.add_subplot(224)
    ax.plot(h['t'], speed, color='#7C5CBF', linewidth=2)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Speed (m/s)')
    ax.set_title('Speed vs Time')
    ax.grid(True, alpha=0.3)
