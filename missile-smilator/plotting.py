"""
plotting.py
-----------
All visualization lives here.
No physics, no simulation logic — only charts and plots.

Charts produced:
    1. 3D trajectory with launch point, peak, impact, and orientation arrow
    2. Thrust magnitude over time  (shows the nonlinear decay)
    3. Angular velocity components over time
    4. Orientation and path vector components over time
    5. Speed over time
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_all(history, x0, y0, z0, elevation_deg, azimuth_deg):
    """
    Render all four charts from the simulation history.

    Parameters:
        history       — dictionary of numpy arrays from simulator.run()
        x0, y0, z0   — launch position (for marking on the 3D plot)
        elevation_deg — launch elevation angle (for drawing thrust arrow)
        azimuth_deg   — launch azimuth angle (for drawing thrust arrow)
    """
    fig = plt.figure(figsize=(16, 10))

    _plot_3d_trajectory(fig, history, x0, y0, z0, elevation_deg, azimuth_deg)
    _plot_thrust_magnitude(fig, history)
    _plot_angular_velocity(fig, history)
    _plot_orientation_path_components(fig, history)
    _plot_speed(fig, history)

    plt.suptitle('3D Missile Trajectory — Orientation and Path Kept Separate',
                 fontsize=12, y=1.01)
    plt.tight_layout()
    plt.savefig("missile_angular_velocity_plot.png", dpi=150, bbox_inches="tight")
    print("Saved plot to missile_angular_velocity_plot.png")
    plt.show()


def _plot_3d_trajectory(fig, h, x0, y0, z0, elevation_deg, azimuth_deg):
    """3D flight path with key points marked and sampled body/thrust arrows."""
    ax = fig.add_subplot(231, projection='3d')

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

    # Body orientation is also the thrust direction. Sample it along the path
    # so rotation-driven thrust steering is visible in the 3D view.
    arrow_length = max(h['z'].max(), 1.0) * 0.12
    sample_count = min(8, len(h['t']))
    sample_indexes = np.linspace(0, len(h['t']) - 1, sample_count, dtype=int)
    ax.quiver(
        h['x'][sample_indexes],
        h['y'][sample_indexes],
        h['z'][sample_indexes],
        h['ox'][sample_indexes] * arrow_length,
        h['oy'][sample_indexes] * arrow_length,
        h['oz'][sample_indexes] * arrow_length,
        color='#D85A30',
        linewidth=1.5,
        normalize=False,
        label='Body/thrust direction',
    )

    ax.set_xlabel('X (m)'); ax.set_ylabel('Y (m)'); ax.set_zlabel('Z (m)')
    ax.set_title(f'3D Trajectory  |  launch elev={elevation_deg}°  az={azimuth_deg}°')
    ax.legend(fontsize=8)


def _plot_thrust_magnitude(fig, h):
    """Thrust force over time — shows the nonlinear exponential decay."""
    ax = fig.add_subplot(232)
    ax.plot(h['t'], h['thrust'], color='#D85A30', linewidth=2)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Thrust (N)')
    ax.set_title('Thrust Magnitude vs Time  (nonlinear decay)')
    ax.grid(True, alpha=0.3)


def _plot_angular_velocity(fig, h):
    """Angular velocity components and total angular speed over time."""
    angular_speed = np.sqrt(h['wx']**2 + h['wy']**2 + h['wz']**2)
    ax = fig.add_subplot(233)
    ax.plot(h['t'], h['wx'], color='#378ADD', linewidth=1.8, label='wx')
    ax.plot(h['t'], h['wy'], color='#1D9E75', linewidth=1.8, label='wy')
    ax.plot(h['t'], h['wz'], color='#EF9F27', linewidth=1.8, label='wz')
    ax.plot(h['t'], angular_speed, color='#7C5CBF', linewidth=2, label='|w|')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Angular velocity (rad/s)')
    ax.set_title('Angular Velocity vs Time')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)


def _plot_orientation_path_components(fig, h):
    """
    Body orientation and velocity/path components over time.
    The gap between these directions is the angle of attack.
    """
    ax = fig.add_subplot(234)
    ax.plot(h['t'], h['ox'], color='#378ADD', linewidth=2, label='orientation x')
    ax.plot(h['t'], h['oy'], color='#1D9E75', linewidth=2, label='orientation y')
    ax.plot(h['t'], h['oz'], color='#EF9F27', linewidth=2, label='orientation z')
    ax.plot(h['t'], h['vdx'], color='#378ADD', linestyle='--', label='path x')
    ax.plot(h['t'], h['vdy'], color='#1D9E75', linestyle='--', label='path y')
    ax.plot(h['t'], h['vdz'], color='#EF9F27', linestyle='--', label='path z')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Component value')
    ax.set_title('Body Orientation vs Velocity Path')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)


def _plot_speed(fig, h):
    """Total missile speed and angle of attack over time."""
    speed = np.sqrt(h['vx']**2 + h['vy']**2 + h['vz']**2)
    ax = fig.add_subplot(235)
    ax.plot(h['t'], speed, color='#7C5CBF', linewidth=2)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Speed (m/s)')
    ax.set_title('Speed and Angle of Attack vs Time')
    ax.grid(True, alpha=0.3)

    ax_aoa = ax.twinx()
    ax_aoa.plot(h['t'], np.degrees(h['aoa']), color='#D85A30', linewidth=1.5)
    ax_aoa.set_ylabel('Angle of attack (deg)')
