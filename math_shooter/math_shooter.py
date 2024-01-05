#Math Asteroid Shooter Game where you shoot the asteroid with the correct answer to the math question displayed

#import necessary modules
import pygame
from pygame.math import Vector2
import random
import math
from math_button import Button

#display screen
pygame.init()
fps = 60
timer = pygame.time.Clock()

(WIDTH, HEIGHT) = (1280, 720)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Shooter Game")

# #load all customized fonts and images 
score_font = pygame.font.Font("math_shooter/assets/score_font.ttf", 50)
question_font = pygame.font.Font("math_shooter/assets/font.ttf", 48)
background = pygame.image.load("math_shooter/assets/galaxy.jpg")
question_display = pygame.image.load("math_shooter/assets/banner.png")
rocket = pygame.transform.scale(pygame.image.load("math_shooter/assets/rocket-ship.png"), (100,100))
empty_heart = pygame.transform.scale(pygame.image.load("math_shooter/assets/empty_heart.jpeg"), (50,50))
heart = pygame.transform.scale(pygame.image.load("math_shooter/assets/heart.png"), (50,50))

score = 0
asteroid_restrict = HEIGHT - 250 # define boundaries for the asteroid area
lives = [heart for _ in range(5)]   #list to store hearts as lives

#Asteroid object
class Asteroid:
    def __init__(self, position, velocity, answer):
        '''
        Position: the position of asteroid on the screen
        Velocity: for movement of the asteroid across the screen
        Answer: String of the possible answers for math equation
        '''
        self.position = Vector2(position)       #use imported vector library to get position of asteroid
        self.answer = answer
        #asteroid is displayed an an imported image
        self.asteroid_image = pygame.transform.scale(pygame.image.load("math_shooter/assets/asteroid.png"), (150,150))
        self.radius = self.asteroid_image.get_width()/2     #radius of asteroid is half of the size of the asteroid image
        self.velocity = Vector2(velocity)       #use imported vector library to get velocity of asteroid
    
    #draw the asteroid on the screen
    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.asteroid_image, blit_position)

        #draw the questions on the asteroids
        font = pygame.font.Font(None, 48)
        #generate answers using random number function alter made
        text_surface = font.render(self.answer, True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=blit_position + Vector2(self.radius))
        surface.blit(text_surface, text_rect)
    
    def move(self):
        #moves asteroid across the screen
        self.position = self.position + self.velocity

        # check for collisions with the screen edges
        if self.position.x - self.radius < 0:
            self.position.x = self.radius  # doesn't go past the left edge
            self.velocity.x *= -1  # reverse the horizontal velocity
        elif self.position.x + self.radius > WIDTH:
            self.position.x = WIDTH - self.radius  # doesn't go past the right edge
            self.velocity.x *= -1  # reverse the horizontal velocity

        if self.position.y - self.radius < 0:
            self.position.y = self.radius  # doesn't go past the top edge
            self.velocity.y = abs(self.velocity.y)  #  bounce up
        elif self.position.y + self.radius > asteroid_restrict:
            self.position.y = asteroid_restrict - self.radius  # doesn't go past the bottom edge
            self.velocity.y = -abs(self.velocity.y)  #  bounce down

#Function to create math questions and correct answer
def generate_question_and_answer():
    #choose a operator at random
    operators = ["+", "-", "x", "/"]
    choice = random.choice(operators)

    # Displaying addition or substraction
    if choice == "+" or choice == "-":
        #generate random numbers from 1-20
        num1 = random.randint(1,20)
        num2 = random.randint(1,20)
        if choice == "+":
            answer = num1 + num2
        else:
            answer = num1 - num2
        question = str(num1) + choice + str(num2) + "="
    else:
        # Displaying multiplication or division
        num1 = random.randint(1,12)
        num2 = random.randint(1,12)
        if choice == "x":
            answer = num1 * num2
            question = str(num1) + choice + str(num2) + "="
        else:
            answer = num1
            div = num1*num2
            question = str(div) + choice + str(num2) + "="

    return question, str(answer)

