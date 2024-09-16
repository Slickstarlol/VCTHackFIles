import pygame

WINDOWWIDTH = 600
WINDOWHEIGHT = 800

WHITE = (255, 255, 255)
DARK = (60, 60, 60)

def handle_events():
    running = True
    active = False
    
    font = pygame.font.Font(None, 32)
    content = 'Type here ...'
    user_text = ''

    while running:
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # Input box
        box = pygame.Rect(1, screen_height - 100, screen_width - 2, 100)
        box_out = pygame.Rect(1, screen_height - 102, screen_width - 2, 102)

        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN: 
                if box.collidepoint(event.pos): 
                    active = True
                else: 
                    active = False

            if active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    # Remove the last character
                    user_text = user_text[:-1]
                else:
                    # Add the new character
                    user_text += event.unicode

        screen.fill(DARK)

        # Draw the input box
        pygame.draw.rect(screen, WHITE, box)
        pygame.draw.rect(screen, DARK, box_out, 2, 3)

        # Render text
        if user_text:
            text = font.render(user_text, True, (0, 0, 0))
        else:
            text = font.render(content, True, (0, 0, 0))

        screen.blit(text, (box.x + 5, box.y + 5))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

def main():
    global screen, clock

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    screen.fill(DARK)

    handle_events()

if __name__ == "__main__": 
    main()
