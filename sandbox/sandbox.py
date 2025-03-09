import time
import math as m
import scipy.integrate
import numpy as np
import pygame
from numba import jit
import colorsys
import copy


def printIF(boolean: bool, printString: str):
    """prints printString if boolean == True"""
    if boolean:
        print(printString)




@jit(nopython=True)
def hamiltonian_derivatives(t, state, m1, m2, l1, l2, g):
    """Computes time derivatives of the Hamiltonian system more efficiently."""
    θ1, θ2, p1, p2 = state

    c, s = np.cos(θ1 - θ2), np.sin(θ1 - θ2)
    denom = m1 + m2 * s**2

    # Precompute common terms
    l1_sq, l2_sq = l1**2, l2**2
    m2_l2_sq = m2 * l2_sq
    m2_l1_l2_c = m2 * l1 * l2 * c

    # Angular velocities
    θ1_dot = (p1 * m2_l2_sq - p2 * m2_l1_l2_c) / (l1_sq * l2_sq * denom)
    θ2_dot = (p2 * (m1 * l1_sq + m2 * l1_sq + m2_l1_l2_c) -
              p1 * m2_l1_l2_c) / (l1_sq * l2_sq * denom)

    # Moment changes
    p1_dot = -(m1 + m2) * g * l1 * np.sin(θ1) - \
        m2 * l1 * l2 * θ1_dot * θ2_dot * s
    p2_dot = -m2 * g * l2 * np.sin(θ2) + m2 * l1 * l2 * θ1_dot * θ2_dot * s

    return np.array([θ1_dot, θ2_dot, p1_dot, p2_dot])


def simulate_double_pendulum(theta1_0,
                             theta2_0,
                             t_max,
                             m1=1,
                             m2=1,
                             l1=1,
                             l2=1,
                             g=9.81,
                             p1_0=0,
                             p2_0=0,
                             dt=0.01):
    """
    Simulates a double pendulum using Hamiltonian mechanics efficiently.

    Parameters:
        theta1_0, theta2_0 : float - Initial angles (radians)
        p1_0, p2_0 : float - Initial conjugate momenta
        t_max  : float - Maximum simulation time
        dt     : float - Time step between frames
        m1, m2 : float - Masses of the pendulum arms
        l1, l2 : float - Lengths of the rods
        g      : float - Gravitational acceleration

    Returns:
        t_eval : ndarray - Time steps of the simulation
        states : ndarray - Frame-by-frame state [theta1, theta2, p1, p2]
    """

    state0 = np.array([theta1_0, theta2_0, p1_0, p2_0])
    t_eval = np.arange(0, t_max, dt)  # Time steps

    # Solve ODEs using DOP853 (higher-order Runge-Kutta, better for chaotic systems)
    solution = scipy.integrate.solve_ivp(
        lambda t, y: hamiltonian_derivatives(t, y, m1, m2, l1, l2, g),
        [0, t_max], state0, t_eval=t_eval, method='DOP853'
    )

    return t_eval, solution.y.T  # Transposed so rows are time steps


import pygame
import time
import colorsys
import numpy as np
import math as m

def grid_sim(theta1_range: tuple,
             theta2_range: tuple,
             sim_height: int = 50,
             sim_width: int = 50,
             screen_height: int = 200,
             screen_width: int = 200,
             m1: float = 1,
             m2: float = 1,
             l1: float = 1,
             l2: float = 1,
             g: float = 9.81,
             p1_0: float = 0,
             p2_0: float = 0,
             dt: float = 0.01,
             chaotic_threshold_omega: float = 5.0,
             chaotic_threshold_alpha: float = 10.0,
             printDeets: bool = False):

    pygame.init()
    if sim_height > screen_height:
        sim_height = screen_height
    if sim_width > screen_width:
        sim_width = screen_width

    pixel_size_x = m.floor(screen_width / sim_width)
    pixel_size_y = m.floor(screen_height / sim_height)

    screen_width_scaled = sim_width * pixel_size_x
    screen_height_scaled = sim_height * pixel_size_y

    screen = pygame.display.set_mode((screen_width_scaled, screen_height_scaled))

    time_chunk = 10
    current_sim_time = 0

    prev_last_DP_state = np.zeros((sim_height, sim_width, 4)) #Initialize with correct dimensions.
    pixels = np.zeros((int(time_chunk / dt), sim_height, sim_width, 3), dtype=np.uint8)

    for i in range(sim_height):
        for j in range(sim_width):
            theta1 = (theta1_range[1] - theta1_range[0]) / (sim_width - 1) * j + theta1_range[0]
            theta2 = (theta2_range[1] - theta2_range[0]) / (sim_height - 1) * i + theta2_range[0]
            t_eval, state = simulate_double_pendulum(theta1, theta2, time_chunk, m1, m2, l1, l2, g, p1_0, p2_0, dt)
            prev_last_DP_state[i, j] = state[-1]

            saturation = 1.0
            for t_idx in range(int(time_chunk / dt)):
                theta1, theta2, p1, p2 = state[t_idx]
                hue = (theta1 % (2 * np.pi)) / (2 * np.pi)
                brightness = 0.3 + 0.7 * abs(np.sin(theta2))
                color = colorsys.hsv_to_rgb(hue, saturation, brightness)
                color_8bit = tuple(int(c * 255) for c in color)
                pixels[t_idx, i, j] = color_8bit

        printIF(printDeets, f"initial render: row {i + 1}/{sim_height} done")

    last_frame_time = chunk_start_time = time.perf_counter()
    t = 0

    while True:
        if (time.perf_counter() - chunk_start_time) >= time_chunk:
            for i in range(sim_height):
                for j in range(sim_width):
                    theta1, theta2, p1, p2 = prev_last_DP_state[i, j]
                    t_eval, state = simulate_double_pendulum(theta1, theta2, time_chunk, m1, m2, l1, l2, g, p1, p2, dt)
                    prev_last_DP_state[i, j] = state[-1]

                    saturation = 1.0
                    for t_idx in range(int(time_chunk / dt)):
                        theta1, theta2, p1, p2 = state[t_idx]
                        hue = (theta1 % (2 * np.pi)) / (2 * np.pi)
                        brightness = 0.3 + 0.7 * abs(np.sin(theta2))
                        color = colorsys.hsv_to_rgb(hue, saturation, brightness)
                        color_8bit = tuple(int(c * 255) for c in color)
                        pixels[t_idx, i, j] = color_8bit

                printIF(printDeets, f"render: row {i + 1}/{sim_height} done")

            last_frame_time = chunk_start_time = time.perf_counter()
            t = 0
        else:
            pixel_array = pygame.surfarray.pixels3d(screen)
            for y in range(sim_height):
                for x in range(sim_width):
                    color = pixels[t, y, x]
                    for px in range(pixel_size_x):
                        for py in range(pixel_size_y):
                            pixel_array[x * pixel_size_x + px, y * pixel_size_y + py] = color

            t = m.floor((time.perf_counter()-(current_sim_time + chunk_start_time))/dt)
            print(t, current_sim_time)
            last_frame_time = time.perf_counter()
            current_sim_time += time.perf_counter() - last_frame_time
            

            del pixel_array
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()



grid_sim((-np.pi/2,np.pi/2),(-np.pi/2,np.pi/2),50,50,500,500,printDeets=True)