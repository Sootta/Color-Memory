import pygame
from pygame.locals import *
import sys
from enum import Enum
import time
import random

W, H = 600, 400
FPS = 30
BLACK = (50, 50, 50)
BLACK_2 = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
VIOLET = (127, 0, 225)
ORANGE = (255, 165, 0)

COLOR_ALL = [RED, BLUE, GREEN, YELLOW, VIOLET, ORANGE, WHITE, WHITE]

pygame.init()

class GameLevel(Enum):
    Std = 0
    Medium = 1
    Hard = 2
    Difficult = 3
    
class Button:
    size_x = 75
    size_y = 60
    def __init__(self, x: int, y: int, color: Color):
        self.x_pos = x
        self.y_pos = y
        self.color = color
    def draw(self):
        pygame.draw.rect(WINDOW, self.color, (self.x_pos, self.y_pos, self.size_x, self.size_y))
        pygame.draw.rect(WINDOW, BLACK_2, (self.x_pos, self.y_pos, 75, 60), 3)
    def is_clicked(self, mouse_x: int, mouse_y: int):
        if (
            abs(mouse_x - (self.x_pos + self.size_x/2)) < self.size_x/2 and
            abs(mouse_y - (self.y_pos + self.size_y/2)) < self.size_y/2
        ):
            return 1
        else:
            return 0
 
BUTTONS = [
    Button(75,  200, RED),
    Button(200, 200, BLUE),
    Button(325, 200, GREEN),
    Button(450, 200, YELLOW),
    Button(75,  310, VIOLET),
    Button(200, 310, ORANGE),
    Button(325, 310, WHITE),
    Button(450, 310, WHITE)
]
    
font = pygame.font.SysFont("freesansbold.ttf", 50)
TEXT_ELEMENT = [
    font.render("RED",    True, BLACK_2),
    font.render("BLUE",   True, BLACK_2),
    font.render("GREEN",  True, BLACK_2),
    font.render("YELLOW", True, BLACK_2),
    font.render("VIOLET", True, BLACK_2),
    font.render("ORANGE", True, BLACK_2),
    font.render("WHITE",  True, BLACK_2),
    font.render("J",      True, BLACK_2)
]

WINDOW = pygame.display.set_mode((W, H))
CLOCK = pygame.time.Clock()

pygame.mixer.init()
sounds = {
    "success": pygame.mixer.Sound("sound/success_sound.mp3"),
    "click": pygame.mixer.Sound("sound/button_click.mp3"),
    "wrong": pygame.mixer.Sound("sound/wrong_sound.mp3")
} 

def main():
    while True:
        ready()
        for i in range(4):
            is_game_over = start(GameLevel(i))
            if is_game_over == 0:
                game_over()
                break
            if i == 3:
                end()
    
def ready():
    title = font.render("COLOR MEMORY", True, WHITE)
    text_start = font.render("Start", True, BLACK)
    text_quit = font.render("Quit", True, BLACK)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if abs(x - 300) < 70 and abs(y - 230) < 30:
                    play_sound("click")
                    return
                elif abs(x - 300) < 70 and abs(y - 330) < 30:
                    play_sound("click")
                    pygame.quit()
                    sys.exit()

        WINDOW.fill(BLACK)
        pygame.draw.rect(WINDOW, WHITE, (230, 200, 140, 60))
        pygame.draw.rect(WINDOW, WHITE, (230, 300, 140, 60))
        WINDOW.blit(title, (160, 100))
        WINDOW.blit(text_start, (257, 215))
        WINDOW.blit(text_quit, (260, 315))
        pygame.display.update()
        CLOCK.tick(FPS)

def game_over():
    title = font.render("GAME OVER", True, WHITE)
    WINDOW.fill(BLACK)
    WINDOW.blit(title, (180,100))
    pygame.display.update()
    time.sleep(2)

def end():
    WINDOW.fill(BLACK)
    text_no = font.render("Congratulations!", True, WHITE)
    WINDOW.blit(text_no, (160, 100))
    pygame.display.update()
    time.sleep(2)

