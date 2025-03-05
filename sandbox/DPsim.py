import numpy as np
import scipy.integrate
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os


def simulate_double_pendulum(theta1_0: float, theta2_0: float, t_max: float, m1: float = 1, m2: float = 1, l1: float = 1, l2: float = 1, g: float = 9.81, p1_0: float = 0, p2_0: float = 0, dt: float = 0.01):
    """
    Simulates a double pendulum using Hamiltonian mechanics.

    Parameters:
        m1, m2 : float - Masses of the pendulum arms
        l1, l2 : float - Lengths of the rods
        g      : float - Gravitational acceleration
        theta1_0, theta2_0 : float - Initial angles (radians)
        p1_0, p2_0 : float - Initial conjugate momenta
        t_max  : float - Maximum simulation time
        dt     : float - Time step between frames

    Returns:
        t_eval : ndarray - Time steps of the simulation
        states : ndarray - Frame-by-frame state [theta1, theta2, p1, p2]
    """

    def hamiltonian_derivatives(t, state):
        """Computes time derivatives of the Hamiltonian system."""
        θ1, θ2, p1, p2 = state
        c = np.cos(θ1 - θ2)
        s = np.sin(θ1 - θ2)
        denom = m1 + m2 * s**2

        # Angular velocities
        θ1_dot = (p1 * (m2 * l2**2) - p2 * (m2 * l1 * l2 * c)) / (l1**2 * l2**2 * denom)
        θ2_dot = (p2 * (m1 * l1**2 + m2 * l1**2 + m2 * l1 * l2 * c) - p1 * (m2 * l1 * l2 * c)) / (l1**2 * l2**2 * denom)

        # Moment changes
        p1_dot = -(m1 + m2) * g * l1 * np.sin(θ1) - m2 * l1 * l2 * (θ1_dot * θ2_dot * s)
        p2_dot = -m2 * g * l2 * np.sin(θ2) + m2 * l1 * l2 * (θ1_dot * θ2_dot * s)

        return [θ1_dot, θ2_dot, p1_dot, p2_dot]

    # Initial conditions
    state0 = [theta1_0, theta2_0, p1_0, p2_0]
    t_eval = np.arange(0, t_max, dt)  # Time steps

    # Solve equations using SciPy
    solution = scipy.integrate.solve_ivp(
        hamiltonian_derivatives, [0, t_max], state0, t_eval=t_eval, method='RK45'
    )

    return t_eval, solution.y.T  # Transposed so rows are time steps


def visualize_double_pendulum(theta1_0:float, theta2_0:float, t_max:float, output_dir:str = "", video_name:str = "double_pendulum", m1:float = 1, m2:float = 1, l1:float = 1, l2:float = 1, g:float = 9.81, p1_0:float = 0, p2_0:float = 0, dt:float = 0.01):
    """
    Creates an animation of the double pendulum from the simulation data.
    
    Parameters:
        m1, m2 : float - Masses of the pendulum arms
        l1, l2 : float - Lengths of the rods
        g      : float - Gravitational acceleration
        theta1_0, theta2_0 : float - Initial angles (radians)
        p1_0, p2_0 : float - Initial conjugate momenta
        t_max  : float - Maximum simulation time
        dt     : float - Time step between frames
    """

    t_eval, states = simulate_double_pendulum(theta1_0, theta2_0, t_max, m1, m2, l1, l2, g, p1_0, p2_0, dt)

    theta1, theta2 = states[:, 0], states[:, 1]


    x1, y1 = l1 * np.sin(theta1), -l1 * np.cos(theta1)
    x2, y2 = x1 + l2 * np.sin(theta2), y1 - l2 * np.cos(theta2)


    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(-l1 - l2 - 0.1, l1 + l2 + 0.1)
    ax.set_ylim(-l1 - l2 - 0.1, l1 + l2 + 0.1)
    ax.set_aspect('equal')
    ax.grid()

    line, = ax.plot([], [], 'o-', lw=2)
    trace, = ax.plot([], [], 'r-', alpha=0.5, lw=1)
    trace_x, trace_y = [], []

    def init():
        line.set_data([], [])
        trace.set_data([], [])
        return line, trace

    def update(i):
        # Update pendulum positions
        line.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])

        # Update trace
        trace_x.append(x2[i])
        trace_y.append(y2[i])
        trace.set_data(trace_x, trace_y)

        return line, trace

    

    ani = animation.FuncAnimation(fig, update, frames=len(t_eval), init_func=init, blit=True)

    # Save as MP4 video
    out = os.path.join(output_dir,video_name+".mp4")
    ani.save(out, fps=1/dt, writer="ffmpeg")
    plt.close(fig)  # Close figure to avoid display issues

    print(f"Animation saved as {out}")




visualize_double_pendulum(np.pi/2,np.pi/3+1,3)
