import pygame
import sys
from pygame.sprite import Sprite
from enum import Enum
from pygame.sprite import RenderUpdates

#just added
(WIDTH, HEIGHT) = (1280, 720)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((228, 218, 199))
pygame.display.set_caption("Quiz Game!")

#boxes to display question and answers 
main_box = pygame.Rect(50, 40, 820, 240)
timer_box = pygame.Rect(990, 40, 195, 165)
answer_box1 = pygame.Rect(50, 358, 495, 165)
answer_box2 = pygame.Rect(735, 358, 495, 165)
answer_box3 = pygame.Rect(50, 538, 495, 165)
answer_box4 = pygame.Rect(735, 538, 495, 165)

#list of all answer boxes
answer_boxes = [answer_box1, answer_box2, answer_box3, answer_box4]
colors = [(248, 200, 220), (253, 253, 150), (174, 198, 207), (193, 225, 193)]
score = 0

def uplaod_questions(filename):
    questions = []
    with open(filename, "r") as file:
        question = []
        for count, line in enumerate(file):
            line = line.strip()  
            question.append(line)
            if count % 6 == 5:
                questions.append(question.copy()) 
                question.clear()

    return questions

def start_screen_text(text, font_size, text_rgb):
    # return the start screen with text written on it
    font = pygame.font.Font("quiz_game/assets/creamy-chalk-font/CreamyChalk-PKa4E.ttf", int(font_size))
    surface = font.render(text, True, text_rgb)
    return surface.convert_alpha()

class Text_Sprite(Sprite):
    #an element that can be added onto a surface
    def __init__(self, center_position, text, font_size, text_rgb, action=None):
        '''
        center_position: (x,y) tuple
        text: string of text to display
        font_size: int for size of text
        text_rgb: tuple (r, g, b) 
        '''
        # self.mouse_over = False         # is mouse held over text

        # #default text
        self.default_text = start_screen_text(text, font_size, text_rgb)
        self.default_rect = self.default_text.get_rect(center=center_position)
        
        self.action = action

        super().__init__()
    
    @property
    def image(self):
        return self.default_text
   
    @property
    def rect(self):   
        return self.default_rect 

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            # self.mouse_over = True
            if mouse_up:
                return self.action
        # else:
        #     self.mouse_over = False

    def draw(self, surf):
        surf.blit(self.image, self.rect)

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    GAMEOVER = 2

def start_screen(screen):
    screen.fill((228, 218, 199))
    (WIDTH, HEIGHT) = (1280, 720)
    chalkboard = pygame.image.load("quiz_game/assets/chalk_board.img") 
    chalk_rect = chalkboard.get_rect()
    center_x = (WIDTH - chalk_rect.width)//2
    center_y = (HEIGHT - chalk_rect.height)//2
    screen.blit(chalkboard, (center_x, center_y))

    font = pygame.font.Font("quiz_game/assets/creamy-chalk-font/CreamyChalk-PKa4E.ttf", 120)
    game_name = font.render("QUIZ GAME", True, (255,255,255))
    game_name_rect = game_name.get_rect()
    game_name_rect.center = (625, 300)
    screen.blit(game_name, game_name_rect)

    play_game = Text_Sprite(
        center_position=(425 ,450),
        text = "Start Quiz",
        font_size= 40,
        text_rgb= (255, 255, 255),
        action=GameState.NEWGAME
    )

    quit_game = Text_Sprite(
        center_position=(850 ,450),
        text = "Quit Quiz",
        font_size= 40,
        text_rgb= (255, 255, 255),
        action= GameState.QUIT
    )

    buttons = RenderUpdates(play_game, quit_game)
    return game_loop(screen, buttons)

def game_over_screen(screen):
    screen.fill((228, 218, 199))
    (WIDTH, HEIGHT) = (1280, 720)
    chalkboard = pygame.image.load("quiz_game/assets/chalk_board.img") 
    chalk_rect = chalkboard.get_rect()
    center_x = (WIDTH - chalk_rect.width)//2
    center_y = (HEIGHT - chalk_rect.height)//2
    screen.blit(chalkboard, (center_x, center_y))
    font = pygame.font.Font("quiz_game/assets/creamy-chalk-font/CreamyChalk-PKa4E.ttf", 120)
    
    # Display Game Over message
    game_over_text = font.render("Game Over!", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(640, 200))
    screen.blit(game_over_text, game_over_rect)

    # Display Score
    score_font = pygame.font.Font("quiz_game/assets/creamy-chalk-font/CreamyChalk-PKa4E.ttf", 50)
    score_text = score_font.render("Your Score: " + str(quiz_game.score), True, (250, 250, 250))
    score_rect = score_text.get_rect(center=(640, 350))
    screen.blit(score_text, score_rect)

    play_game = Text_Sprite(
        center_position=(425 ,450),
        text = "Start Quiz",
        font_size= 40,
        text_rgb= (255, 255, 255),
        action=GameState.NEWGAME
    )

    quit_game = Text_Sprite(
        center_position=(850 ,450),
        text = "Quit Quiz",
        font_size= 40,
        text_rgb= (255, 255, 255),
        action= GameState.QUIT
    )

    buttons = RenderUpdates(play_game, quit_game)
    return game_loop(screen, buttons)
    
