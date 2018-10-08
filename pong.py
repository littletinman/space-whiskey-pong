# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from random import randint

# Initialize Pygame
pygame.init()
pygame.font.init()
fontLG = pygame.font.SysFont('Arial', 30)
fontSM = pygame.font.SysFont('Arial', 16)
clock = pygame.time.Clock()

# Globals
WHITE = (255, 255, 255)
ISDOWN = pygame.key.get_pressed()
BOOL = {True: 1, False: 0}
SPEED = 3
GAME_LIMIT = 5
PLAYER_WON = None
REMATCH_TIMER = 10
RUNNING = True

# Screen
pygame.display.set_caption("Pong")
screen = pygame.display.set_mode((800, 480), 0, 32)
width, height = pygame.display.get_surface().get_size()
screen.fill((0, 0, 0))


# Objects
class Ball:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy


class Player:
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score


ball = Ball(width/2, height/2, -SPEED, SPEED)
player1 = Player(10, height/2, 0)
player2 = Player(width - 30, height/2, 0)


def initial_game_state(
        white=(255, 255, 255),
        is_down=pygame.key.get_pressed(),
        bool_value={True: 1, False: 0}, speed=3,
        game_limit=5, player_won=None, rematch_timer=10, running=True):
    global WHITE
    global ISDOWN
    global BOOL
    global SPEED
    global GAME_LIMIT
    global PLAYER_WON
    global REMATCH_TIMER
    global RUNNING
    global ball
    global player1
    global player2

    WHITE = white
    ISDOWN = is_down
    BOOL = bool_value
    SPEED = speed
    GAME_LIMIT = game_limit
    PLAYER_WON = player_won
    REMATCH_TIMER = rematch_timer
    RUNNING = running
    ball = Ball(width/2, height/2, -SPEED, SPEED)
    player1 = Player(10, height/2, 0)
    player2 = Player(width - 30, height/2, 0)


def update():
    global RUNNING
    global SPEED
    global PLAYER_WON

    pygame.event.pump()
    ISDOWN = pygame.key.get_pressed()

    if player1.score == GAME_LIMIT:
        RUNNING = False
        PLAYER_WON = 1
        return
    elif player2.score == GAME_LIMIT:
        RUNNING = False
        PLAYER_WON = 2
        return

    player1.y = player1.y + \
        (BOOL[ISDOWN[pygame.K_a]] - BOOL[ISDOWN[pygame.K_q]]) * 7
    player2.y = player2.y + \
        (BOOL[ISDOWN[pygame.K_DOWN]] - BOOL[ISDOWN[pygame.K_UP]]) * 7

    if player1.y < 100:
        player1.y = 100
    if player1.y > (height - 60):
        player1.y = height - 60
    if player2.y < 100:
        player2.y = 100
    if player2.y > (height - 60):
        player2.y = height - 60

    ball.x = ball.x + ball.vx
    ball.y = ball.y + ball.vy

    if abs(ball.y) >= (height - 20):
        ball.vy = -ball.vy
    if abs(ball.y) <= 60:
        ball.vy = -ball.vy

    if ball.x < 40 and ball.x > 20 and abs(player1.y - ball.y) < 60:
        SPEED = SPEED + 0.2
        ball.x = 40
        ball.vx = SPEED
        ball.vy = ball.vy * 0.5 + randint(-10, 10) / 20 * SPEED

    if ball.x < -10:
        ball.x = width/3 * 2
        ball.y = height/2
        SPEED = 3
        ball.vx = -SPEED
        ball.vy = -SPEED
        player2.score = player2.score + 1

    if ball.x > (width - 40) and ball.x < (width - 20) and abs(player2.y - ball.y) < 60:
        SPEED = SPEED + 0.5
        ball.x = (width - 40)
        ball.vx = -SPEED
        ball.vy = ball.vy * 0.8 + randint(-10, 10) / 10 * SPEED

    if ball.x > width + 10:
        ball.x = width/3
        ball.y = height/2
        SPEED = 3
        ball.vx = SPEED
        ball.vy = SPEED
        player1.score = player1.score + 1

    for event in pygame.event.get():
        if event.type == QUIT:
            RUNNING = False


def draw():
    title = fontLG.render("PONG", False, WHITE)
    screen.blit(title, (width/2 - title.get_size()[0]/2, 10))

    pygame.draw.rect(screen, WHITE, [player1.x, player1.y - 50, 20, 100])
    pygame.draw.rect(screen, WHITE, [player2.x, player2.y - 50, 20, 100])

    pygame.draw.circle(screen, WHITE, [int(ball.x), int(ball.y)], 10)

    score1 = fontLG.render(str(player1.score), False, WHITE)
    screen.blit(score1, (10, 10))
    instructions1 = fontSM.render("P1 Keys: Q and A", False, WHITE)
    screen.blit(instructions1, (score1.get_size()[0] + 20, 18))

    score2 = fontLG.render(str(player2.score), False, WHITE)
    screen.blit(score2, (width - score2.get_size()[0] - 10, 10))
    instructions2 = fontSM.render("P2 Keys: UP and DOWN", False, WHITE)
    screen.blit(instructions2, (width - score2.get_size()
                                [0] - 20 - instructions2.get_size()[0], 18))


def drawGameEnd():
    screen.fill((0, 0, 0))
    title = fontLG.render("Player {0} won!".format(PLAYER_WON), False, WHITE)
    screen.blit(title, (width/2 - title.get_size()[0]/2, height/4))
    message = fontSM.render("Up for a rematch? (y / n)", False, WHITE)
    screen.blit(message, (width/2 - message.get_size()[0]/2, height/2))
    message = fontSM.render("({0})".format(REMATCH_TIMER), False, WHITE)
    screen.blit(message, (width/2 - message.get_size()[0]/2, 3*height/4))
    pygame.display.flip()


def main():
    global RUNNING
    initial_game_state()
    while RUNNING:
        print("Game running")
        screen.fill((0, 0, 0))
        update()
        draw()
        clock.tick(60)
        pygame.display.flip()
    if not game_end():
        print("Game restarted")
        main()


def game_end():
    global REMATCH_TIMER
    result = True
    while True:
        # Retry or not
        events = pygame.event.get()
        selected = None
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    print("Yes pressed!")
                    selected = "y"
                    break
                elif event.key == pygame.K_n:
                    selected = "n"
                    break
        # Has the timer ended?
        if REMATCH_TIMER <= 0:
            result = True
            break
        # Check selected
        if selected == "y":
            result = False
            break
        elif selected == "n":
            result = True
            break
        # Keeps counting down
        REMATCH_TIMER -= 1
        drawGameEnd()
        pygame.time.wait(1000)
    return result


if RUNNING:
    main()

pygame.quit()
