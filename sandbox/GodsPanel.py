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
FONT_SIZE = 20
CHANGE_CALC_THRESHOLD = 0.0001
SLIDER_BORDER_RADIUS = 10
SCROLL_SPEED = 20  # Added scroll speed
DAMPING_FACTOR = 0.5

# Set up the display
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Fullscreen
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()  # Get screen size
pygame.display.set_caption("Slider Simulation")
font = pygame.font.Font(None, FONT_SIZE)


# --- Data and State ---
slider_data = {
    "Environment & Energy": {
        "Fossil Fuel Consumption": {"init": 70, "connections": {"Carbon Emissions": 0.8, "Air Quality": -0.5, "Global Energy Prices": 0.6}},
        "Carbon Emissions": {"init": 80, "connections": {"Global Temperature": 0.9, "Ocean Acidification": 0.7, "Air Quality": -0.8}},
        "Air Quality": {"init": 60, "connections": {"Healthcare Access": -0.3, "Fossil Fuel Consumption": 0.5, "Carbon Emissions": -0.8}},
        "Global Temperature": {"init": 90, "connections": {"Sea Level Rise": 0.95, "Species Biodiversity": -0.6, "Sustainable Agriculture": -0.2}},
        "Sea Level Rise": {"init": 70, "connections": {"Economic Growth": -0.1}},
        "Investment in Renewable Energy": {"init": 40, "connections": {"Fossil Fuel Consumption": -0.7, "Renewable Energy Production": 0.9, "Economic Growth": 0.2}},
        "Deforestation Rate": {"init": 60, "connections": {"Species Biodiversity": -0.8, "Carbon Emissions": 0.4, "Agricultural Land Use": 0.6}},
        "Species Biodiversity": {"init": 30, "connections": {"Food Security": -0.4, "Deforestation Rate": -0.8, "Ocean Acidification": -0.5}},
        "Ocean Acidification": {"init": 75, "connections": {"Species Biodiversity": -0.5, "Food Security": -0.3}},
        "Methane Emissions": {"init": 65, "connections": {"Global Temperature": 0.3, "Air Quality": -0.2}},
        "Plastic Pollution": {"init": 85, "connections": {"Ocean Acidification": 0.6, "Species Biodiversity": -0.4}},
        "Water Usage": {"init": 55, "connections": {"Agricultural Land Use": 0.7, "Food Security": -0.2}},
        "Renewable Energy Production": {"init": 35, "connections": {"Fossil Fuel Consumption": -0.6, "Energy Efficiency": 0.5}},
        "Energy Efficiency": {"init": 45, "connections": {"Fossil Fuel Consumption": -0.4, "Industrial Output": 0.3}},
        "Sustainable Agriculture": {"init": 40, "connections": {"Food Security": 0.7, "Deforestation Rate": -0.3, "Water Usage": -0.2}},
    },
    "Economy": {
        "Economic Growth": {"init": 60, "connections": {"Unemployment Rate": -0.5, "Industrial Output": 0.7, "Inflation Rate": 0.3}},
        "Unemployment Rate": {"init": 40, "connections": {"Economic Growth": -0.6, "Social Stability": -0.2, "Income Inequality": 0.4}},
        "Global Energy Prices": {"init": 70, "connections": {"Inflation Rate": 0.6, "Industrial Output": -0.4, "Fossil Fuel Consumption": 0.8}},
        "Income Inequality": {"init": 65, "connections": {"Social Stability": -0.7, "Economic Growth": -0.2, "Crime Rate": 0.5}},
        "Industrial Output": {"init": 55, "connections": {"Economic Growth": 0.7, "Energy Efficiency": 0.3, "Resource Scarcity": -0.2}},
        "Resource Scarcity": {"init": 80, "connections": {"Global Energy Prices": 0.4, "Industrial Output": -0.3, "Food Security": -0.1}},
        "Trade Openness": {"init": 50, "connections": {"Economic Growth": 0.3, "Global Energy Prices": 0.2}},
        "Inflation Rate": {"init": 50, "connections": {"Interest Rates": 0.7, "Economic Growth": -0.2, "Unemployment Rate": 0.3}},
        "Interest Rates": {"init": 40, "connections": {"Inflation Rate": 0.6, "Stock Market Volatility": 0.5, "Foreign Direct Investment": -0.3}},
        "Stock Market Volatility": {"init": 60, "connections": {"Foreign Direct Investment": -0.7, "Interest Rates": 0.5}},
        "Foreign Direct Investment": {"init": 50, "connections": {"Economic Growth": 0.4, "Tech Innovation Rate": 0.3}},
    },
    "Society": {
        "Population Growth": {"init": 60, "connections": {"Urbanization Rate": 0.5, "Resource Scarcity": 0.3, "Healthcare Access": -0.2}},
        "Urbanization Rate": {"init": 55, "connections": {"Air Quality": -0.4, "Social Stability": -0.2}},
        "Healthcare Access": {"init": 40, "connections": {"Life Expectancy": 0.8, "Social Stability": 0.3, "Public Trust in Institutions": 0.2}},
        "Education Access": {"init": 50, "connections": {"Digital Literacy": 0.6, "Economic Growth": 0.4, "Civic Participation": 0.3}},
        "Social Stability": {"init": 50, "connections": {"Crime Rate": -0.6, "Public Trust in Institutions": 0.7, "Economic Growth": 0.2}},
        "Migration Rate": {"init": 45, "connections": {"Cultural Diversity": 0.8, "Social Stability": -0.3, "Economic Growth": 0.1}},
        "Crime Rate": {"init": 30, "connections": {"Social Stability": -0.6, "Income Inequality": 0.5}},
        "Civic Participation": {"init": 40, "connections": {"Social Stability": 0.4, "Government Transparency": 0.5, "Public Trust in Institutions": 0.6}},
        "Life Expectancy": {"init": 75, "connections": {"Healthcare Access": 0.8, "Air Quality": 0.4, "Obesity Rate": -0.3}},
        "Public Trust in Institutions": {"init": 35, "connections": {"Government Transparency": 0.7, "Social Stability": 0.5, "Civic Participation": 0.4}},
        "Cultural Diversity": {"init": 60, "connections": {"Social Connectedness": 0.4, "Social Stability": 0.2}},
    },
    "Politics & Governance": {
        "Military Spending": {"init": 60, "connections": {"International Cooperation": -0.4, "Economic Growth": -0.2, "Social Stability": -0.3}},
        "Government Transparency": {"init": 40, "connections": {"Corruption Perception": -0.9, "Public Trust in Institutions": 0.7, "International Cooperation": 0.2}},
        "Democratic Index": {"init": 50, "connections": {"Freedom of Press": 0.8, "Political Stability": 0.6, "Civic Participation": 0.5}},
        "Corruption Perception": {"init": 70, "connections": {"Government Transparency": -0.9, "Foreign Direct Investment": -0.5, "Public Trust in Institutions": -0.8}},
        "International Cooperation": {"init": 50, "connections": {"Global Temperature": -0.2, "Economic Growth": 0.3, "Political Stability": 0.4}},
        "Freedom of Press": {"init": 60, "connections": {"Democratic Index": 0.8, "Public Trust in Institutions": 0.3}},
        "Political Stability": {"init": 65, "connections": {"Foreign Direct Investment": 0.2, "Social Stability": 0.7, "Economic Growth": 0.1}},
        "Rule of Law": {"init": 55, "connections": {"Foreign Direct Investment": 0.4, "Economic Growth": 0.3, "Social Stability": 0.2}},
        "Regulatory Quality": {"init": 50, "connections": {"Industrial Output": 0.4, "Economic Growth": 0.2, "Innovation Rate": 0.3}},
        "Voice and Accountability": {"init": 45, "connections": {"Civic Participation": 0.6, "Social Stability": 0.4, "Government Transparency": 0.5}},
    },
    "Technology & Innovation": {
        "Tech Innovation Rate": {"init": 50, "connections": {"Economic Growth": 0.5, "Automation Penetration": 0.6, "Renewable Energy Tech": 0.4}},
        "AI Development": {"init": 40, "connections": {"Automation Penetration": 0.7, "Economic Growth": 0.3, "Cybersecurity Investment": 0.5}},
        "Cybersecurity Investment": {"init": 60, "connections": {"Digital Literacy": 0.4, "AI Development": 0.5, "Public Trust in Institutions": 0.3}},
        "Automation Penetration": {"init": 55, "connections": {"Unemployment Rate": 0.6, "Economic Growth": 0.4, "Tech Innovation Rate": 0.6}},
        "Space Exploration Funding": {"init": 20, "connections": {"Tech Innovation Rate": 0.2}},
        "Digital Literacy": {"init": 50, "connections": {"Education Access": 0.6, "Internet Access": 0.8, "Tech Innovation Rate": 0.3}},
        "Internet Access": {"init": 70, "connections": {"Digital Literacy": 0.8, "Economic Growth": 0.2, "Social Connectedness": 0.4}},
        "Renewable Energy Tech": {"init": 45, "connections": {"Investment in Renewable Energy": 0.9, "Fossil Fuel Consumption": -0.5, "Energy Efficiency": 0.7}},
        "Biotechnology Development": {"init": 30, "connections": {"Healthcare Access": 0.6, "Agricultural Productivity": 0.5, "Ethical Considerations": -0.2}},
    },
    "Health & Epidemics": {
        "Global Pandemic Risk": {"init": 70, "connections": {"International Cooperation": -0.5, "Healthcare Access": -0.2, "Global Travel": 0.6}},
        "Vaccination Rate": {"init": 60, "connections": {"Global Pandemic Risk": -0.8, "Life Expectancy": 0.5, "Public Health Spending": 0.7}},
        "Antibiotic Resistance": {"init": 65, "connections": {"Healthcare Access": -0.4, "Global Pandemic Risk": 0.3, "Public Health Spending": 0.2}},
        "Obesity Rate": {"init": 50, "connections": {"Healthcare Access": -0.3, "Life Expectancy": -0.4, "Food Security": -0.2}},
        "Mental Health Index": {"init": 40, "connections": {"Healthcare Access": 0.4, "Social Stability": 0.3, "Work-Life Balance": 0.6}},
        "Access to Clean Water": {"init": 60, "connections": {"Healthcare Access": 0.7, "Food Security": 0.4, "Public Health Spending": 0.3}},
    },
    "Agriculture & Food": {
        "Food Security": {"init": 50, "connections": {"Population Growth": -0.3, "Sustainable Agriculture": 0.6, "Economic Growth": 0.2}},
        "Crop Yield": {"init": 60, "connections": {"Sustainable Farming Practices": 0.7, "Agricultural Land Use": -0.2, "Food Security": 0.5}},
        "Agricultural Land Use": {"init": 40, "connections": {"Deforestation Rate": 0.5, "Water Usage": 0.7, "Species Biodiversity": -0.3}},
        "Meat Consumption": {"init": 70, "connections": {"Carbon Emissions": 0.4, "Agricultural Land Use": 0.3, "Healthcare Access": -0.2}},
        "Sustainable Farming Practices": {"init": 30, "connections": {"Crop Yield": 0.7, "Agricultural Land Use": -0.4, "Food Security": 0.6}},
        "Food Waste": {"init": 40, "connections": {"Food Security": -0.2, "Agricultural Land Use": 0.1, "Economic Growth": -0.1}},
    },
    "Culture & Wellbeing": {
        "Mental Health Index": {"init": 40, "connections": {"Social Connectedness": 0.7, "Work-Life Balance": 0.6, "Healthcare Access": 0.4}},
        "Work-Life Balance": {"init": 50, "connections": {"Economic Growth": -0.3, "Mental Health Index": 0.6, "Leisure Time": 0.8}},
        "Cultural Diversity": {"init": 60, "connections": {"Social Connectedness": 0.5, "Social Stability": 0.2, "Civic Participation": 0.3}},
        "Social Connectedness": {"init": 55, "connections": {"Mental Health Index": 0.7, "Cultural Diversity": 0.5, "Civic Participation": 0.4}},
        "Leisure Time": {"init": 50, "connections": {"Work-Life Balance": 0.8, "Mental Health Index": 0.3, "Economic Growth": 0.1}},
        "Arts and Culture Funding": {"init": 30, "connections": {"Cultural Diversity": 0.4, "Social Connectedness": 0.2, "Civic Participation": 0.3}},
    },
}


