import sympy as sp
import numpy as np
import time

GRAVITY = -9.8  # M/S


# LAUNCH_PARAMS = [t_span, initial_velocity, launch_angle, GRAVITY]


def get_time(initial_velocity, launch_angle):
    t = sp.symbols('t')
    y = (initial_velocity * np.sin(launch_angle) * t) + ((GRAVITY / 2) * t ** 2)
    solutions = sp.solve(y, t)
    return float(solutions[1])


def altitude_t(t, initial_velocity, launch_angle):
    y = (initial_velocity * np.sin(launch_angle) * t) + ((GRAVITY / 2) * t ** 2)
    return y


def fly(initial_velocity, launch_angle, t_span):
    start_time = time.time()
    x = initial_velocity * np.cos(launch_angle) * t_span
    y = (initial_velocity * np.sin(launch_angle) * t_span) + ((GRAVITY / 2) * t_span ** 2)
