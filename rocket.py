import numpy as np
import time
import pandas as pd
import pymap3d as pm

launch_site = np.array([25.996190, -97.154423, 14.6304])  # Lat/Long Elevation in m
Ve = 3000  # Exhaust velocity (m/s)
Cd = 0.5  # Drag coefficient (approximate for rockets)
AREA = 63.6  # Cross-sectional area (m^2)
rho_0 = 1.225  # Air density at sea level (kg/m^3)
H = 8000  # Atmospheric scale height (m)
GRAVITY = 9.8
dt = .1
# tons_kg = 907.2
# rocket_mass: float = 5_080_235 # 5600 tons
# heavy_booster_mass = 1100 #tons
# starship_mass = 1200 # tons
# fuel = 2700* tons_kg
# rocket_mass = (heavy_booster_mass+starship_mass)*tons_kg


class Ship:
    def __init__(self, position: object = launch_site, fuel_mass: float = 2700*907.2, thrust: float = 2_260_000,
                 rocket_mass: float = 2_086_560, engines: int = 33,
                 burn_rate: float = 650,
                 rocket_engine="Raptor"
                 ):
        self.initial_velcoity = None
        self.azimuth = None
        self.elevation = np.radians(90)  # degrees
        self.engine_specs = self.get_rocket_specs(rocket_engine)
        self.engines = engines
        self.fuel_mass = fuel_mass
        self.thrust = 0  # Newtons x number of Raptor engines
        self.thrust_vec = np.array([0.0, 0.0, 0.0]) * self.thrust
        self.displacement_enu = np.array([0.0, 0.0, 0.0])  # displaced distance in meters from origin in 3 axis
        self.velocity_vec = np.array([0.0, 0.0, 0.0])  # Velocity vector
        self.acceleration_vec = np.array([0.0, 0.0, 0.0])  # Acceleration vector
        self.position = {"LAT": 0.0, "LONG": 0.0, "ALT": 0.0}  # Position on the earth in lat/long
        self.burn_rate = burn_rate  # how fast fuel burns
        self.rocket_mass = rocket_mass
        self.total_mass = self.rocket_mass + self.fuel_mass  # kg
        self.weight_vec = np.array([0.0, 0.0, -self.total_mass * GRAVITY])
        self.flight_time = 0.0
        self.flight_log = pd.DataFrame(
            {"LAT": [0], "LONG": [0], "ALT": [0], "Time": [0.00], "Velocity": 0.0, "Acceleration": 0.0,
             "Weight": self.weight_vec[2], "Q": 0.0, "Fuel": self.fuel_mass})
        self.altitude = []  #  ['LAT', 'LONG', 'ALT', "Time", "Velocity", "Acceleration"]

    def launch(self, initial_velocity, flight_path):
        self.initial_velcoity = initial_velocity
        self.elevation = flight_path

    def velocity_(self):
        ve = isp*GRAVITY
        delta_v = ve*ln(m0/mf)
    def get_thrust(self):
        if self.fuel_mass > 0:
            max_thrust = 2_260_000 * 33
            print(self.engine_specs)
            self.thrust = max_thrust
            return max_thrust
        else:
            self.thrust = 0
            return 0
        #     print(self.engine_specs.index)
        #     R = self.engine_specs.loc["R"]
        #     Tc = self.engine_specs.loc["Tc"]
        #     gamma = self.engine_specs.loc["gamma"]
        #     Pc = self.engine_specs.loc["Pc"]
        #     At = self.engine_specs.loc["At"]
        #     Ae = self.engine_specs.loc["Ae"]
        #     Pe = self.engine_specs.loc["Pe"]
        #     Pa = self.engine_specs.loc["Pa"]
        #     # Compute characteristic velocity c*
        #     c_star = np.sqrt(R * Tc / gamma) * ((2 / (gamma + 1)) ** ((gamma + 1) / (2 * (gamma - 1))))
        #
        #     # Compute mass flow rate
        #     mdot = (Pc * At) / c_star
        #
        #     # Compute exhaust velocity ve
        #     ve = np.sqrt((2 * gamma / (gamma - 1)) * R * Tc * (1 - (Pe / Pc) ** ((gamma - 1) / gamma)))
        #
        #     # Compute total thrust at sea level
        #     thrust_sea = mdot * ve + (Pe - Pa) * Ae
        #
        #     return thrust_sea

    def get_position(self):
        self.position = {key: float(value) for key, value in
                         zip(self.position, pm.enu2geodetic(*self.displacement_enu, *launch_site))}

        return self.position

    def get_velocity(self):
        return np.linalg.norm(self.velocity_vec)

    def get_acceleration(self):
        return np.linalg.norm(self.acceleration_vec)

    def get_rocket_specs(self, rocket_engine):
        rocket_df = pd.read_csv(r"data/engine_data.csv")
        rocket_df.set_index("Engine Name", inplace=True)
        engine_specs = rocket_df.loc[rocket_engine]
        self.engine_specs = engine_specs
        return self.engine_specs


    def fly(self):
        # Step 1: Accumulate velocity updates rather than overwriting.
        self.get_thrust()
        rho = rho_0 * np.exp(-self.position["ALT"] / H)
        drag_magnitude = 0.5 * Cd * rho * (self.get_velocity() ** 2) * AREA
        speed = self.get_velocity()
        dynamic_pressure = .5 * rho * speed ** 2
        if speed > 0:
            drag_vec = -self.velocity_vec / speed * drag_magnitude
        else:
            drag_vec = np.array([0.0, 0.0, 0.0])

        if not self.azimuth:
            self.thrust_vec[0] = 0
            self.thrust_vec[1] = 0
            self.thrust_vec[2] = self.thrust * np.sin(self.elevation)
        else:
            self.thrust_vec[0] = self.thrust * np.cos(self.azimuth) * np.cos(self.elevation)
            self.thrust_vec[1] = self.thrust * np.sin(self.azimuth) * np.cos(self.elevation)
            self.thrust_vec[2] = self.thrust * np.sin(self.elevation)

        # print(f"Thrust: {self.thrust_vec}")
        net_force = self.thrust_vec + self.weight_vec + drag_vec

        # Update accelerations
        self.acceleration_vec = (net_force / self.total_mass)
        acceleration = self.get_acceleration()
        # Update velocity
        self.velocity_vec += self.acceleration_vec * dt

        # Update position
        self.displacement_enu += self.velocity_vec * dt
        self.position = self.get_position()
        self.altitude.append(self.position["ALT"])

        # Burn fuel
        if self.fuel_mass > 0:
            self.fuel_mass -= self.burn_rate * self.engines * dt
            self.total_mass = self.rocket_mass + self.fuel_mass  # recalc each step
            self.weight_vec = np.array([0.0, 0.0, -self.total_mass * GRAVITY])  # if you want to keep it 'positive up'
        else:
            self.burn_rate = 0
            self.fuel_mass = 0

        # Increase time
        self.flight_time += dt

        # Log flight path
        new_row = pd.DataFrame([[self.position["LAT"], self.position["LONG"], self.position["ALT"], self.flight_time,
                                 speed, self.thrust, acceleration, self.weight_vec[2], dynamic_pressure, self.fuel_mass]],
                               columns=['LAT', 'LONG', 'ALT', "Time", "Velocity", "Thrust",  "Acceleration", "Weight", "Q",
                                        "Fuel"])
        self.flight_log = pd.concat([self.flight_log, new_row], ignore_index=True)
        # print(self.displacement_enu)

        # print(
        #     f"LAT x: {self.position["LAT"]:.4f} LONG: {self.position["LONG"]:.4f} ALT: {self.position["ALT"]:.4f} Time: {self.flight_time:.2f}")
