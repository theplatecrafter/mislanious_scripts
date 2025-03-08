import math as m
import scipy.integrate
import numpy as np
import pygame
from numba import jit
import colorsys
import copy


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
    
    pixel_size_x = m.floor(screen_width/sim_width)
    pixel_size_y = m.floor(screen_height/sim_height)
    
    screen_width = sim_width * pixel_size_x
    screen_height = sim_height * pixel_size_y

    
    screen = pygame.display.set_mode((screen_width,screen_height))

    prev_DP_state= []
    for i in range(sim_height):
        prev_DP_state.append([])
        for j in range(sim_width):
            theta1 = (theta1_range[1]-theta1_range[0])/(sim_width-1)*j+theta1_range[0]
            theta2 = (theta2_range[1]-theta2_range[0])/(sim_height-1)*i+theta2_range[0]

            state = (theta1, theta2, p1_0, p2_0)
            prev_DP_state[-1].append(state)

    while True:
        next_DP_state = []
        pixel_array = pygame.surfarray.pixels3d(screen)
        for i in range(sim_height):
            next_DP_state.append([])
            for j in range(sim_width):
                theta1, theta2, p1, p2 = prev_DP_state[i][j]

                t_eval, state = simulate_double_pendulum(theta1, theta2, dt, m1, m2, l1, l2, g, p1, p2, dt)
                next_DP_state[-1].append(state[0])

                saturation = 1.0
                theta1, theta2, p1, p2 = state[0]
                hue = (theta1 % (2 * np.pi)) / (2 * np.pi)
                brightness = 0.3 + 0.7 * abs(np.sin(theta2))
                color = colorsys.hsv_to_rgb(hue, saturation, brightness)
                color_8bit = tuple(int(c * 255) for c in color)
                for x in range(pixel_size_x):
                    for y in range(pixel_size_y):
                        pixel_array[j * pixel_size_x + x, i * pixel_size_y + y] = color_8bit

        print("w")

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        prev_DP_state = copy.deepcopy(next_DP_state)


grid_sim((-np.pi/2,np.pi/2),(-np.pi/2,np.pi/2),20,20)