def start(level: GameLevel):
    WINDOW.fill(BLACK)
    if level == GameLevel.Difficult:
        title = font.render(f"FINAL ROUND", True, WHITE)
        WINDOW.blit(title, (190, 100))
    else:
        title = font.render(f"ROUND{level.value + 1}", True, WHITE)
        WINDOW.blit(title, (220, 100))
    pygame.display.update()
    time.sleep(2)

    max_questions = 0
    rand_range = 0

    if level == GameLevel.Std:
        max_questions = 4
        rand_range = 4
    elif level == GameLevel.Medium:
        max_questions = 5
        rand_range = 5
    elif level == GameLevel.Hard:
        max_questions = 6
        rand_range = 6
    elif level == GameLevel.Difficult:
        max_questions = 7
        rand_range = 8

    answer_number = []
    fake_number = []

    for i in range(max_questions):
        n = random.randrange(0, rand_range)
        f = random.randrange(0, rand_range)
        answer_number.append(n)
        fake_number.append(f)

    WINDOW.fill(BLACK)
    pygame.display.update()
    count = 0
    game_count = 1
    show_problem(answer_number, game_count, level, fake_number)

    t1 = time.time()

    while True:
        t0 = time.time() - t1
        if t0 * 15 > 400:
            return 0
        pygame.draw.rect(WINDOW, (0,0,0), (0, 0, 600, int(t0) * 15))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                color_num = check_color(x, y, level)
                if color_num == answer_number[count]:
                    pygame.draw.rect(WINDOW, COLOR_ALL[color_num], (100, 40, 400, 130))
                    pygame.draw.rect(WINDOW, (0,0,0), (100, 40, 400, 130),5)
                    WINDOW.blit(TEXT_ELEMENT[color_num], (220, 90))
                    
                    play_sound("click")
                    count += 1
                elif color_num != None:
                    count = 0
                    WINDOW.fill(BLACK)
                    pygame.draw.rect(WINDOW, (0,0,0), (0, 0, 600, int(t0) * 15))
                    text_no = font.render("NO", True, WHITE)
                    WINDOW.blit(text_no, (250, 100))
                    pygame.display.update()
                    play_sound("wrong")
                    time.sleep(1)
                    show_problem(answer_number, game_count, level, fake_number)

        if count == game_count:
            WINDOW.fill(BLACK)

            if game_count == max_questions:
                none = font.render("Clear", True, WHITE)
                WINDOW.blit(none, (250, 100))
                pygame.display.update()
                time.sleep(0.5)
                play_sound("success")
                time.sleep(2)
                return 1

            text_ok = font.render("OK", True, WHITE)
            t1 = time.time()
            WINDOW.blit(text_ok, (250, 100))
            pygame.display.update()
            time.sleep(2)

            game_count += 1
            count = 0
            show_problem(answer_number, game_count, level, fake_number)

        draw_button(level)

        pygame.display.update()
        CLOCK.tick(FPS)


def draw_button(level: GameLevel):
    num = 4 + level.value

    for i in range(num):
        BUTTONS[i].draw()
    if level.value == 3:
        BUTTONS[7].draw()
        WINDOW.blit(TEXT_ELEMENT[7], (470, 330))
    return

def show_problem(answer_number, count, level: GameLevel, fake_num):
    tim = 0
    isShowed = False
    WINDOW.fill(BLACK)

    pygame.display.update()

    while tim < count:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if isShowed:
            WINDOW.fill(BLACK)
            pygame.display.update()
            isShowed = False
            tim += 1
        else:
            pygame.draw.rect(WINDOW, COLOR_ALL[answer_number[tim]], (100, 50, 400, 300))
            if level.value == 3:
                pygame.draw.rect(WINDOW, COLOR_ALL[fake_num[tim]], (100, 50, 400, 300))

            pygame.draw.rect(WINDOW, (0,0,0), (100, 50, 400, 300),5)

            WINDOW.blit(TEXT_ELEMENT[answer_number[tim]], (230, 175))
            pygame.display.update()
            isShowed = True

        CLOCK.tick(FPS)

        if level.value == 3:
            time.sleep(0.15)
        else:
            time.sleep(0.2)


def check_color(x: int, y: int, level: GameLevel):
    num = 4 + level.value
    if level.value == 3:
        num += 1
    for i in range(num):
        is_color = BUTTONS[i].is_clicked(x,y)
        if is_color == 1:
            return i
    return None

def play_sound(name):
    if name in sounds:
        sounds[name].play()
    else:
        print(f"Sound '{name}' not found")


if __name__ == '__main__':
    main()
