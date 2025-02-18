import numpy as np

launch_site = np.array([25.996190, -97.154423, 14.6304])  # Lat/Long Elevation in m
Ve = 3000  # Exhaust velocity (m/s)
Cd = 0.5  # Drag coefficient (approximate for rockets)
AREA = 63.6  # Cross-sectional area (m^2)
rho_0 = 1.225  # Air density at sea level (kg/m^3)
H = 8000  # Atmospheric scale height (m)
GRAVITY = 9.8
dt = .1


