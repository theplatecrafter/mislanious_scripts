import numpy as np
import matplotlib.pyplot as plt
from scipy.special import sph_harm, assoc_laguerre
from matplotlib import cm
from matplotlib.widgets import Slider

# Create a 3D figure to visualize the 1s orbital
n, l, m = 1, 0, 0  # Quantum numbers for 1s orbital

# Create a grid in spherical coordinates
r = np.linspace(0, 15, 100)  # Radial distance
theta = np.linspace(0, np.pi, 100)  # Polar angle
phi = np.linspace(0, 2*np.pi, 100)  # Azimuthal angle

# Calculate the radial part (R) of the wavefunction
def hydrogen_R(r, n, l):
    # Bohr radius in atomic units
    a0 = 1.0
    # Normalization factor
    norm = np.sqrt((2.0/(n*a0))**3 * np.math.factorial(n-l-1) / (2*n*np.math.factorial(n+l)))
    # Calculate radial part
    rho = 2.0*r/(n*a0)
    L = assoc_laguerre(rho, n-l-1, 2*l+1)
    return norm * np.exp(-rho/2.0) * rho**l * L

# Calculate the angular part (Y) using spherical harmonics
def hydrogen_Y(theta, phi, l, m):
    return sph_harm(m, l, phi, theta)

# Calculate the full wavefunction and probability density
r_mesh, theta_mesh = np.meshgrid(r, theta)
R = hydrogen_R(r_mesh, n, l)
Y = hydrogen_Y(theta_mesh, 0, l, m)  # Using phi=0 for 2D slice
psi = R * Y
probability = np.abs(psi)**2

# Convert to Cartesian coordinates for the plot
x = r_mesh * np.sin(theta_mesh)
y = r_mesh * np.cos(theta_mesh)

# Create the plot
fig, ax = plt.subplots(figsize=(10, 8))
contour = ax.contourf(x, y, probability, 50, cmap='viridis')
plt.colorbar(contour, label='Probability Density')
ax.set_title(f'Hydrogen Atom 1s Orbital (n={n}, l={l}, m={m})\nProbability Density Cross-Section')
ax.set_xlabel('x (atomic units)')
ax.set_ylabel('z (atomic units)')
ax.set_aspect('equal')

plt.tight_layout()
plt.savefig("outputs/hydrogen_1s_orbital.jpg")