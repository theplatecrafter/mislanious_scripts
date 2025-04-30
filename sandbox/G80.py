import pygame
import sys
import time

class ConnectedSliderEngine:
    def __init__(self):
        self.sliders = {}
        self.connections = {}
        self.ui_sliders = {}  # Store UISlider instances
        self.animation_duration = 0.2  # in seconds
        self.last_update_time = time.time()

    def add_slider(self, name, initial_value=0):
        """Adds a new slider to the engine."""
        if name in self.sliders:
            return  # Skip adding the slider if it already exists.
        self.sliders[name] = float(initial_value)
        self.connections[name] = {}

    def connect_sliders(self, slider1, slider2, weight=1.0):
        """Connects two sliders, so a change in slider1 affects slider2."""
        if slider1 not in self.sliders or slider2 not in self.sliders: # Changed to self.sliders
            raise ValueError("One or both sliders do not exist.")
        self.connections[slider1][slider2] = float(weight)
        self.connections[slider2][slider1] = float(weight) #make connection both ways

    def set_slider_value(self, name, new_value, propagate=True, damping_factor=0.8, max_iterations=100,
                         change_threshold=0.001, threshold=0.001):
        """Sets the value of a slider and propagates the change."""
        if name not in self.sliders:
            raise ValueError(f"Slider with name '{name}' does not exist.")

        old_value = self.sliders[name]
        new_value = float(new_value)  # Ensure new_value is a float
        new_value = max(0, min(new_value, 100))  # Cap the value between 0 and 100
        self.sliders[name] = new_value
        delta = new_value - old_value

        if propagate and abs(delta) > change_threshold:
            self._propagate_change(name, delta, damping_factor, max_iterations, threshold)

    def get_slider_value(self, name):
        """Returns the current value of a slider."""
        if name not in self.sliders:
            raise ValueError(f"Slider with name '{name}' does not exist.")
        return self.sliders[name]

    def _propagate_change(self, source_slider, change, damping, max_iterations, threshold):
        """Recursively propagates the change through connected sliders."""
        queue = [(source_slider, change)]
        processed = set()
        iteration = 0

        while queue and iteration < max_iterations:
            current_slider, current_change = queue.pop(0)
            if current_slider in processed:
                continue
            processed.add(current_slider)

            for connected_slider, weight in self.connections[current_slider].items():
                impact = current_change * weight * damping
                if abs(impact) > threshold:
                    old_value = self.sliders[connected_slider]
                    new_value = old_value + impact  # Calculate new value
                    new_value = max(0, min(new_value, 100))  # Cap the value between 0 and 100
                    self.sliders[connected_slider] = new_value

                    # Update the UISlider's value directly, if it exists
                    if connected_slider in self.ui_sliders:
                        self.ui_sliders[connected_slider].target_val = new_value #store the target value
                        self.ui_sliders[connected_slider].start_val = self.ui_sliders[connected_slider].val #store the starting value
                        self.ui_sliders[connected_slider].animation_start_time = time.time() #store the start time
                        

                    queue.append((connected_slider, impact))
            iteration += 1

    def __str__(self):
        slider_info = "\n".join(f"  {name}: {value}" for name, value in self.sliders.items())
        connection_info = "\n".join(
            f"  {s1} -> {s2} (weight: {weight})"
            for s1, connections in self.connections.items()
            for s2, weight in connections.items()
        )
        return f"Sliders:\n{slider_info}\nConnections:\n{connection_info}"

    def add_ui_slider(self, ui_slider):
        """Adds a UISlider instance to the engine's dictionary."""
        if ui_slider.name in self.ui_sliders:
            #print(f"UI Slider with name '{ui_slider.name}' already exists. Skipping.")
            return # Skip adding if it exists
        self.ui_sliders[ui_slider.name] = ui_slider

    def update_slider_values(self):
        """Updates slider values for smooth animation."""
        current_time = time.time()
        for slider in self.ui_sliders.values():
            if hasattr(slider, 'animation_start_time'):
                elapsed_time = current_time - slider.animation_start_time
                if elapsed_time >= self.animation_duration:
                    slider.val = slider.target_val
                    del slider.animation_start_time  # Remove animation attributes
                else:
                    # Apply easing function (ease-out quadratic)
                    t = elapsed_time / self.animation_duration
                    ease = 1 - (1 - t) * (1 - t)
                    slider.val = slider.start_val + (slider.target_val - slider.start_val) * ease
                self.sliders[slider.name] = slider.val #update the engine's value



