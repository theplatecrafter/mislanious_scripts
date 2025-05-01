import pygame
import sys

def debug_fonts():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Font Debugger")
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    
    # List of Japanese fonts to try
    japanese_fonts = [
        "Yu Gothic", "MS Gothic", "Meiryo", "Hiragino Sans", 
        "Noto Sans CJK JP", "Noto Sans JP", "Arial Unicode MS", "Osaka",
        "MS Mincho", "sans-serif"
    ]
    
    test_text = "日本語テスト ABC 123"
    font_size = 20
    y_position = 20
    
    # System available fonts
    print("Available system fonts:")
    available_fonts = pygame.font.get_fonts()
    for i, font_name in enumerate(available_fonts):
        if i < 20 or "sans" in font_name or "gothic" in font_name:  # Limit output
            print(f"- {font_name}")
    
    # Test each font
    print("\nTesting Japanese fonts:")
    
    fonts_loaded = []
    fonts_failed = []
    
    # Wait for the user to close the window
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        screen.fill(BLACK)
        y_position = 20
        
        # Try each font
        for font_name in japanese_fonts:
            try:
                font = pygame.font.SysFont(font_name, font_size)
                text_surface = font.render(f"{font_name}: {test_text}", True, WHITE)
                screen.blit(text_surface, (20, y_position))
                if font_name not in fonts_loaded:
                    fonts_loaded.append(font_name)
                    print(f"✓ {font_name} loaded successfully")
                y_position += 30
            except Exception as e:
                if font_name not in fonts_failed:
                    fonts_failed.append(font_name)
                    print(f"✗ {font_name} failed: {e}")
                
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    
    print("\nFont loading results:")
    print("Successful fonts:", ", ".join(fonts_loaded))
    print("Failed fonts:", ", ".join(fonts_failed))
    
if __name__ == "__main__":
    debug_fonts()