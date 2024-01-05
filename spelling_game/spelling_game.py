#Typing Game
import pygame, random, copy 
from button import Button
pygame.init()

#natural language tooklit for corpus 
from nltk.corpus import words
wordlist = words.words()

#high score tracker
file = open("/Users/ada/martyna_project/spelling_game/high_score_type.txt", "r")
read = file.readlines()
high_score = int(read[0])
file.close()

#sort words by length
len_indexes = []
length = 1
wordlist.sort(key=len)
for i in range(len(wordlist)):
    if len(wordlist[i]) > length:
        length += 1
        len_indexes.append(i)
len_indexes.append(len(wordlist)) #max length

#Game screen set up
(WIDTH, HEIGHT) = (1280, 720)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Game")
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
timer = pygame.time.Clock()
fps = 60

#game varibales
level = 1
user_input = ""
submit = ""
score = 0
word_objects = []
lives = 5
paused = True
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
           "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
new_level = True
#2 letters to 7 letters words only, expressed as boolean values
choices = [False, True, False, False, False, False, False]
#fonts
head_font = pygame.font.Font("fonts/Square.ttf", 50)
pause_font = pygame.font.Font("fonts/1up.ttf", 38)
banner_font = pygame.font.Font("fonts/1up.ttf", 28)
font = pygame.font.Font("fonts/AldotheApache.ttf", 48)

class Word:
    def __init__(self, text, speed, y_pos, x_pos):
        '''
        text: string of text to display
        speed: speed word goes across screen
        y_pos: position of word vertically on screen
        x_pos: position of word horizontally on screen
        '''
        self.text = text
        self.speed = speed
        self.y_pos = y_pos
        self.x_pos = x_pos

    #display word on the screen
    def draw(self):
        screen.blit(font.render(self.text, True, "white"), (self.x_pos, self.y_pos))
        string_length = len(user_input)
        #show that a word is typed
        if user_input == self.text[:string_length]:
            screen.blit(font.render(user_input, True, "red"), (self.x_pos, self.y_pos))
    
    def update(self):
        #Moves word acorss screen
        self.x_pos -= self.speed

#create game screen with scores and other data
def draw_screen():
    #botton rectangles that hold user input, level, etc.
    pygame.draw.rect(screen, "white", [0, HEIGHT - 100, WIDTH, 100], 0)
    pygame.draw.rect(screen, "black", [0, 0, WIDTH, HEIGHT], 5)
    pygame.draw.line(screen, "black", (250, HEIGHT-100), (250, HEIGHT), 2)
    pygame.draw.line(screen, "black", (1100, HEIGHT-100), (1100, HEIGHT), 2)

    #current level, current input, high score, score, lives, pause
    screen.blit(head_font.render(f'Level: {level}', True, "black"), (20, HEIGHT - 75))
    screen.blit(head_font.render(f'"{user_input}"', True, "black"), (270, HEIGHT - 75))
    
    #pause button
    pause_button = Button("circle", pause_font, "II", 1150, HEIGHT - 50, False, screen)
    pause_button.draw()

    screen.blit(banner_font.render(f' Score: {score}', True, "white"), (550, 10))
    screen.blit(banner_font.render(f' Best: {high_score}', True, "white"), (1000, 10))
    screen.blit(banner_font.render(f' Lives: {lives}', True, "white"), (100, 10))
    return pause_button.clicked

# display screen when pause button is pressed
def pause():
    choice_changes = copy.deepcopy(choices)
    surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surf, (255,255,255,100), [350, 200, 700, 300], 0, 5)
    pygame.draw.rect(surf, (255,255,255,200), [350, 200, 700, 300], 5, 5)

    #buttons for pause menu
    resume_button = Button("circle", pause_font, ">", 450, 300, False, surf)
    resume_button.draw()
    quit_button = Button("circle", pause_font, "X", 700, 300, False, surf)
    quit_button.draw()

    #pause menu text
    surf.blit(head_font.render("MENU", True, "white"), (380, 210))
    surf.blit(head_font.render("PLAY!", True, "white"), (500, 275))
    surf.blit(head_font.render("QUIT", True, "white"), (750, 275))
    surf.blit(head_font.render("Letter Length:", True, "white"), (475, 350))
   
    #button for seleting length of letters in word
    for i in range(len(choices)):
        word_button = Button("circle", pause_font, str(i+2), 420 + (i*90), 450, False, surf)
        word_button.draw()
        if word_button.clicked:
            if choice_changes[i]:
                choice_changes[i] = False
            else:
                choice_changes[i] = True
        if choices[i]:
            pygame.draw.circle(surf, "red", (420 + (i*90), 450), 40, 5)
    screen.blit(surf, (0,0))
    return resume_button.clicked, choice_changes, quit_button.clicked

#choose words to display on screen
def make_words():
    word_objects = []
    include = []
    #make sure words dont overlap
    vertical_spacing = (HEIGHT - 150)// level 
    if True not in choices:
        choices[0] = True
    for i in range(len(choices)):
        if choices[i]:
            include.append((len_indexes[i], len_indexes[i+1]))
    for i in range(level):
        speed = random.randint(2, 3)
        #range to draw words in
        y_pos = random.randint(10 + (i*vertical_spacing), (i + 1) * vertical_spacing)
        x_pos = random.randint(WIDTH, WIDTH + 750)
        index_selection = random.choice(include)
        index = random.randint(index_selection[0], index_selection[1])
        text = wordlist[index].lower()
        new_word = Word(text, speed, y_pos, x_pos)
        word_objects.append(new_word)

    return word_objects

def check_answer(cur_score):
    for word in word_objects:
        if word.text == submit:
            points = word.speed * len(word.text) * 10 * (len(word.text)/4)
            cur_score += int(points)
            word_objects.remove(word)

    return cur_score

def check_high_score():
    global high_score
    if score > high_score:
        high_score = score
        file = open("high_score_type.txt", "w")
        file.write(str(int(high_score)))
        file.close()

#main game loop
running = True
while running:
    screen.fill("black")
    timer.tick(fps)

    pause_button = draw_screen()

    if paused:
        #paused menu
        resume_button, changes, quit_button = pause()
        if resume_button:
            paused = False
        if quit_button:
            #when doing all games, this should return you to main menu
            check_high_score()
            running = False
    if new_level and not paused:
        word_objects = make_words()
        new_level = False
    else:
        for w in word_objects:
            w.draw()
            if not paused:
                w.update()
            if w.x_pos < -200:
                word_objects.remove(w)
                lives -= 1
    #Move on to next level once words are finished
    if len(word_objects) <= 0 and not paused:
        level += 1
        new_level = True

    if submit != "":
        init = score
        score = check_answer(score)
        submit = ""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            check_high_score()
            running = False
        if event.type == pygame.KEYDOWN:
            if not paused:
                if event.unicode.lower() in letters:
                    user_input += event.unicode.lower()
                #deleting
                if event.key == pygame.K_BACKSPACE and len(user_input) > 0:
                    user_input = user_input[:-1]
                #submitting
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    submit = user_input
                    user_input = ""
            if event.type == pygame.K_ESCAPE:
                if paused:
                    paused = False
                else:
                    paused = True
        if event.type == pygame.MOUSEBUTTONUP and paused:
            if event.button == 1:
                choices = changes

    if pause_button:
        paused = True
    
    #reset everything once you die
    if lives < 0:
        paused = True
        level = 1
        lives = 5
        word_objects = []
        new_level = True
        check_high_score()
        score = 0

    pygame.display.flip()
pygame.quit()