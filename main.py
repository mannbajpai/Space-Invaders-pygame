from tkinter import font
import pygame
from pygame import mixer
import random
import math

#initialize pygame
pygame.init()

# Create Screen
screen = pygame.display.set_mode((800,600))

# Background Image
bgImg = pygame.image.load('images\game-background.jpg')

# Background Music
mixer.music.load('sounds\\background.wav')
mixer.music.play(-1)

# Title & Icon
icon =  pygame.image.load('images\logo.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Space Invaders")

# Player
playerImg = pygame.image.load('images\\battleship.png')
playerX = 368
playerY = 520
playerX_change = 0
playerY_change = 0

# Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('images/ufo.png'))
    enemyX.append( random.randint(0,735) )
    enemyY.append( random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(10)

# Bullet
bulletImg = pygame.image.load('images\\bullet (1).png')
bulletX = 0
bulletY = playerY
bulletY_change = 2
bullet_state = 'ready'

# Score
score_value = 0
high_score = 0
font = pygame.font.Font('fonts\\broken-console-broken-console-regular-400.ttf', 25)
scoreX = 15
scoreY = 15
hscoreX = 15
hscoreY = 40

# Game Over
over_font = pygame.font.Font('fonts\\broken-console-broken-console-bold-700.ttf', 60)

def game_over_text():
    over = over_font.render("Game Over!!!", True, (255,0,0))
    # play_ag = font.render("Press ENTER to Play Again...", True, (255,255,255))
    screen.blit(over, (250,250))
    # screen.blit(play_ag, (250,400))


def show_score(Sx,Sy,Hx,Hy):
    score = font.render("Score : "+str(score_value), True, (255,255,255))
    hscore = font.render("High Score : "+str(high_score), True, (255,255,255))
    screen.blit(score, (Sx,Sy))
    screen.blit(hscore, (Hx,Hy))
# Player Function
def player(x,y):
    screen.blit(playerImg, (x,y))

# Enemy Function
def enemy(i,x,y):
    screen.blit(enemyImg[i], (x,y))

# Bullet Fire Function
def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x+16,y-10))

# Bullet Collision
def isCollision(eX,eY,bX,bY):
    distance = math.sqrt((eX - bX)**2 + (eY - bY)**2)
    if distance <= 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(bgImg, (0,0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.6
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.6
            if event.key == pygame.K_UP:
                playerY_change = -0.6
            if event.key == pygame.K_DOWN:
                playerY_change = 0.6
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletX = playerX
                    bullet_sound = mixer.Sound('sounds\laser-shot-silenced.wav')
                    bullet_sound.play()
                    fire_bullet(bulletX, bulletY)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0
    
    # Player Movement
    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
    if playerX >= 735:
        playerX = 735
    if playerY <=450:
        playerY = 450
    if playerY >= 536:
        playerY = 536

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] >= 450:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            high_score = score_value
            game_over_text()
            break

        # Difficulty Based on Your Score
        # if score_value % 10 == 0 and score_value != 0:
        #    enemyX_change[i]+= 0.01


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = abs(enemyX_change[i])
            enemyY[i] += enemyY_change[i]

        if enemyX[i] >= 735:
            enemyX_change[i] = -abs(enemyX_change[i]) 
            enemyY[i] += enemyY_change[i]
        
        # Collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision : 
            collision_sound = mixer.Sound('sounds\explosion.wav')
            collision_sound.play()
            bulletY = playerY
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)

        enemy(i,enemyX[i],enemyY[i])

    # Bullet Fire Movement
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = 'ready'
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX,playerY)
    show_score(scoreX, scoreY, hscoreX, hscoreY)
    pygame.display.update()