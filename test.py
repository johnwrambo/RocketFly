import matplotlib
from plot import *
import numpy as np
import pandas as pd
from flight_time import get_time
import pymap3d as pm
# INITIAL_VELOCITY = 150 # m/s
# LAUNCH_ANGLE = np.radians(45) # degrees
# GRAVITY = -9.8
# T_LIMIT = get_time(INITIAL_VELOCITY, LAUNCH_ANGLE)
# print(f"Expected Flight Time: {T_LIMIT:.2f} Seconds")
# t_span = np.linspace(0,T_LIMIT,100)
#
# x = INITIAL_VELOCITY*np.cos(LAUNCH_ANGLE)*t_span
# y = (INITIAL_VELOCITY*np.sin(LAUNCH_ANGLE)*t_span) + ((GRAVITY/2)*t_span**2)
# # indices = np.where(y > 0)
# # print(indices)
#
#
# end = indices
#
# print(end)
# print(t_span)
# print(y)
# plot_fun(x,y,f"Launch {initial_velocity} at {launch_angle}\N{DEGREE SIGN}")

# plot_animation(x,y,t_span,initial_velocity,launch_angle)

#
# print(f"X Coord: {x[50]:.2f}")
# print(f"Y Coord: {y[50]:.2f}")
# step = 50
# xdiff = x[step]-x[step-1]
# ydiff = y[step]-y[step-1]
# print(f"X diff: {xdiff:.2f}")
# print(f"Y diff: {ydiff:.2f}")
rocket_enu = np.array([500.0, 300.0, 120.0])
reference_position= np.array([28.5729, -80.6490, 2.0])
position = {"LAT":0.0,"LONG":0.0,"ALT":0.0}
# pm.enu2geodetic(*rocket_enu,*reference_position)
# c = 0
# for keys in position:
#     position[keys] = float(pm.enu2geodetic(*rocket_enu,*reference_position)[c])
#     c += 1
# print(position)
#
# position = {key: float(value) for key, value in zip(position, pm.enu2geodetic(*rocket_enu, *reference_position))}
#
# # print(position)
# rocket_engine = "Raptor"
# rocket_df = pd.read_csv(r"data/engine_data.csv")
# rocket_df.set_index("Engine Name", inplace=True)
# # print(rocket_df.describe())
# engine_specs = rocket_df.loc["Raptor"]
# print(engine_specs)

import numpy as np

# Given values for SpaceX Raptor
Pc = 30e6   # Chamber pressure (Pa)
Tc = 3500    # Chamber temperature (K)
At = 0.052   # Throat area (m²)
Ae = 0.7     # Nozzle exit area (m²)
Pe = 5000    # Exhaust pressure at exit (Pa)
Pa_sea = 101300  # Ambient pressure at sea level (Pa)
Pa_vac = 0   # Ambient pressure in vacuum (Pa)
R = 370      # Specific gas constant for CH4/LOX (J/kg·K)
gamma = 1.25  # Ratio of specific heats

# Compute characteristic velocity c*
c_star = np.sqrt(R * Tc / gamma) * ((2 / (gamma + 1)) ** ((gamma + 1) / (2 * (gamma - 1))))

# Compute mass flow rate
mdot = (Pc * At) / c_star

# Compute exhaust velocity ve
ve = np.sqrt((2 * gamma / (gamma - 1)) * R * Tc * (1 - (Pe / Pc) ** ((gamma - 1) / gamma)))

# Compute total thrust at sea level
thrust_sea = mdot * ve + (Pe - Pa_sea) * Ae

# Compute total thrust in vacuum
thrust_vac = mdot * ve + (Pe - Pa_vac) * Ae

print(f"Mass Flow Rate (ṁ): {mdot:.2f} kg/s")
print(f"Exhaust Velocity (ve): {ve:.2f} m/s")
print(f"Thrust at Sea Level: {thrust_sea / 1000:.2f} kN")
print(f"Thrust in Vacuum: {thrust_vac / 1000:.2f} kN")
