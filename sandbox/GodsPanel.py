import pygame
import time
import colorsys
import copy

# Initialize Pygame
pygame.init()

# Constants
FPS = 30  # Reduced FPS for Pygame
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FONT_SIZE = 20
CHANGE_CALC_THRESHOLD = 0.0001
SLIDER_BORDER_RADIUS = 10

# Set up the display
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Fullscreen
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()  # Get screen size
pygame.display.set_caption("Slider Simulation")
font = pygame.font.Font(None, FONT_SIZE)


# --- Data and State ---
slider_data = {
    "A": {
        "A1": {"init": 70, "connections": {"B2": 0.5, "A2": -0.2}},
        "A2": {"init": 60, "connections": {"A3": -0.1}},
        "A3": {"init": 50, "connections": {"B1": 0.2}}
    },
    "B": {
        "B1": {"init": 40, "connections": {"B2": 0.2, "A3": 0.6}},
        "B2": {"init": 30, "connections": {"A1": -0.3}},
    }
}

slider_state = {}


def init():
    """Initializes the slider_state dictionary."""
    global slider_state
    slider_state = {}
    for category in slider_data:
        for slider in slider_data[category]:
            slider_state[slider] = {
                "value": slider_data[category][slider]["init"],
                "change": 0,
                "connections": slider_data[category][slider]["connections"]
            }



def tick():
    """Calculates the next state of the sliders."""
    global slider_state
    next_slider_state = copy.deepcopy(slider_state)

    for slider in slider_state:
        if slider_state[slider]["change"] != 0:
            change = slider_state[slider]["change"]
            for connection, weight in slider_state[slider]["connections"].items():
                if connection in next_slider_state:
                    next_slider_state[connection]["value"] += change * weight
                    next_slider_state[connection]["change"] += change * weight
                else:
                    print(f"Warning: Connection '{connection}' not found for slider '{slider}'")
            next_slider_state[slider]["change"] = 0
        if abs(next_slider_state[slider]["change"]) < CHANGE_CALC_THRESHOLD:
            next_slider_state[slider]["change"] = 0
        if next_slider_state[slider]["value"] < 0:
            next_slider_state[slider]["value"] = 0
        if next_slider_state[slider]["value"] > 100:
            next_slider_state[slider]["value"] = 100

    slider_state = copy.deepcopy(next_slider_state)



# --- Pygame UI functions ---
def draw_slider(screen, x, y, width, height, value, slider_name, change):
    """
    Draws a slider on the screen.

    Args:
        screen: The Pygame screen to draw on.
        x: The x-coordinate of the slider.
        y: The y-coordinate of the slider.
        width: The width of the slider.
        height: The height of the slider.
        value: The current value of the slider.
        slider_name: The name of the slider.
        change: The current change value of the slider.
    """
    # Background of the slider
    pygame.draw.rect(screen, WHITE, (x, y, width, height), 2, border_radius=SLIDER_BORDER_RADIUS)

    # Calculate the fill based on the value
    fill_width = (value / 100) * width if width > 0 else 0

    # Ensure fill_width is within the bounds
    fill_width = max(0, min(fill_width, width))

    fill_color = tuple([i * 255 for i in colorsys.hsv_to_rgb((x / SCREEN_WIDTH) % 1, 1, 1)])
    pygame.draw.rect(screen, fill_color, (x, y, fill_width, height), border_radius=SLIDER_BORDER_RADIUS)

    # Slider name label
    text_surface = font.render(f"{slider_name}: {value:.2f}", True, WHITE)
    screen.blit(text_surface, (x, y + height + 5))

    # Display the change value
    change_text_surface = font.render(f"Change: {change:.2f}", True, DARK_GRAY)
    screen.blit(change_text_surface, (x, y - 20))