class QuizGame:
    def __init__(self):
        self.score = 0
        self.current_question = None
        self.questions = uplaod_questions("quiz_game/questions.txt") #update this later to be length of uploarded questions
        self.next_questions()
    
    def next_questions(self):
        if self.questions:
            self.current_question = self.questions.pop(0)
        else:
            # self.quiz_game_over()
            game_over_screen(screen)
            return

    def check_answer(self, selected_answer_index):
        if self.current_question and len(self.current_question) > 5:
            if selected_answer_index == int(self.current_question[5]):
                self.score += 1
            self.next_questions()

    def quiz_draw(self, screen):
        (WIDTH, HEIGHT) = (1280, 720)

        quit_button = Text_Sprite(
            center_position= (WIDTH-150, 20),
            text= "Return to main menu",
            font_size= 20,
            text_rgb= (0,0,0),
            action= GameState.QUIT
        )

        button = RenderUpdates(quit_button)

        #new stuff
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                    on_mouse_down(event.pos)
        #end new
        #all indented below 
            screen.fill((251, 251, 244))
            pygame.draw.rect(screen, (195, 177, 225), main_box)
            pygame.draw.rect(screen, (195, 177, 225), timer_box)
        #draw answer rectanges
            for i in range(len(answer_boxes)):
                pygame.draw.rect(screen, colors[i], answer_boxes[i])
    
        #display timer box
            font = pygame.font.Font(None, 36)
            timer_text = font.render("Good Luck! ", True, (0, 0, 0))
            timer_text_rect = timer_text.get_rect(center=timer_box.center)
            screen.blit(timer_text, timer_text_rect)
            
        #display question
            question_font = pygame.font.Font(None, 48)
            question_surface = question_font.render(self.current_question[0], True, (0, 0, 0))
            question_surface_rect = question_surface.get_rect(center=main_box.center)
            screen.blit(question_surface, question_surface_rect)
        
            if self.current_question:
                # question_text = self.current_question[0]
                index = 1
                for box in answer_boxes:
                    q_font = pygame.font.Font(None, 40)
                    q_surface = q_font.render(str(self.current_question[index]), True, (0, 0, 0))
                    q_surface_rect = q_surface.get_rect(center=box.center)
                    screen.blit(q_surface, q_surface_rect)
                    index = index + 1
            else:
                game_over_screen(screen)

        #display score
            score_font = pygame.font.Font(None, 36)
            score_text = score_font.render("Score:" + str(self.score), True, (0, 0, 0))
            screen.blit(score_text, (50,10))

            pygame.display.flip() 
    
    def reset_game(self):
        self.score = 0
        self.next_questions()

 
def on_mouse_down(pos):
    index = 1
    for box in answer_boxes:
        if box.collidepoint(pos):
            quiz_game.check_answer(index)
        index += 1

def game_loop(screen, buttons):
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_up = True
                for button in buttons:
                    act = button.update(pygame.mouse.get_pos(), mouse_up)
                    if act is not None:
                        return act
                on_mouse_down(event.pos)

        for button in buttons:
            if button.action == GameState.QUIT and button.rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    pygame.quit()
                    sys.exit()

        buttons.update(pygame.mouse.get_pos(), mouse_up)
        buttons.draw(screen)
        pygame.display.flip()
        
quiz_game = QuizGame()

def main():
    pygame.init()
    pygame.font.init()

    game_state = GameState.TITLE

    while True:
        if game_state == GameState.QUIT:
            pygame.quit()
            sys.exit()
        elif game_state == GameState.TITLE:
            game_state = start_screen(screen)
        elif game_state == GameState.NEWGAME:
            game_state = quiz_game.quiz_draw(screen)
        elif game_state == GameState.GAMEOVER:
            game_state = game_over_screen(screen)

if __name__ == "__main__":
    main()

sys.exit()