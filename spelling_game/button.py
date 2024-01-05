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
    
    #place button accordingly on screen
    def draw(self):
        if self.shape == "rect":
            button_text = self.font.render(self.txt, True, "black")
            button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (400, 80))
            #change color when clicked on 
            if self.check_click():
                pygame.draw.rect(screen, "white", button_rect, 2, 5)
                pygame.draw.rect(screen, ((65, 105, 225)), button_rect, 0, 5)
            else:
                pygame.draw.rect(screen, "white", button_rect, 0, 5)
                pygame.draw.rect(screen, ((65, 105, 225)), button_rect, 2, 5)
            screen.blit(button_text, (self.x_pos + 20, self.y_pos + 15))
        elif self.shape == "circle":
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

    #check if you are clicking on button or not 
    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (400, 80))
        if left_click and button_rect.collidepoint(mouse_pos) and self.clicked:
            return True
        else:
            return False

