
# Missile Trajectory Simulator
3D rigid-body missile simulator with nonlinear thrust decay, drag, lift, torque, and quaternion orientation.

---

## What it does

Takes launch position, velocity, angular velocity, body shape, mass, and engine parameters as inputs
and simulates the full 3D flight path until the missile hits the ground.

At every timestep (0.01s) it:
1. Reads the missile body orientation from the quaternion state
2. Keeps body orientation separate from the velocity/path vector
3. Applies thrust at the rear face and gravity/drag/lift at the center of mass
4. Computes net force, torque, linear acceleration, and angular acceleration
5. Integrates position, velocity, quaternion, and angular velocity with RK4

Outputs the peak height, impact coordinates, ground range, time of flight,
orientation, angular velocity, torque, and optionally renders 4 charts.

---

## Requirements

Python 3.x and two libraries:

```bash
pip install numpy matplotlib
```

---

## How to run

```bash
cd missile_sim
python main.py
```

The simulator will prompt you for inputs one by one.
Press **Enter** to accept the default value shown in brackets.

---

## Inputs explained

```
Initial Position (metres)
  x0          — launch position along x-axis          [default: 0]
  y0          — launch position along y-axis          [default: 0]
  z0          — launch height above ground            [default: 0]

Initial Velocity (m/s)
  vx0         — velocity along x-axis at launch       [default: 0]
  vy0         — velocity along y-axis at launch       [default: 0]
  vz0         — vertical velocity, positive = upward  [default: 0]

Initial Angular Velocity (rad/s)
  wx0         — angular velocity around world x       [default: 0]
  wy0         — angular velocity around world y       [default: 0]
  wz0         — angular velocity around world z       [default: 0]

Body Orientation
  elevation   — angle above horizontal (degrees)      [default: 75]
                  90 = straight up
                  45 = diagonal
                   0 = purely horizontal
  azimuth     — compass direction (degrees)           [default: 45]
                   0 = along +x axis
                  90 = along +y axis
                 180 = along -x axis
                 270 = along -y axis

Missile Mass
  dry mass    — missile body weight without fuel (kg) [default: 500]
  fuel mass   — fuel weight at launch (kg)            [default: 300]

Rocket Body Shape
  length      — cylindrical rocket length (m)          [default: 6]
  radius      — cylindrical rocket radius (m)          [default: 0.3]

Engine
  max thrust  — thrust force at launch (Newtons)      [default: 80000]
  burn rate k — how fast thrust decays               [default: 0.1]
                  small k (0.01) = long slow burn
                  large k (0.5)  = short aggressive burn
                  formula: T(t) = T_max * e^(-k*t)
```

---

## Example run

```
── Initial Position (metres) ──
  x0 [0]:
  y0 [0]:
  z0 (height above ground) [0]:

── Initial Velocity (m/s) ──
  vx0 [0]:
  vy0 [0]:
  vz0  (positive = upward) [0]:

── Initial Angular Velocity (rad/s) ──
  wx0  (around world x) [0]:
  wy0  (around world y) [0]:
  wz0  (around world z) [0]:

── Body Orientation ──
  elevation angle (degrees) [75]:
  azimuth   angle (degrees) [45]:

── Missile Mass ──
  Dry mass  (kg, missile body without fuel) [500]:
  Fuel mass (kg, at launch) [300]:

── Rocket Body Shape ──
  Length (m) [6]:
  Radius (m) [0.3]:

── Engine ──
  Max thrust at launch (N) [80000]:
  Burn rate k  (higher = faster burnoff) [0.1]:
```

All defaults accepted → missile fires at 75° elevation, 45° azimuth.