#Function to create wrong answers for asteroids
def generate_wrong_answers():
    return str(random.randint(1,45))

#Display rocket on the screen
def draw_rocket():
    #Rocket is displayed and rotated with appropriate geometrical calculation
    mouse_pos = pygame.mouse.get_pos()
    pointer = (WIDTH/2, HEIGHT - 150)
    clicks = pygame.mouse.get_pressed()

    if mouse_pos[0] != pointer[0]:
        slope = (mouse_pos[1] - pointer[0])/ (mouse_pos[0] - pointer[0])
    else:
        slope = float("-inf")

    angle = math.atan(slope)
    rotation = math.degrees(angle)

    if mouse_pos[0] < WIDTH/2:
        if mouse_pos[1] < 600:
            screen.blit(pygame.transform.rotate(rocket, 90-rotation), (WIDTH/2 - 90, HEIGHT-250))
            if clicks[0]:
                pygame.draw.circle(screen, (255,0,0), mouse_pos, 5)
    else:
        if mouse_pos[1] < 600:
            screen.blit(pygame.transform.rotate(rocket, 270-rotation), (WIDTH/2 - 30, HEIGHT-250))
            if clicks[0]:
                pygame.draw.circle(screen, (255,0,0), mouse_pos, 5)

def random_position(screen):
    return Vector2(
        random.randrange(screen.get_width()),
        random.randrange(screen.get_height()),
    )

def get_random_velcoity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)

#Display asteroids on the screen
def draw_asteroids(answer):
    position = random_position(screen)
    velocity = get_random_velcoity(1,3)

    #make sure they are in the boundary and not in scoreboard
    position.y = min(max(position.y, 0), asteroid_restrict) 
    asteroid = Asteroid(position, velocity, answer)
    return asteroid