def create_slider_rects(slider_data, slider_width, slider_height, x_spacing, y_spacing, x_start, y_start):
    """
    Creates rectangles for each slider, organized by category.

    Args:
        slider_data: The dictionary containing the slider data, organized by category.
        slider_width: The width of each slider.
        slider_height: The height of each slider.
        x_spacing: The horizontal spacing between columns.
        y_spacing: The vertical spacing between sliders in the same column.
        x_start: The starting x-coordinate for the first column.
        y_start: The starting y-coordinate for the first slider.

    Returns:
        A dictionary where keys are slider names (e.g., "A1", "B2") and values are
        pygame.Rect objects representing the slider's position and size.
    """
    slider_rects = {}
    x = x_start
    y = y_start
    for category_name, sliders in slider_data.items():
        for slider_name in sliders:
            slider_rects[slider_name] = pygame.Rect(x, y, slider_width, slider_height)
            y += slider_height + y_spacing
        x += slider_width + x_spacing
        y = y_start  # Reset y for the next column
    return slider_rects



def handle_slider_drag(slider_rects, mouse_pos, slider_state, is_dragging, dragged_slider, initial_values):
    """
    Handles mouse interaction with sliders.

    Args:
        slider_rects: A dictionary of slider names and their corresponding pygame.Rect objects.
        mouse_pos: The current position of the mouse.
        slider_state: The dictionary containing the state of the sliders.
        is_dragging: A boolean indicating if a slider is currently being dragged.
        dragged_slider: The name of the slider that is currently being dragged (or None).
        initial_values:  Dictionary to store initial values before dragging.

    Returns:
        A tuple containing:
        - The updated is_dragging state.
        - The name of the dragged slider.
        - The updated initial_values dictionary.
    """
    if not is_dragging:
        for slider_name, rect in slider_rects.items():
            if rect.collidepoint(mouse_pos):
                is_dragging = True
                dragged_slider = slider_name
                initial_values[dragged_slider] = slider_state[dragged_slider]["value"]
                break
    elif is_dragging and dragged_slider:
        rect = slider_rects[dragged_slider]
        new_value = ((mouse_pos[0] - rect.x) / rect.width) * 100
        new_value = max(0, min(new_value, 100))
        slider_state[dragged_slider]["value"] = new_value
    return is_dragging, dragged_slider, initial_values



def run_simulation():
    """
    Runs the main Pygame simulation loop.
    """
    global slider_state
    init()
    running = True
    clock = pygame.time.Clock()
    slider_width = 200
    slider_height = 20
    x_start = 50
    y_start = 50
    x_spacing = 250
    y_spacing = 50

    slider_rects = create_slider_rects(slider_data, slider_width, slider_height, x_spacing, y_spacing, x_start, y_start)
    is_dragging = False
    dragged_slider = None
    initial_values = {}

    # Calculate the x positions for the category labels
    category_x_positions = {}
    x = x_start
    for category_name in slider_data:
        category_x_positions[category_name] = x
        x += slider_width + x_spacing

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:  # Check for key press
                if event.key == pygame.K_ESCAPE:  # If it's the ESC key
                    running = False  # set running to false, which will break the loop and quit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                is_dragging, dragged_slider, initial_values = handle_slider_drag(slider_rects, event.pos, slider_state,
                                                                            is_dragging, dragged_slider, initial_values)
            elif event.type == pygame.MOUSEBUTTONUP:
                if is_dragging and dragged_slider:
                    slider_state[dragged_slider]["change"] = slider_state[dragged_slider]["value"] - \
                                                            initial_values[dragged_slider]
                is_dragging = False
                dragged_slider = None
            elif event.type == pygame.MOUSEMOTION:
                if is_dragging and dragged_slider:
                    is_dragging, dragged_slider, initial_values = handle_slider_drag(slider_rects, event.pos, slider_state,
                                                                                is_dragging, dragged_slider,
                                                                                initial_values)

        if not is_dragging:
            tick()

        screen.fill(BLACK)

        # Draw category labels
        for category_name, x_pos in category_x_positions.items():
            category_label_surface = font.render(category_name, True, WHITE)
            #  category label 20 pixels above the first slider.
            screen.blit(category_label_surface, (x_pos, y_start - 40))

        for slider_name, rect in slider_rects.items():
            category = slider_name[0]
            draw_slider(screen, rect.x, rect.y, rect.width, rect.height,
                        slider_state[slider_name]["value"], slider_name, slider_state[slider_name]["change"])
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()



if __name__ == "__main__":
    run_simulation()
