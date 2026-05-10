"""
config.py
---------
All simulation constants and default settings in one place.
Change values here — nowhere else needs to be touched.
"""

# Physics
GRAVITY    = 9.81    # gravitational acceleration (m/s²)

# Simulation
TIME_STEP  = 0.01    # dt — how many seconds between each calculation
MAX_TIME   = 600     # safety cap — stop simulation after this many seconds

# Default missile parameters (used as input hints)
DEFAULT_X0         = 0
DEFAULT_Y0         = 0
DEFAULT_Z0         = 0
DEFAULT_VX0        = 0
DEFAULT_VY0        = 0
DEFAULT_VZ0        = 0
DEFAULT_ELEVATION  = 75      # degrees above horizontal
DEFAULT_AZIMUTH    = 45      # compass direction in degrees
DEFAULT_DRY_MASS   = 500     # kg — missile body without fuel
DEFAULT_FUEL_MASS  = 300     # kg — fuel at launch
DEFAULT_MAX_THRUST = 80000   # Newtons
DEFAULT_BURN_RATE  = 0.1     # k — higher means faster fuel burnoff