class UISlider:
    def __init__(self, name, x, y, length, min_val, max_val, initial_val,
                 bg_color=(255, 255, 255), fill_color=(255, 0, 0), outline_color=(255, 255, 255),
                 dragging_fill_color=(255, 100, 100), thickness=20):
        self.name = name
        self.x = x
        self.y = y
        self.length = length
        self.min_val = float(min_val)
        self.max_val = float(max_val)
        self.val = float(initial_val)
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.outline_color = outline_color
        self.dragging_fill_color = dragging_fill_color
        self.dragging = False
        self.rect = pygame.Rect(x, y, length, thickness)
        self.handle_radius = 0
        self.outline_width = 2
        self.thickness = thickness
        self.name_font = pygame.font.Font(None, 20)  # Use a font for the name
        self.name_surface = self.name_font.render(self.name, True, (255, 255, 255))
        self.name_rect = self.name_surface.get_rect(center=(x + length / 2, y - 20))
        self.start_val = initial_val #add this line
        self.target_val = initial_val #add this line


    def handle_event(self, event, engine):
        """Handles Pygame events for the slider."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.start_val = self.val # store the value when dragging starts
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Constrain the fill position within the slider's bounds
                mouse_x = event.pos[0]
                self.val = self.min_val + (mouse_x - self.x) / self.length * (self.max_val - self.min_val)
                self.val = max(self.min_val, min(self.val, self.max_val))
                engine.set_slider_value(self.name, self.val, propagate=True)
                engine.sliders[self.name] = self.val
                self.target_val = self.val # set target val.
                self.animation_start_time = time.time() #start time for animation


    def draw(self, surface, scroll_x, scroll_y):
        """Draws the slider on the Pygame surface, accounting for scroll."""
        # Use dragging color if dragging, otherwise use default color
        fill_color = self.dragging_fill_color if self.dragging else self.fill_color

        # Calculate adjusted position for drawing
        draw_rect = pygame.Rect(self.x - scroll_x, self.y - scroll_y, self.length, self.thickness)
        pygame.draw.rect(surface, self.bg_color, draw_rect, 0, 5)
        pygame.draw.rect(surface, self.outline_color, draw_rect, self.outline_width, 5)

        # Calculate fill width
        fill_width = int((self.val - self.min_val) / (self.max_val - self.min_val) * self.length)
        fill_rect = pygame.Rect(self.x - scroll_x, self.y - scroll_y, fill_width, self.thickness)
        pygame.draw.rect(surface, fill_color, fill_rect, 0, 5)

        # Display the slider's value inside the bar
        font = pygame.font.Font(None, 24)
        text_surface = font.render(f"{self.val:.2f}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=draw_rect.center)
        surface.blit(text_surface, text_rect)

        # Draw the slider name above the slider
        name_rect = self.name_rect.move(-scroll_x, -scroll_y)
        surface.blit(self.name_surface, name_rect)



def main():
    pygame.init()
    # Use pygame.FULLSCREEN to make the window fullscreen
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = screen.get_size()  # Get the actual screen size
    pygame.display.set_caption("Connected Sliders")
    font = pygame.font.Font(None, 36)

    # Initialize the slider engine
    engine = ConnectedSliderEngine()

    # Add sliders from the dictionary
    slider_data = {
        "Environment & Energy": [
            "Fossil Fuel Consumption",
            "Carbon Emissions",
            "Air Quality",
            "Global Temperature",
            "Sea Level Rise",
            "Investment in Renewable Energy",
            "Deforestation Rate",
            "Species Biodiversity",
            "Ocean Acidification",
            "Methane Emissions",
            "Plastic Pollution",
            "Water Usage",
            "Renewable Energy Production",
            "Energy Efficiency",
            "Sustainable Agriculture",
        ],
        "Economy": [
            "Economic Growth",
            "Unemployment Rate",
            "Global Energy Prices",
            "Income Inequality",
            "Industrial Output",
            "Resource Scarcity",
            "Trade Openness",
            "Inflation Rate",
            "Interest Rates",
            "Stock Market Volatility",
            "Foreign Direct Investment",
        ],
        "Society": [
            "Population Growth",
            "Urbanization Rate",
            "Healthcare Access",
            "Education Access",
            "Social Stability",
            "Migration Rate",
            "Crime Rate",
            "Civic Participation",
            "Life Expectancy",
            "Public Trust in Institutions",
            "Cultural Diversity",
        ],
        "Politics & Governance": [
            "Military Spending",
            "Government Transparency",
            "Democratic Index",
            "Corruption Perception",
            "International Cooperation",
            "Freedom of Press",
            "Political Stability",
            "Rule of Law",
            "Regulatory Quality",
            "Voice and Accountability",
        ],
        "Technology & Innovation": [
            "Tech Innovation Rate",
            "AI Development",
            "Cybersecurity Investment",
            "Automation Penetration",
            "Space Exploration Funding",
            "Digital Literacy",
            "Internet Access",
            "Renewable Energy Tech",
            "Biotechnology Development",
        ],
        "Health & Epidemics": [
            "Global Pandemic Risk",
            "Vaccination Rate",
            "Antibiotic Resistance",
            "Obesity Rate",
            "Mental Health Index",
            "Access to Clean Water",
        ],
        "Agriculture & Food": [
            "Food Security",
            "Crop Yield",
            "Agricultural Land Use",
            "Meat Consumption",
            "Sustainable Farming Practices",
            "Food Waste",
        ],
        "Culture & Wellbeing": [
            "Mental Health Index",
            "Work-Life Balance",
            "Cultural Diversity",
            "Social Connectedness",
            "Leisure Time",
            "Arts and Culture Funding",
        ]
    }

    # Calculate slider positions.  The sliders will be arranged in columns.
    slider_width = 300
    slider_height = 20
    slider_spacing = 50  # Increased spacing to accommodate names.  Changed from 30 to 50
    col_spacing = 350  # Space between columns
    start_x = 100
    start_y = 100
    
    for i, (category, sub_categories) in enumerate(slider_data.items()):
        x = start_x + i * col_spacing
        for j, sub_category in enumerate(sub_categories):
            y = start_y + j * slider_spacing
            slider = UISlider(sub_category, x, y, slider_width, 0, 100, 50,
                              bg_color=(0, 0, 0), fill_color=(255, 0, 0), outline_color=(255, 255, 255),
                              dragging_fill_color=(255, 100, 100), thickness=20)
            engine.add_slider(sub_category, 50)  # Add to engine
            engine.add_ui_slider(slider)  # Add to UI
            
    # Add connections here
    engine.connect_sliders("Fossil Fuel Consumption", "Carbon Emissions", 0.8)
    engine.connect_sliders("Carbon Emissions", "Global Temperature", 0.7)
    engine.connect_sliders("Global Temperature", "Sea Level Rise", 0.6)
    engine.connect_sliders("Investment in Renewable Energy", "Fossil Fuel Consumption", -0.5)
    engine.connect_sliders("Economic Growth", "Unemployment Rate", -0.6)
    engine.connect_sliders("Economic Growth", "Inflation Rate", 0.5)
    engine.connect_sliders("Inflation Rate", "Interest Rates", 0.9)
    engine.connect_sliders("Population Growth", "Urbanization Rate", 0.8)
    engine.connect_sliders("Healthcare Access", "Life Expectancy", 0.7)
    engine.connect_sliders("Education Access", "Digital Literacy", 0.6)
    engine.connect_sliders("Tech Innovation Rate", "Economic Growth", 0.4)
    engine.connect_sliders("AI Development", "Automation Penetration", 0.7)
    engine.connect_sliders("Global Pandemic Risk", "Vaccination Rate", -0.9)
    engine.connect_sliders("Food Security", "Sustainable Farming Practices", 0.6)
    engine.connect_sliders("Mental Health Index", "Social Connectedness", 0.5)
    

    running = True
    scroll_x = 0
    scroll_y = 0
    scroll_speed = 20  # Adjust for desired scroll speed
    fast_scroll_speed = 100 # added fast scroll
    scroll_delay = 200  # Initial delay before scrolling starts (milliseconds)
    scroll_interval = 50  # Interval between scroll steps (milliseconds)
    key_pressed = {  # Keep track of which keys are pressed
        pygame.K_LEFT: False,
        pygame.K_RIGHT: False,
        pygame.K_UP: False,
        pygame.K_DOWN: False,
    }
    
    scroll_start_time = 0 #store the time when scrolling starts
    
    content_width = 1500  # Adjust based on the number of sliders and columns.  This is a placeholder. You will need to calculate this based on the number of columns and the max x of the rightmost slider.
    content_height = 800 #  You will need to calculate this based on the number of sliders in the longest column and the max y of the bottommost slider.
    
    #Calculate content width and height
    max_x = 0
    max_y = 0
    for slider in engine.ui_sliders.values():
        max_x = max(max_x, slider.x + slider.length)
        max_y = max(max_y, slider.y + slider.thickness)
    content_width = max_x + 100  # Add some padding
    content_height = max_y + 100

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for slider in engine.ui_sliders.values():  # handle events for each slider.
                slider.handle_event(event, engine)

            if event.type == pygame.KEYDOWN:
                if event.key in key_pressed:
                    key_pressed[event.key] = True
                    scroll_start_time = pygame.time.get_ticks()  # Start the scroll timer
            elif event.type == pygame.KEYUP:
                if event.key in key_pressed:
                    key_pressed[event.key] = False
                    
        
        # Continuous scrolling logic
        current_time = pygame.time.get_ticks()
        
        
        if key_pressed[pygame.K_LEFT]:
            if current_time - scroll_start_time > scroll_delay:
                scroll_x -= scroll_speed if (current_time - scroll_start_time) < 500 else fast_scroll_speed
                
        if key_pressed[pygame.K_RIGHT]:
            if current_time - scroll_start_time > scroll_delay:
                scroll_x += scroll_speed if (current_time - scroll_start_time) < 500 else fast_scroll_speed
                
        if key_pressed[pygame.K_UP]:
            if current_time - scroll_start_time > scroll_delay:
                scroll_y -= scroll_speed if (current_time - scroll_start_time) < 500 else fast_scroll_speed
                
        if key_pressed[pygame.K_DOWN]:
            if current_time - scroll_start_time > scroll_delay:
                scroll_y += scroll_speed if (current_time - scroll_start_time) < 500 else fast_scroll_speed
        
        
        

        # Keep scroll within bounds
        scroll_x = max(0, min(scroll_x, content_width - screen_width))
        scroll_y = max(0, min(scroll_y, content_height - screen_height))


        engine.update_slider_values() #update slider values

        screen.fill((0, 0, 0))

        for slider in engine.ui_sliders.values():
            slider.draw(screen, scroll_x, scroll_y)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
