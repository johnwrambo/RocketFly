import numpy
import numpy as np
import rocket
import time
from plot import *
heavy_booster = rocket.Ship()

# heavy_booster.fly()
x = heavy_booster.get_rocket_specs("Raptor")
y = heavy_booster.thrust
# print(y)

# print(f"Thrust at Sea Level: {y/1000:.2f} kN")
# print(y.loc["R"])


gofor = "flight"
while gofor == "flight":
    heavy_booster.fly()
    t = heavy_booster.flight_log["Time"].tolist()
    # if heavy_booster.altitude[-1] >= 30000:
    #     break
    if t[-1] >= 200:
        break

y = heavy_booster.flight_log["ALT"]
print(y)
# x = range(len(y))
# t = heavy_booster.flight_log["Time"].tolist()
v = heavy_booster.flight_log["Velocity"].tolist()
w = heavy_booster.flight_log["Weight"].tolist()
q = heavy_booster.flight_log["Q"].tolist()
f = heavy_booster.flight_log["Fuel"].tolist()
a = heavy_booster.flight_log["Acceleration"].tolist()
print(f"fuel: {f}")
print(f"Acceleration: {a}")
# print(t)
print(v)
# print(w)
# plot_fun(t,f,"Fuel")
plot_fun(t,a,"Acceleration")
# plot_fun(t,q,"Dynamic Pressure")
# plot_fun(t,v,"Velocity")
# plot_fun(t,y,"Altitude")
print(y)

# print(f"LAT x: {heavy_booster.position["LAT"]:.4f} LONG: {heavy_booster.position["LONG"]:.4f} ALT: {heavy_booster.position["ALT"]:.4f} Time: {heavy_booster.flight_time:.2f}")