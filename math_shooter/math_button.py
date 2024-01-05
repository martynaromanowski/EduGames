# This is the Button object that we will be using inside our Math Game
import pygame
pygame.init()

#create the game window
(WIDTH, HEIGHT) = (1280, 720)
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Button:
    """
    Button Class for buttons used throughout games
    shape: string indicated whether the shape is a rectangle or circle
    font: font used for text displayed
    txt: string for text that will be displayed
    x_pos: x position
    y_pos: y_position
    clicked: boolean indiacting status of button
    surface: surface the button will be displayed on 
    """
    def __init__(self, shape, font, txt, x_pos, y_pos, clicked, surface):
        self.shape = shape
        self.font = font
        self.txt = txt
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.clicked = clicked
        self.surface = surface
        self.draw()
    
    def draw(self):
        #display the button on the screen
        cir = pygame.draw.circle(self.surface, "white", (self.x_pos, self.y_pos), 40)
        if cir.collidepoint(pygame.mouse.get_pos()):
            left_click = pygame.mouse.get_pressed()[0]
            if left_click:
                pygame.draw.circle(self.surface, "pink", (self.x_pos, self.y_pos), 40)
                self.clicked = True
            else:
                pygame.draw.circle(self.surface, "pink", (self.x_pos, self.y_pos), 40)
        cir = pygame.draw.circle(self.surface, "light gray", (self.x_pos, self.y_pos), 40, 3)
        self.surface.blit(self.font.render(self.txt, True, "black"), (self.x_pos-15, self.y_pos -25))

    def check_click(self):
        #check if the button was clicked by mouse or not
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_cir = pygame.rect.Rect((self.x_pos, self.y_pos), (400, 80))
        if left_click and button_cir.collidepoint(mouse_pos) and self.clicked:
            return True
        else:
            return False
