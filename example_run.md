
# Missile Trajectory Simulator
3D ballistic missile simulator with nonlinear thrust decay and per-timestep guidance hook.

---

## What it does

Takes launch position, velocity, thrust direction, mass, and engine parameters as inputs
and simulates the full 3D flight path until the missile hits the ground.

At every timestep (0.01s) it:
1. Computes the thrust direction vector (guidance hook)
2. Applies thrust + gravity using RK4 numerical integration
3. Records position, velocity, thrust, mass, and thrust vector

Outputs the peak height, impact coordinates, ground range, time of flight,
and optionally renders 4 charts.

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

Thrust Direction
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

── Thrust Direction ──
  elevation angle (degrees) [75]:
  azimuth   angle (degrees) [45]:

── Missile Mass ──
  Dry mass  (kg, missile body without fuel) [500]:
  Fuel mass (kg, at launch) [300]:

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
    Thrust        : 80000 N
    Thrust vector : (0.1830, 0.1830, 0.9659)

  Peak
    Height        : 61098.42 m
    Position      : (25730.17, 25730.17, 61098.42) m
    At time       : 123.41 s
    Speed         : 324.39 m/s

  Impact
    Position      : (51331.00, 51331.00, 0.00) m
    Time          : 235.02 s
    Speed         : 1141.95 m/s
    Ground range  : 72593.00 m from launch
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
├── guidance.py     thrust direction vector (guidance hook)
├── integrator.py   RK4 numerical integration
├── simulator.py    main simulation loop
└── plotting.py     all matplotlib charts
```

### What each file is responsible for

| File | Responsibility |
|---|---|
| `config.py` | All magic numbers in one place — edit here to change global settings |
| `inputs.py` | Everything that talks to the user — nothing else handles input |
| `physics.py` | Force calculations — thrust decay, mass over time, accelerations |
| `guidance.py` | Thrust direction — currently fixed angles, future guidance laws plug in here |
| `integrator.py` | RK4 stepping — advances the state vector by one dt |
| `simulator.py` | The loop — calls guidance → integrator → records history each dt |
| `plotting.py` | All charts — change visuals without touching physics |
| `main.py` | Connects everything — inputs → simulate → print → plot |

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

Open `guidance.py` and replace the internals of `get_thrust_vector()`:

```python
def get_thrust_vector(t, state, elevation_deg, azimuth_deg):
    # current: fixed direction
    return angles_to_unit_vector(elevation_deg, azimuth_deg)

    # future: proportional navigation toward a target
    # target = np.array([target_x, target_y, target_z])
    # return proportional_navigation(state, target)
```

No other file needs to change.

---

## Physics reference

```
Forces on the missile:
  Thrust    T(t) = T_max * exp(-k * t)            [Newtons, decays over time]
  Mass      m(t) = m_dry + m_fuel * exp(-k * t)   [kg, decreases as fuel burns]
  Accel     a(t) = T(t) / m(t)                    [m/s², increases as mass drops]

Thrust direction:
  tx = cos(elevation) * cos(azimuth)
  ty = cos(elevation) * sin(azimuth)
  tz = sin(elevation)

Total accelerations:
  ax = tx * a(t)
  ay = ty * a(t)
  az = tz * a(t) - 9.81                           [gravity subtracts from vertical]

Integration: Runge-Kutta 4th order (RK4) at dt = 0.01s
```