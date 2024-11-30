import numpy as np
import pygame
import math

# Parameters for the double pendulum
g = 9.81      # Gravitational constant
dt = 0.01     # Time step for the simulation
L1, L2 = 1.0, 1.0  # Lengths of the pendulums

# Helper function to determine chaos in the double pendulum
def is_chaotic(theta1, theta2):
    # Calculate the positions of the first and second nodes
    x1 = L1 * math.sin(theta1)
    y1 = -L1 * math.cos(theta1)
    x2 = x1 + L2 * math.sin(theta2)
    y2 = y1 - L2 * math.cos(theta2)
    
    # Debugging: Print positions of nodes for specific pixels
    if np.random.rand() < 0.0001:  # Print for a random pixel to avoid overwhelming output
        print(f"Node 1 position: (x1={x1}, y1={y1}), Node 2 position: (x2={x2}, y2={y2})")
    
    # Check if either node is above the y-coordinate of the pivot point (y = 0)
    return y1 > 0 or y2 > 0

# Draw a button with text
def draw_button(screen, rect, color, text, font, text_color=(0, 0, 0)):
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# Function to initialize and run the double pendulum chaos simulation
def double_pendulum_chaos_sim(screen_size, theta1_range, theta2_range):
    width, height = screen_size
    pygame.init()
    screen = pygame.display.set_mode((width, height + 50))
    pygame.display.set_caption("Double Pendulum Chaos Simulation")

    # Set up font and buttons
    font = pygame.font.Font(None, 30)
    button_pause = pygame.Rect(10, height + 10, 80, 30)
    button_step = pygame.Rect(100, height + 10, 80, 30)
    button_max_speed = pygame.Rect(190, height + 10, 120, 30)

    chaotic_grid = np.zeros((width, height), dtype=bool)
    theta1_grid = np.linspace(theta1_range[0], theta1_range[1], width)
    theta2_grid = np.linspace(theta2_range[0], theta2_range[1], height)
    theta1_dot_grid = np.zeros((width, height))
    theta2_dot_grid = np.zeros((width, height))

    paused = False
    max_speed = False

    def update_simulation():
        # Perform simulation step
        for i in range(width):
            for j in range(height):
                if not chaotic_grid[i, j]:  # Only simulate if not already chaotic
                    theta1 = theta1_grid[i]
                    theta2 = theta2_grid[j]
                    theta1_dot = theta1_dot_grid[i, j]
                    theta2_dot = theta2_dot_grid[i, j]
                    
                    delta_theta = theta2 - theta1
                    denominator1 = (2 - math.cos(2 * delta_theta))
                    denominator2 = (2 - math.cos(delta_theta)**2)
                    
                    theta1_ddot = (-g * (2 * math.sin(theta1) - math.sin(delta_theta) * math.cos(delta_theta)) - 
                                   math.sin(delta_theta) * theta2_dot**2 * math.sin(delta_theta)) / denominator1
                    theta2_ddot = (2 * math.sin(delta_theta) * (theta1_dot**2 * math.sin(delta_theta) +
                                   g * math.cos(theta2))) / denominator2
                    
                    theta1_dot += theta1_ddot * dt
                    theta2_dot += theta2_ddot * dt
                    theta1 += theta1_dot * dt
                    theta2 += theta2_dot * dt
                    
                    # Debugging: Print the angles and their derivatives for a few pixels
                    if (i, j) == (0, 0) or (i, j) == (width // 2, height // 2):  # Check edge and center pixels
                        print(f"Pixel ({i}, {j}): theta1={theta1}, theta2={theta2}, theta1_dot={theta1_dot}, theta2_dot={theta2_dot}")

                    theta1_grid[i] = theta1
                    theta2_grid[j] = theta2
                    theta1_dot_grid[i, j] = theta1_dot
                    theta2_dot_grid[i, j] = theta2_dot
                    
                    # Check if pendulum has gone chaotic
                    if is_chaotic(theta1, theta2):
                        chaotic_grid[i, j] = True

    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear the screen
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_pause.collidepoint(event.pos):
                    paused = not paused
                elif button_step.collidepoint(event.pos) and paused:
                    update_simulation()  # Step once if paused
                elif button_max_speed.collidepoint(event.pos):
                    max_speed = not max_speed

        # Draw buttons
        draw_button(screen, button_pause, (200, 200, 200), "Pause" if not paused else "Unpause", font)
        draw_button(screen, button_step, (200, 200, 200), "Step", font)
        draw_button(screen, button_max_speed, (200, 200, 200), "Max Speed" if not max_speed else "Normal Speed", font)

        # Simulation logic
        if not paused or (paused and max_speed):
            update_simulation()

        # Draw chaotic grid
        for i in range(width):
            for j in range(height):
                color = (255, 255, 255) if chaotic_grid[i, j] else (0, 0, 0)
                screen.set_at((i, j), color)

        pygame.display.flip()

        # Control speed if not in max speed mode
        if not max_speed:
            pygame.time.delay(30)
    
    pygame.quit()

# Example usage
screen_size = (200, 200)
theta1_range = [math.pi / 4, 3 * math.pi / 4]
theta2_range = [math.pi / 4, 3 * math.pi / 4]
double_pendulum_chaos_sim(screen_size, theta1_range, theta2_range)
