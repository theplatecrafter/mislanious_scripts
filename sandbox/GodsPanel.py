import pygame
import time
import colorsys
import copy
import json
import os

def GodsPanel(input_file=None):
    # Initialize Pygame
    pygame.init()

    # Constants
    FPS = 30
    WHITE = (255, 255, 255)
    GRAY = (200, 200, 200)
    DARK_GRAY = (100, 100, 100)
    BLACK = (0, 0, 0)
    FONT_SIZE = 20
    CHANGE_CALC_THRESHOLD = 0.0001
    SLIDER_BORDER_RADIUS = 10
    SCROLL_SPEED = 20
    DAMPING_FACTOR = 0.5
    BUTTON_WIDTH = 100
    BUTTON_HEIGHT = 30
    BUTTON_SPACING = 10
    BUTTON_COLOR = GRAY
    BUTTON_TEXT_COLOR = BLACK
    BUTTON_FONT_SIZE = 16
    INFO_TEXT_COLOR = WHITE
    INFO_FONT_SIZE = 14
    INFO_DISPLAY_TIME = 5  # Time to display info text in seconds

    # Set up the display
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()
    pygame.display.set_caption("Slider Simulation")
    font = pygame.font.Font(None, FONT_SIZE)
    button_font = pygame.font.Font(None, BUTTON_FONT_SIZE)
    info_font = pygame.font.Font(None, INFO_FONT_SIZE)

    # UI variables
    slider_width = 200
    slider_height = 20
    x_start = 50
    y_start = 50
    x_spacing = 250
    y_spacing = 50
    
    # Global state variables - all declared here to fix nonlocal references
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
    slider_rects = {}  # Initialize here to avoid nonlocal binding error
    category_x_positions = {}  # Initialize here to avoid nonlocal binding error
    info_text = ""
    info_start_time = 0

    def init():
        """Initializes the slider_state dictionary."""
        nonlocal slider_state
        slider_state = {}
        for category in slider_data:
            for slider in slider_data[category]:
                slider_state[slider] = {
                    "value": slider_data[category][slider]["init"],
                    "change": 0,
                    "connections": slider_data[category][slider]["connections"]
                }
        return slider_state

    def tick():
        """Calculates the next state of the sliders."""
        nonlocal slider_state
        next_slider_state = copy.deepcopy(slider_state)

        for slider in slider_state:
            if slider_state[slider]["change"] != 0:
                change = slider_state[slider]["change"] * DAMPING_FACTOR
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

        slider_state = next_slider_state

    # --- Pygame UI functions ---
    def draw_slider(screen, x, y, width, height, value, slider_name, change, scroll_offset):
        """
        Draws a slider on the screen.
        """
        # Background of the slider
        pygame.draw.rect(screen, WHITE, (x, y, width, height), 2, border_radius=SLIDER_BORDER_RADIUS)

        # Calculate the fill based on the value
        fill_width = (value / 100) * width if width > 0 else 0
        fill_width = max(0, min(fill_width, width))
        fill_color = tuple([i * 255 for i in colorsys.hsv_to_rgb(((x + scroll_offset[0]) / SCREEN_WIDTH) % 1, 1, 1)])
        pygame.draw.rect(screen, fill_color, (x, y, fill_width, height), border_radius=SLIDER_BORDER_RADIUS)

        # Slider name label
        text_surface = font.render(f"{slider_name}: {value:.2f}", True, WHITE)
        screen.blit(text_surface, (x, y + height + 5))

        # Display the change value
        change_text_surface = font.render(f"Change: {change:.2f}", True, DARK_GRAY)
        screen.blit(change_text_surface, (x, y - 20))

    def create_slider_rects(data, width, height, x_spacing, y_spacing, x_start, y_start):
        """
        Creates rectangles for each slider, organized by category.
        """
        rects = {}
        x = x_start
        y = y_start
        for category_name, sliders in data.items():
            for slider_name in sliders:
                rects[slider_name] = pygame.Rect(x, y, width, height)
                y += height + y_spacing
            x += width + x_spacing
            y = y_start
        return rects

    def create_category_positions(data, width, spacing, start_x):
        """
        Create a dictionary of x positions for category labels
        """
        positions = {}
        x = start_x
        for category_name in data:
            positions[category_name] = x
            x += width + spacing
        return positions

    def handle_slider_drag(slider_rects, mouse_pos, state, is_dragging, dragged_slider, initial_values, scroll_offset):
        """
        Handles mouse interaction with sliders.
        """
        if not is_dragging:
            for slider_name, rect in slider_rects.items():
                adjusted_rect = rect.move(-scroll_offset[0], -scroll_offset[1])
                if adjusted_rect.collidepoint(mouse_pos):
                    is_dragging = True
                    dragged_slider = slider_name
                    initial_values[dragged_slider] = state[dragged_slider]["value"]
                    break
        elif is_dragging and dragged_slider:
            rect = slider_rects[dragged_slider]
            adjusted_mouse_pos = (mouse_pos[0] + scroll_offset[0], mouse_pos[1] + scroll_offset[1])
            new_value = ((adjusted_mouse_pos[0] - rect.x) / rect.width) * 100
            new_value = max(0, min(new_value, 100))
            state[dragged_slider]["value"] = new_value
        return is_dragging, dragged_slider, initial_values

    def draw_button(screen, rect, text):
        """Draws a button on the screen."""
        pygame.draw.rect(screen, BUTTON_COLOR, rect, border_radius=SLIDER_BORDER_RADIUS)
        text_surface = button_font.render(text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    def display_info_text(screen, text):
        """Displays info text at the bottom of the screen."""
        text_surface = info_font.render(text, True, INFO_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20))
        screen.blit(text_surface, text_rect)

    def handle_button_click(button_rects, mouse_pos):
        """Handles button clicks."""
        for button_name, rect in button_rects.items():
            if rect.collidepoint(mouse_pos):
                return button_name
        return None

    def export_slider_data(filename="slider_data.json"):
        """Exports the current slider data to a JSON file."""
        nonlocal info_text, info_start_time
        try:
            with open(filename, "w") as f:
                json.dump(slider_data, f, indent=4)
            info_text = f"Exported data to {filename}"
            info_start_time = time.time()
            print(info_text)  # Keep the print for debugging
        except Exception as e:
            info_text = f"Error exporting data: {e}"
            info_start_time = time.time()
            print(info_text)

    def import_slider_data(filename="slider_data.json"):
        """Imports slider data from a JSON file."""
        nonlocal slider_data, slider_state, info_text, info_start_time, slider_rects, category_x_positions

        try:
            if not os.path.exists(filename):
                info_text = f"File not found: {filename}. Using default data."
                info_start_time = time.time()
                print(info_text)
                return

            with open(filename, "r") as f:
                slider_data = json.load(f)

            # Re-initialize the slider state
            init()
            
            # Recreate the UI based on the imported data
            slider_rects = create_slider_rects(
                slider_data, slider_width, slider_height, 
                x_spacing, y_spacing, x_start, y_start
            )
            
            # Calculate the x positions for the category labels
            category_x_positions = create_category_positions(
                slider_data, slider_width, x_spacing, x_start
            )

            info_text = f"Imported data from {filename}"
            info_start_time = time.time()
            print(info_text)
        except Exception as e:
            info_text = f"Error importing data: {e}"
            info_start_time = time.time()
            print(info_text)

    def reset_slider_data():
        """Resets the slider values to their initial values."""
        nonlocal slider_state, info_text, info_start_time
        init()  # Re-initialize slider_state to reset to initial values.
        info_text = "Reset slider data to initial values"
        info_start_time = time.time()
        print(info_text)
    
    def run_simulation():
        """
        Runs the main Pygame simulation loop.
        """
        nonlocal slider_state, info_text, info_start_time, slider_rects, category_x_positions

        # Initialize slider state
        slider_state = init()

        # Initialize UI components
        slider_rects = create_slider_rects(
            slider_data, slider_width, slider_height, 
            x_spacing, y_spacing, x_start, y_start
        )
        
        # Calculate the x positions for the category labels
        category_x_positions = create_category_positions(
            slider_data, slider_width, x_spacing, x_start
        )

        # Main loop variables
        running = True
        clock = pygame.time.Clock()
        is_dragging = False
        dragged_slider = None
        initial_values = {}
        scroll_offset = [0, -60]
        keys_down = {
            pygame.K_w: False,
            pygame.K_a: False,
            pygame.K_s: False,
            pygame.K_d: False,
            pygame.K_UP: False,
            pygame.K_LEFT: False,
            pygame.K_DOWN: False,
            pygame.K_RIGHT: False,
        }

        # Calculate button positions
        button_x = SCREEN_WIDTH / 2 - (3 * BUTTON_WIDTH + 2 * BUTTON_SPACING) / 2
        button_y = 20
        export_button_rect = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        import_button_rect = pygame.Rect(button_x + BUTTON_WIDTH + BUTTON_SPACING, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        reset_button_rect = pygame.Rect(button_x + 2 * (BUTTON_WIDTH + BUTTON_SPACING), button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_rects = {
            "export": export_button_rect,
            "import": import_button_rect,
            "reset": reset_button_rect,
        }

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key in keys_down:
                        keys_down[event.key] = True
                elif event.type == pygame.KEYUP:
                    if event.key in keys_down:
                        keys_down[event.key] = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_button = handle_button_click(button_rects, event.pos)
                    if clicked_button == "export":
                        export_slider_data()  # Use the default filename
                    elif clicked_button == "import":
                        import_slider_data()  # Use the default filename
                    elif clicked_button == "reset":
                        reset_slider_data()
                    else:  # Only handle slider dragging if no button was clicked
                        is_dragging, dragged_slider, initial_values = handle_slider_drag(
                            slider_rects, event.pos, slider_state, is_dragging, 
                            dragged_slider, initial_values, scroll_offset
                        )
                elif event.type == pygame.MOUSEBUTTONUP:
                    if is_dragging and dragged_slider:
                        slider_state[dragged_slider]["change"] = slider_state[dragged_slider]["value"] - \
                                                                initial_values[dragged_slider]
                    is_dragging = False
                    dragged_slider = None
                elif event.type == pygame.MOUSEMOTION:
                    if is_dragging and dragged_slider:
                        is_dragging, dragged_slider, initial_values = handle_slider_drag(
                            slider_rects, event.pos, slider_state, is_dragging, 
                            dragged_slider, initial_values, scroll_offset
                        )

            # Handle scrolling with WASD and arrow keys
            if keys_down[pygame.K_w] or keys_down[pygame.K_UP]:
                scroll_offset[1] -= SCROLL_SPEED
            if keys_down[pygame.K_a] or keys_down[pygame.K_LEFT]:
                scroll_offset[0] -= SCROLL_SPEED
            if keys_down[pygame.K_s] or keys_down[pygame.K_DOWN]:
                scroll_offset[1] += SCROLL_SPEED
            if keys_down[pygame.K_d] or keys_down[pygame.K_RIGHT]:
                scroll_offset[0] += SCROLL_SPEED

            if not is_dragging:
                tick()

            screen.fill(BLACK)

            # Draw buttons
            for button_name, rect in button_rects.items():
                draw_button(screen, rect, button_name.capitalize())

            # Draw category labels
            for category_name, x_pos in category_x_positions.items():
                category_label_surface = font.render(category_name, True, WHITE)
                screen.blit(category_label_surface, (x_pos - scroll_offset[0], y_start - 40 - scroll_offset[1]))

            # Draw sliders
            for slider_name, rect in slider_rects.items():
                adjusted_rect = rect.move(-scroll_offset[0], -scroll_offset[1])
                draw_slider(
                    screen, adjusted_rect.x, adjusted_rect.y, adjusted_rect.width, adjusted_rect.height,
                    slider_state[slider_name]["value"], slider_name, slider_state[slider_name]["change"], scroll_offset
                )

            # Display info text
            if info_text and time.time() - info_start_time < INFO_DISPLAY_TIME:
                display_info_text(screen, info_text)

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()

    # Load input file if provided
    if input_file and os.path.exists(input_file):
        try:
            with open(input_file, 'r') as f:
                loaded_data = json.load(f)
                slider_data = loaded_data  # Update the slider_data variable
            print(f"Successfully loaded slider data from {input_file}")
        except Exception as e:
            print(f"Error loading input file {input_file}: {e}")
            print("Using default slider data instead.")
    
    # Start the simulation
    run_simulation()




input_file = "slider_data.json"
GodsPanel(input_file)