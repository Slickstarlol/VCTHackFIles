# Example file showing a basic pygame "game loop"
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

        #input box
        box = pygame.Rect(1, screen_height - 100, screen_width - 2, 100)
        box_out = pygame.Rect(1, screen_height - 102, screen_width - 2, 102)

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if box.collidepoint(event.pos): 
                active = True
            else: 
                active = False

        if active:
            print(event.type == pygame.KEYDOWN)
            if event.type == pygame.KEYDOWN: 
                print(event.type)
                # Check for backspace 
                if event.key == pygame.K_BACKSPACE: 
    
                    # get text input from 0 to -1 i.e. end. 
                    user_text = user_text[:-1] 
    
                # Unicode standard is used for string 
                # formation 
                else: 
                    user_text += event.unicode
      

        screen.fill(DARK)

        # RENDER YOUR GAME HERE
                
        pygame.draw.rect(screen, WHITE, box)
        pygame.draw.rect(screen, DARK, box_out, 2, 3)

        if user_text != '':
            text = font.render(user_text, True, (0, 0, 0))
        else:
            text = font.render(content, True, (0, 0, 0))

        # print(user_text)

        screen.blit(text, (box.x + 5, box.y + 5))

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()


def main():

    global screen, clock

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    screen.fill(DARK)

    handle_events()

if __name__ == "__main__": 
    main()  