```
  RESULTS
  Launch
    Position      : (0.00, 0.00, 0.00) m
    Mass          : 800.0 kg
    Body shape    : length=6.00 m  radius=0.30 m
    Thrust        : 80000 N
    Body vector   : (0.1830, 0.1830, 0.9659)
    Path vector   : (0.0000, 0.0000, 0.0000)
    Initial AoA   : 0.00°

  Peak
    Height        : 14493.52 m
    Position      : (4187.71, 4187.71, 14493.52) m
    At time       : 56.18 s
    Speed         : 72.02 m/s
    AoA           : 74.97°
    Angular speed : 0.0000 rad/s

  Impact
    Position      : (9161.67, 9161.67, 0.00) m
    Time          : 136.62 s
    Speed         : 251.22 m/s
    Ground range  : 12956.56 m from launch
    AoA           : 138.08°
    Torque        : (0.0000, 0.0000, 0.0000) N·m
```

---

## File structure

```
missile_sim/
│
├── main.py         entry point — run this file
├── config.py       all constants and default values
├── inputs.py       user input prompts
├── physics.py      thrust magnitude, mass decay, accelerations
├── rocket_body.py  cylindrical body geometry and inertia tensor
├── guidance.py     body orientation vector (guidance hook)
├── integrator.py   RK4 numerical integration
├── simulator.py    main simulation loop
├── plotting.py     all matplotlib charts
└── vectors.py      vector and quaternion helpers
```

### What each file is responsible for

| File | Responsibility |
|---|---|
| `config.py` | All magic numbers in one place — edit here to change global settings |
| `inputs.py` | Everything that talks to the user — nothing else handles input |
| `physics.py` | Force and torque calculations — thrust, gravity, drag, lift, mass over time, linear/angular acceleration |
| `rocket_body.py` | Cylindrical body geometry — center of mass, rear thrust point, inertia tensor |
| `guidance.py` | Initial launch orientation and current body vector from quaternion state |
| `integrator.py` | RK4 stepping — advances the 13-value rigid-body state vector |
| `simulator.py` | The loop — calls guidance → integrator → records history each dt |
| `plotting.py` | All charts — change visuals without touching physics |
| `main.py` | Connects everything — inputs → simulate → print → plot |
| `vectors.py` | Shared vector helpers — normalization, path direction, angle of attack |

---

## Changing settings

All simulation constants are in `config.py`:

```python
GRAVITY    = 9.81    # m/s²
TIME_STEP  = 0.01    # seconds per step — smaller = more accurate, slower
MAX_TIME   = 600     # simulation cap in seconds
```

Decrease `TIME_STEP` for higher accuracy. Increase it for faster runs.

---

## Adding a guidance law (Project 3 upgrade)

The current body orientation comes from the quaternion state. Future guidance should create torque by changing thrust direction or thrust application, not by overwriting orientation directly:

```python
# future example:
# thrust_direction = gimbaled_nozzle_direction(state, target)
# torque = cross(rear_thrust_offset, thrust_force)
```

No other file needs to change.

---

## Physics reference

```
Forces on the missile:
  Thrust    T(t) = T_max * exp(-k * t)            [Newtons, decays over time]
  Mass      m(t) = m_dry + m_fuel * exp(-k * t)   [kg, decreases as fuel burns]
  Gravity   Fg = [0, 0, -m*g]                     [Newtons]
  Drag      Fd = -0.5*rho*v²*Cd*A*path_vec        [Newtons]
  Lift      Fl = 0.5*rho*v²*Cl*A*lift_dir         [Newtons]

Force application points:
  gravity, drag, lift  -> center of mass
  thrust               -> center of rear circular face

Two direction vectors:
  orientation_vec  = where the missile body/nose points
  path_vec         = normalized velocity vector
  angle_of_attack  = angle between orientation_vec and path_vec

Rigid-body state:
  position         = [x, y, z]
  velocity         = [vx, vy, vz]
  orientation      = [q0, q1, q2, q3]
  angular_velocity = [wx, wy, wz]

Translation:
  acceleration = net_force / mass

Rotation:
  torque = sum(r x F)
  I_axial   = 0.5 * m * radius²
  I_lateral = (1/12) * m * length² + (1/4) * m * radius²
  angular_acceleration = inverse(I) * torque

Integration: Runge-Kutta 4th order (RK4) at dt = 0.01s
```
