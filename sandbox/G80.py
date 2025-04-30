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
        self.simulation_running = True  # Add a flag to control simulation state
        self.propagate_interval = 0.01  # Add a new attribute to control propagation frequency (in seconds)
        self.next_propagation_time = time.time()  # Store the time of the next propagation
        self.sliders_to_propagate = set()

    def add_slider(self, name, initial_value=0):
        """Adds a new slider to the engine."""
        if name in self.sliders:
            return  # Skip adding the slider if it already exists.
        self.sliders[name] = float(initial_value)
        self.connections[name] = {}

    def connect_sliders(self, slider1, slider2, weight=1.0):
        """Connects two sliders, so a change in slider1 affects slider2."""
        if slider1 not in self.sliders or slider2 not in self.sliders: # Changed to self.sliders
            raise ValueError(f"One or both sliders do not exist. '{slider1}', '{slider2}'")
        self.connections[slider1][slider2] = float(weight)
        self.connections[slider2][slider1] = float(weight) #make connection both ways

    def set_slider_value(self, name, new_value, propagate=True):
        """Sets the value of a slider and propagates the change."""
        if name not in self.sliders:
            raise ValueError(f"Slider with name '{name}' does not exist.")

        old_value = self.sliders[name]
        new_value = float(new_value)  # Ensure new_value is a float
        new_value = max(0, min(new_value, 100))  # Cap the value between 0 and 100
        self.sliders[name] = new_value
        delta = new_value - old_value

        if propagate:
            self.sliders_to_propagate.add(name) # Add to set of sliders to propagate

    def get_slider_value(self, name):
        """Returns the current value of a slider."""
        if name not in self.sliders:
            raise ValueError(f"Slider with name '{name}' does not exist.")
        return self.sliders[name]

    def _propagate_change(self, source_slider, change):
        """Iteratively propagates the change through connected sliders."""
        queue = [(source_slider, change)]
        processed_sliders = set()

        while queue:
            current_slider, current_change = queue.pop(0)

            if current_slider in processed_sliders:
                continue  # Skip sliders that have already been processed
            processed_sliders.add(current_slider)

            for connected_slider, weight in self.connections[current_slider].items():
                impact = current_change * weight
                old_value = self.sliders[connected_slider]
                new_value = old_value + impact
                new_value = max(0, min(new_value, 100))
                self.sliders[connected_slider] = new_value

                # Update the UISlider's value directly, if it exists
                if connected_slider in self.ui_sliders:
                    self.ui_sliders[connected_slider].target_val = new_value
                    self.ui_sliders[connected_slider].start_val = self.ui_sliders[connected_slider].val
                    self.ui_sliders[connected_slider].animation_start_time = time.time()
                
                # Only add to queue if the connected slider hasn't been processed
                if connected_slider not in processed_sliders:
                    queue.append((connected_slider, impact))



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
        if self.simulation_running: # Only update if the simulation is running
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

    def update_simulation(self):
        """Update the simulation at a fixed interval."""
        current_time = time.time()
        if current_time >= self.next_propagation_time:
            # Pick a slider to propagate from.  For simplicity, pick the first one.
            #if self.sliders:
            #    first_slider_name = list(self.sliders.keys())[0]
            #    self._propagate_change(first_slider_name, 1)  # Start propagation with a small change.
            #    self.next_propagation_time = current_time + self.propagate_interval
            
            # Propagate changes for all sliders that have been changed
            for slider_name in self.sliders_to_propagate:
                self._propagate_change(slider_name, 1)  # Start propagation with a small change.
            self.sliders_to_propagate.clear() # Clear the set
            self.next_propagation_time = current_time + self.propagate_interval



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
        self.engine = None #store the engine
        self.is_being_dragged = False # Add this line



    def handle_event(self, event, engine, scroll_x, scroll_y):
        """Handles Pygame events for the slider."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Adjust mouse position for scrolling
            adjusted_mouse_pos = (event.pos[0] + scroll_x, event.pos[1] + scroll_y)
            if self.rect.collidepoint(adjusted_mouse_pos):
                self.dragging = True
                self.start_val = self.val # store the value when dragging starts
                engine.simulation_running = False  # Pause simulation when dragging starts
                self.engine = engine #store the engine
                self.is_being_dragged = True #set the flag

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
            if self.engine:
                self.engine.simulation_running = True  # Resume simulation when dragging ends
                self.engine = None
            self.is_being_dragged = False #reset the flag

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Constrain the fill position within the slider's bounds
                mouse_x = event.pos[0] + scroll_x # Adjust mouse position for scrolling
                self.val = self.min_val + (mouse_x - (self.x)) / self.length * (self.max_val - self.min_val) #removed self.x - scroll_x
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

    # Define slider data with initial values that approximate the real world
    slider_data = {
        "Environment & Energy": {
            "color": (50, 200, 50),  # Green
            "sub_categories": {
                "Fossil Fuel Consumption": 70,
                "Carbon Emissions": 75,
                "Air Quality": 60,
                "Global Temperature": 80,
                "Sea Level Rise": 65,
                "Investment in Renewable Energy": 40,
                "Deforestation Rate": 55,
                "Species Biodiversity": 50,
                "Ocean Acidification": 70,
                "Methane Emissions": 65,
                "Plastic Pollution": 80,
                "Water Usage": 75,
                "Renewable Energy Production": 30,
                "Energy Efficiency": 50,
                "Sustainable Agriculture": 40,
            },
        },
        "Economy": {
            "color": (255, 200, 50),  # Yellow
            "sub_categories": {
                "Economic Growth": 60,
                "Unemployment Rate": 40,
                "Global Energy Prices": 70,
                "Income Inequality": 70,
                "Industrial Output": 65,
                "Resource Scarcity": 55,
                "Trade Openness": 75,
                "Inflation Rate": 50,
                "Interest Rates": 45,
                "Stock Market Volatility": 55,
                "Foreign Direct Investment": 60,
            },
        },
        "Society": {
            "color": (50, 100, 255),  # Blue
            "sub_categories": {
                "Population Growth": 60,
                "Urbanization Rate": 55,
                "Healthcare Access": 65,
                "Education Access": 70,
                "Social Stability": 60,
                "Migration Rate": 50,
                "Crime Rate": 40,
                "Civic Participation": 55,
                "Life Expectancy": 75,
                "Public Trust in Institutions": 40,
                "Cultural Diversity": 70,
            },
        },
        "Politics & Governance": {
            "color": (200, 50, 255),  # Magenta
            "sub_categories": {
                "Military Spending": 50,
                "Government Transparency": 45,
                "Democratic Index": 60,
                "Corruption Perception": 65,
                "International Cooperation": 50,
                "Freedom of Press": 60,
                "Political Stability": 65,
                "Rule of Law": 70,
                "Regulatory Quality": 60,
                "Voice and Accountability": 55,
            },
        },
        "Technology & Innovation": {
            "color": (255, 50, 200),  # Pink
            "sub_categories": {
                "Tech Innovation Rate": 70,
                "AI Development": 50,
                "Cybersecurity Investment": 60,
                "Automation Penetration": 55,
                "Space Exploration Funding": 40,
                "Digital Literacy": 65,
                "Internet Access": 75,
                "Renewable Energy Tech": 45,
                "Biotechnology Development": 60,
            },
        },
        "Health & Epidemics": {
            "color": (255, 50, 50),  # Red
            "sub_categories": {
                "Global Pandemic Risk": 80,
                "Vaccination Rate": 70,
                "Antibiotic Resistance": 60,
                "Obesity Rate": 65,
                "Mental Health Index": 50,
                "Access to Clean Water": 75,
            },
        },
        "Agriculture & Food": {
            "color": (100, 255, 100),  # Light Green
            "sub_categories": {
                "Food Security": 60,
                "Crop Yield": 70,
                "Agricultural Land Use": 65,
                "Meat Consumption": 55,
                "Sustainable Farming Practices": 40,
                "Food Waste": 70,
            },
        },
        "Culture & Wellbeing": {
            "color": (200, 200, 200),  # Gray
            "sub_categories": {
                "Mental Health Index": 55,
                "Work-Life Balance": 60,
                "Cultural Diversity": 75,
                "Social Connectedness": 65,
                "Leisure Time": 50,
                "Arts and Culture Funding": 45,
            },
        },
    }

    # Calculate slider positions.  The sliders will be arranged in columns.
    slider_width = 300
    slider_height = 20
    slider_spacing = 50  # Increased spacing to accommodate names.  Changed from 30 to 50
    col_spacing = 350  # Space between columns
    start_x = 100
    start_y = 100

    for i, (category, data) in enumerate(slider_data.items()):
        x = start_x + i * col_spacing
        color = data["color"]
        for j, (sub_category, initial_value) in enumerate(data["sub_categories"].items()): # Changed to iterate through sub_categories.items()
            y = start_y + j * slider_spacing
            slider = UISlider(sub_category, x, y, slider_width, 0, 100, initial_value,
                                 bg_color=(0, 0, 0), fill_color=color, outline_color=(255, 255, 255),
                                 dragging_fill_color=(255, 100, 100), thickness=20)
            engine.add_slider(sub_category, initial_value)  # Add to engine with initial value
            engine.add_ui_slider(slider)  # Add to UI

    #test
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
    engine.connect_sliders("Fossil Fuel Consumption", "Global Energy Prices", 0.7)
    engine.connect_sliders("Carbon Emissions", "Air Quality", -0.8)
    engine.connect_sliders("Air Quality", "Healthcare Access", -0.6)
    engine.connect_sliders("Global Temperature", "Agricultural Land Use", -0.5)
    engine.connect_sliders("Sea Level Rise", "Migration Rate", 0.4)
    engine.connect_sliders("Investment in Renewable Energy", "Economic Growth", 0.6)
    engine.connect_sliders("Deforestation Rate", "Species Biodiversity", -0.9)
    engine.connect_sliders("Species Biodiversity", "Food Security", 0.5)
    engine.connect_sliders("Ocean Acidification", "Food Security", -0.4)
    engine.connect_sliders("Methane Emissions", "Global Temperature", 0.6)
    engine.connect_sliders("Plastic Pollution", "Ocean Acidification", 0.7)
    engine.connect_sliders("Water Usage", "Agricultural Land Use", 0.8)
    engine.connect_sliders("Renewable Energy Production", "Global Energy Prices", -0.6)
    engine.connect_sliders("Energy Efficiency", "Fossil Fuel Consumption", -0.4)
    engine.connect_sliders("Sustainable Agriculture", "Food Security", 0.7)
    engine.connect_sliders("Economic Growth", "Industrial Output", 0.8)
    engine.connect_sliders("Unemployment Rate", "Social Stability", -0.7)
    engine.connect_sliders("Global Energy Prices", "Inflation Rate", 0.6)
    engine.connect_sliders("Income Inequality", "Social Stability", -0.9)
    engine.connect_sliders("Industrial Output", "Resource Scarcity", 0.5)
    engine.connect_sliders("Resource Scarcity", "Global Energy Prices", 0.4)
    engine.connect_sliders("Trade Openness", "Economic Growth", 0.6)
    engine.connect_sliders("Inflation Rate", "Income Inequality", -0.5)
    engine.connect_sliders("Interest Rates", "Stock Market Volatility", 0.7)
    engine.connect_sliders("Stock Market Volatility", "Foreign Direct Investment", -0.6)
    engine.connect_sliders("Foreign Direct Investment", "Economic Growth", 0.9)
    engine.connect_sliders("Population Growth", "Food Security", -0.4)
    engine.connect_sliders("Urbanization Rate", "Air Quality", -0.5)
    engine.connect_sliders("Healthcare Access", "Economic Growth", 0.4)
    engine.connect_sliders("Education Access", "Income Inequality", -0.6)
    engine.connect_sliders("Social Stability", "Migration Rate", -0.5)
    engine.connect_sliders("Migration Rate", "Social Stability", -0.4)
    engine.connect_sliders("Crime Rate", "Social Stability", -0.8)
    engine.connect_sliders("Civic Participation", "Government Transparency", 0.7)
    engine.connect_sliders("Life Expectancy", "Healthcare Access", 0.8)
    engine.connect_sliders("Public Trust in Institutions", "Government Transparency", 0.9)
    engine.connect_sliders("Cultural Diversity", "Social Stability", 0.6)
    engine.connect_sliders("Military Spending", "Economic Growth", -0.5)
    engine.connect_sliders("Government Transparency", "Corruption Perception", -0.9)
    engine.connect_sliders("Democratic Index", "Social Stability", 0.7)
    engine.connect_sliders("Corruption Perception", "Foreign Direct Investment", -0.6)
    engine.connect_sliders("International Cooperation", "Global Temperature", -0.4)
    engine.connect_sliders("Freedom of Press", "Government Transparency", 0.8)
    engine.connect_sliders("Political Stability", "Economic Growth", 0.6)
    engine.connect_sliders("Rule of Law", "Foreign Direct Investment", 0.7)
    engine.connect_sliders("Regulatory Quality", "Industrial Output", 0.5)
    engine.connect_sliders("Voice and Accountability", "Social Stability", 0.4)
    engine.connect_sliders("Tech Innovation Rate", "Industrial Output", 0.7)
    engine.connect_sliders("AI Development", "Unemployment Rate", 0.6)
    engine.connect_sliders("Cybersecurity Investment", "Tech Innovation Rate", 0.5)
    engine.connect_sliders("Automation Penetration", "Unemployment Rate", 0.8)
    engine.connect_sliders("Space Exploration Funding", "Tech Innovation Rate", 0.4)
    engine.connect_sliders("Digital Literacy", "Education Access", 0.9)
    engine.connect_sliders("Internet Access", "Digital Literacy", 0.7)
    engine.connect_sliders("Renewable Energy Tech", "Investment in Renewable Energy", 0.6)
    engine.connect_sliders("Biotechnology Development", "Life Expectancy", 0.5)
    engine.connect_sliders("Global Pandemic Risk", "Economic Growth", -0.7)
    engine.connect_sliders("Vaccination Rate", "Life Expectancy", 0.9)
    engine.connect_sliders("Antibiotic Resistance", "Healthcare Access", -0.6)
    engine.connect_sliders("Obesity Rate", "Life Expectancy", -0.5)
    engine.connect_sliders("Mental Health Index", "Social Stability", 0.7)
    engine.connect_sliders("Access to Clean Water", "Healthcare Access", 0.8)
    engine.connect_sliders("Food Security", "Social Stability", 0.6)
    engine.connect_sliders("Crop Yield", "Food Security", 0.8)
    engine.connect_sliders("Agricultural Land Use", "Deforestation Rate", 0.7)
    engine.connect_sliders("Meat Consumption", "Agricultural Land Use", 0.5)
    engine.connect_sliders("Sustainable Farming Practices", "Crop Yield", 0.9)
    engine.connect_sliders("Food Waste", "Food Security", -0.4)
    engine.connect_sliders("Work-Life Balance", "Mental Health Index", 0.7)
    engine.connect_sliders("Social Connectedness", "Mental Health Index", 0.8)
    engine.connect_sliders("Leisure Time", "Work-Life Balance", 0.6)
    engine.connect_sliders("Arts and Culture Funding", "Social Connectedness", 0.5)
    engine.connect_sliders("Air Quality", "Global Temperature", 0.4)
    engine.connect_sliders("Migration Rate", "Population Growth", 0.3)


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
                slider.handle_event(event, engine, scroll_x, scroll_y) # Pass scroll_x and scroll_y

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #check for escape key
                    running = False #set running to false
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

        engine.update_simulation() #call update_simulation
        engine.update_slider_values() #update slider values

        screen.fill((0, 0, 0))

        for slider in engine.ui_sliders.values():
            slider.draw(screen, scroll_x, scroll_y)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

