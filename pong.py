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

# Screen
pygame.display.set_caption("Pong")
screen = pygame.display.set_mode((800, 480), 0, 32)
width, height = pygame.display.get_surface().get_size()
screen.fill((0,0,0))

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

def update():
    global running
    global SPEED

    pygame.event.pump()
    ISDOWN = pygame.key.get_pressed()

    player1.y = player1.y + (BOOL[ISDOWN[pygame.K_a]] - BOOL[ISDOWN[pygame.K_q]]) * 7
    player2.y = player2.y + (BOOL[ISDOWN[pygame.K_DOWN]] - BOOL[ISDOWN[pygame.K_UP]]) * 7

    if player1.y < 100: player1.y = 100
    if player1.y > (height - 60): player1.y = height - 60
    if player2.y < 100: player2.y = 100
    if player2.y >  (height - 60): player2.y = height - 60

    ball.x = ball.x + ball.vx
    ball.y = ball.y + ball.vy

    if abs(ball.y) >= (height - 20): ball.vy = -ball.vy
    if abs(ball.y) <= 60: ball.vy = -ball.vy

    if ball.x < 40 and ball.x > 30 and abs(player1.y - ball.y) < 60:
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
	
    if ball.x > (width - 40) and ball.x < (width - 30) and abs(player2.y - ball.y) < 60:
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

    if player1.score > 6 or player2.score > 6:
        pass
		#print("player " .. (score1 > score2 and 1 or 2) .. " wins.")

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

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
    screen.blit(instructions2, (width - score2.get_size()[0] - 20 - instructions2.get_size()[0], 18))


running = True
while running:
    screen.fill((0,0,0))
    update()
    draw()
    clock.tick(60)
    pygame.display.flip()

pygame.quit()