slider_state = {}


def init():
    global slider_state
    """Initializes the slider_state dictionary."""
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
            change = slider_state[slider]["change"]*DAMPING_FACTOR
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
def draw_slider(screen, x, y, width, height, value, slider_name, change, scroll_offset):
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

    fill_color = tuple([i * 255 for i in colorsys.hsv_to_rgb(((x+scroll_offset[0]) / SCREEN_WIDTH) % 1, 1, 1)])
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



def handle_slider_drag(slider_rects, mouse_pos, slider_state, is_dragging, dragged_slider, initial_values, scroll_offset):
    """
    Handles mouse interaction with sliders.

    Args:
        slider_rects: A dictionary of slider names and their corresponding pygame.Rect objects.
        mouse_pos: The current position of the mouse.
        slider_state: The dictionary containing the state of the sliders.
        is_dragging: A boolean indicating if a slider is currently being dragged.
        dragged_slider: The name of the slider that is currently being dragged (or None).
        initial_values:  Dictionary to store initial values before dragging.
        scroll_offset: The current scroll offset.

    Returns:
        A tuple containing:
        - The updated is_dragging state.
        - The name of the dragged slider.
        - The updated initial_values dictionary.
    """
    if not is_dragging:
        for slider_name, rect in slider_rects.items():
            # Adjust the rect position for scrolling
            adjusted_rect = rect.move(-scroll_offset[0], -scroll_offset[1])
            if adjusted_rect.collidepoint(mouse_pos):
                is_dragging = True
                dragged_slider = slider_name
                initial_values[dragged_slider] = slider_state[dragged_slider]["value"]
                break
    elif is_dragging and dragged_slider:
        rect = slider_rects[dragged_slider]
        # Adjust mouse position for scrolling
        adjusted_mouse_pos = (mouse_pos[0] + scroll_offset[0], mouse_pos[1] + scroll_offset[1])
        new_value = ((adjusted_mouse_pos[0] - rect.x) / rect.width) * 100
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
    scroll_offset = [0, 0]  # [x, y] offset
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
                if event.key in keys_down:
                    keys_down[event.key] = True
            elif event.type == pygame.KEYUP:
                if event.key in keys_down:
                    keys_down[event.key] = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                is_dragging, dragged_slider, initial_values = handle_slider_drag(slider_rects, event.pos, slider_state,
                                                                                is_dragging, dragged_slider, initial_values, scroll_offset)
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
                                                                                    initial_values, scroll_offset)

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

        # Draw category labels
        for category_name, x_pos in category_x_positions.items():
            category_label_surface = font.render(category_name, True, WHITE)
            #  category label, adjusted for scroll
            screen.blit(category_label_surface, (x_pos - scroll_offset[0], y_start - 40 - scroll_offset[1]))

        for slider_name, rect in slider_rects.items():
            category = slider_name[0]
            # Adjust slider position for scroll offset.
            adjusted_rect = rect.move(-scroll_offset[0], -scroll_offset[1])
            draw_slider(screen, adjusted_rect.x, adjusted_rect.y, adjusted_rect.width, adjusted_rect.height,
                        slider_state[slider_name]["value"], slider_name, slider_state[slider_name]["change"], scroll_offset)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()



if __name__ == "__main__":
    run_simulation()
