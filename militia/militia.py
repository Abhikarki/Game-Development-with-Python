import pygame
import math
import random

# Initialize all imported pygame modules.
pygame.init()

#  Create a visible image surface on the monitor.
screen = pygame.display.set_mode((800,600))

# Set caption and icon.
pygame.display.set_caption("militia")
# Icons made by <href="https://www.flaticon.com/authors/eucalyp" title="Eucalyp">
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# player image.
playerImg = pygame.image.load('player.png')
# Initial position of the player.
playerX = 0
playerY = 270
playerX_change = 0
playerY_change = 0

# list of enemies.
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):    
    #Icons made by <href="https://www.flaticon.com/authors/ultimatearm">
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(125,350))
    enemyY.append(random.randint(0,535))
    enemyX_change.append(40)
    enemyY_change.append(0.3)

# Bullet
# Icons made by <href="https://www.flaticon.com/authors/freepik" title="Freepik">
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 320
bulletY_change = 0
bulletX_change = 2
bullet_state = "ready"

scoreValue = 0
font = pygame.font.Font('freesansbold.ttf', 32)

# For the position of the score on the screen.
textX = 620
textY = 560

space = pygame.font.Font('freesansbold.ttf', 16)

over_font = pygame.font.Font('freesansbold.ttf', 64)

# To display the updated score on the screen.
def show_score(x, y):
    score = font.render("Score: " + str(scoreValue), True, (255,255,255))
    screen.blit(score, (x, y))

# For instruction to fire the bullet.
def show_Instructions():
    instruct = space.render("Press 'space' to shoot", True, (255, 255, 255))
    screen.blit(instruct, (330, 8))    

# To display "GAME OVER" if any enemy crosses the screen.
def game_over_text():
    over = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (180, 205))

# To update the position of the player.
def player(x, y):
    screen.blit(playerImg, (x, y))

# To update the position of the enemies.
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# To update the position of the bullet once it's fired.
def fireBullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 16))

# Check for the collision of bullet and enemy.
def isCollision(enemyX, enemyY, bulletX, bulletY):
    # Calculate distance between bullet and enemy.
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    # Return True if there is a collision(estimated collision at a distance 27)
    if distance < 27:
        return True
    else:
        return False  

running = True
while running:
    # Fills the Surface object, our screen, with the colour black.
    screen.fill((0,0,0)) 
    
    # Pygame will register all events from the user into an event queue which can be received with pygame.event.get()
    for event in pygame.event.get():
        # when the user clicks the window's "X" button
        if event.type == pygame.QUIT:
            running = False
        
        # To detect if a key is physically pressed down. 
        if event.type == pygame.KEYDOWN:
            # Check if the upward arrow key is pressed.
            if event.key == pygame.K_UP:
                playerY_change = -0.9
            # Check if the downward arrow key is pressed.    
            if event.key == pygame.K_DOWN:
                playerY_change = 0.9
            # Check if the space is pressed.    
            if event.key == pygame.K_SPACE:
                # If the space is pressed, check whether the bullet is in fired condition or not.
                if bullet_state == "ready":
                    bulletY = playerY
                    fireBullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # Change the vertical position of the player as per the arrow key pressed.
    playerY += playerY_change

    # Set boundaries to the movement of the player
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # Set boundaries to the movement of enemies.
    for i in range(num_of_enemies):
        # Check if the enemy is on the screen
        # If any enemy crosses the screen, GAME OVER.
        if enemyX[i] >= 795:
            for j in range(num_of_enemies):
                # Remove all enemies from the visible screen.
                enemyX[j] = 2000
            game_over_text()
            break    
        
        # Change the vertical position of the enemies.
        enemyY[i] += enemyY_change[i]

        # Keep the enemies within the screen.
        if enemyY[i] <= 0:
            enemyY_change[i] = 0.3
            enemyX[i] += enemyX_change[i]
        elif enemyY[i] >= 536:
            enemyY_change[i] = -0.3
            enemyX[i] += enemyX_change[i]
    
        # Check for the collision of bullet and the enemy.
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletX = 0
            # Return the bullet to original(ready) position if an enemy is hit.
            bullet_state = "ready"
            # Increase the score by 1.    
            scoreValue += 1
            # Respawn the enemies at random position within the boundaries.
            enemyX[i] = random.randint(125, 350)
            enemyY[i] = random.randint(0,535)
        
        # call enemy function to draw the enemy on the screen.
        enemy(enemyX[i], enemyY[i], i)       

    # Return the bullet to original(ready) position 
    if bulletX >= 800:
        bulletX = 0
        bullet_state = "ready"

    # If bullet is in fired state, keep updating its position on the screen with fireBullet function.
    if bullet_state == "fire":
        fireBullet(bulletX, bulletY)
        bulletX += bulletX_change

    # Update the player's position by calling player function.
    player(playerX, playerY)

    # Show the updated score on the screen.
    show_score(textX, textY)
    # Show the instruction to shoot.
    show_Instructions()
    pygame.display.update()        
     