#Display game screen
def draw_questions(score, question):
    rect_height = 150
    rect_width = HEIGHT - rect_height
    rect_color = (255,255,255)

    #create rectangle and draw
    rectangle = pygame.Rect(0, rect_width, WIDTH, rect_height)
    pygame.draw.rect(screen, rect_color, rectangle)

    #draw a border around the screen
    border_color = (0,0,0)
    pygame.draw.rect(screen, border_color, rectangle, 5)

    #postion score and question
    score_text = score_font.render(f"Score    {score}", True, (0,0,0))
    question_text = question_font.render(question, True, (0,0,0))

    score_text_rect = score_text.get_rect(left = 10, centery= (rect_width + rect_height // 2) - 30)
    question_text_rect = question_text.get_rect(centerx= WIDTH // 2, centery=rect_width + rect_height // 2)

    #draw lives
    x, y = 10, HEIGHT - 60
    for life in lives:
        screen.blit(life, (x,y))
        x += 60
    screen.blit(score_text, score_text_rect)
    screen.blit(question_text, question_text_rect)

#check if mouse clicks an asteroid
def check_shot(point, center, radius):
    distance = point.distance_to(center)
    return distance <= radius

#in game pause menu   
def pause():
    #display the pause button on the screen
    pause_button = Button("circle", score_font, "II", 1200, HEIGHT - 75, False, screen)
    pause_button.draw()

    pause_menu_rect = pygame.Rect(350, 200, 700, 300)

    pygame.draw.rect(screen, (255,255,255,100), [350, 200, 550, 250], 0, 5)
    pygame.draw.rect(screen, (255,255,255,200), [350, 200, 550, 250], 5, 5)

    #buttons for pause menu
    resume_button = Button("circle", score_font, ">", 450, 325, False, screen)
    resume_button.draw()
    quit_button = Button("circle", score_font, "X", 700, 325, False, screen)
    quit_button.draw()

    #pause menu text
    screen.blit(score_font.render("MENU", True, "black"), (380, 210))
    screen.blit(score_font.render("PLAY!", True, "black"), (500, 300))
    screen.blit(score_font.render("QUIT", True, "black"), (750, 300))

    return resume_button.clicked, quit_button.clicked, pause_button.clicked

#display game over screen
def draw_game_over(score):
    print("in here")  
    #display game over message
    game_over_font = pygame.font.Font("math_shooter/assets/game_over.ttf", 500)
    game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    #display game over screen
    screen.fill((0,0,0))
    screen.blit(game_over_text, game_over_rect)
    
    quit_game = False
    while not quit_game:
        play_again_button = Button("circle", score_font, "P", WIDTH // 2 - 100, HEIGHT // 2 + 100, False, screen)
        quit_button = Button("circle", score_font, "X", WIDTH // 2 + 100, HEIGHT // 2 + 100, False, screen)
        play_again_button.draw()
        quit_button.draw()
        
        play_again_label = score_font.render("Play again!", True, (255, 255, 255))
        play_again_label_rect = play_again_label.get_rect(center=(WIDTH // 2 - 100, HEIGHT // 2 + 200))
        screen.blit(play_again_label, play_again_label_rect)

        quit_label = score_font.render("Quit", True, (255, 255, 255))
        quit_label_rect = quit_label.get_rect(center=(WIDTH // 2 + 100, HEIGHT // 2 + 200))
        screen.blit(quit_label, quit_label_rect)
        # pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
    
        pygame.display.flip()
        if play_again_button.clicked:
            return False 
        elif quit_button.clicked:
            return True
    return quit_game
 

#store asteroids and generate answers
asteroids = []
question, correct_answer = generate_question_and_answer()
asteroids.append(draw_asteroids(correct_answer)) 

pause_button = Button("circle", score_font, "II", 1200, HEIGHT - 75, False, screen)
running = True
paused = False
game_over = False
quit_game = False
i = len(lives)      #variable for removing lives from lives array

while running:
    timer.tick(fps)
    screen.fill("black")
    screen.blit(background, (0,0))
    draw_questions(score, question)

    #if game is not puased, display normal game function
    if not paused:
        draw_rocket()

        for asteroid in asteroids:
            asteroid.move()
            asteroid.draw(screen)

        if len(asteroids) < 6:
            asteroids.append(draw_asteroids(generate_wrong_answers()))

    for event in pygame.event.get():
        draw_questions(score, question)
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #mouse is clicked
            mouse_pos = Vector2(pygame.mouse.get_pos())
            if not paused and pause_button.clicked:
                paused = True   #game is paused when pause button is clicked
            for asteroid in asteroids:
                if not paused and check_shot(mouse_pos, asteroid.position, asteroid.radius):    #check if asteroid is shot
                    if asteroid.answer == correct_answer:           #score points to correct answer, add points, and generate new question
                        score += 10
                        asteroids.clear()
                        for _ in range(5):
                            asteroids.append(draw_asteroids(generate_wrong_answers()))
                        question, correct_answer = generate_question_and_answer()
                        asteroids.append(draw_asteroids(correct_answer))
                    else:       #if wrong answer is chosen, remove lives and remove that asteroid from the screen
                        if i >= 1:
                            i -= 1
                            lives[i] = empty_heart
                            asteroids.remove(asteroid)
                            #if all lives are lost display game over screen
                        if i == 0:
                            game_over = True
                  
    if game_over:
        quit_game = draw_game_over(score)
        print(quit_game)
        if quit_game:
            running = False
        else: 
            print("hiiiiiiii")
            game_over = False
            score = 0
            i = len(lives) 
            lives = [heart for _ in range(5)]
            asteroids.clear()
            for _ in range(5):
                asteroids.append(draw_asteroids(generate_wrong_answers()))
            question, correct_answer = generate_question_and_answer()
            asteroids.append(draw_asteroids(correct_answer))

    if paused:
        # Display the pause menu
        resume_button, quit_button, pause_button_clicked = pause()
        if resume_button:
            paused = False
        if quit_button:
            # When doing all games, this should return you to the main menu
            # check_high_score()
            running = False

    pause_button.draw()
    pygame.display.flip()

pygame.quit()
