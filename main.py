# necessary imports
import pygame
import random
import time
import tkinter

# function to reset the game
def reset():
    pass

# function to fire a bullet
def fire_bullet(x, y):
    bullet_x.append(x)
    bullet_y.append(y)

# function to apply the settings
def apply_settings():
    global settings_active
    settings_active = False

# function to create a settings window
def settings_window():
    global settings_active
    if settings_active:
        try:
            window.destroy()
        except:
            pass
        return
    else:
        settings_active = True
        window = tkinter.Tk()
        window.title("Settings")
        window.geometry("300x300")
        window.resizable(False, False)
        # creting apply button
        apply_button = tkinter.Button(window, text="Apply", command=apply_settings)
        apply_button.pack()
        window.mainloop()

# function to create enemies
def create_enemies():
    possitions = [0, 150, 300, 450, 600, 750]
    for i in range(num_of_enemies):
        enemy_x.append(possitions[i])
        enemy_y.append(50)

# Initialize the game
pygame.init()

# setting up the screen
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(pygame.image.load("icon.png"))
screen = pygame.display.set_mode((800, 600))

# variables
running = True
score = 0
lives = 3

# enemy variables
num_of_enemies = 6
enemy_x = []
enemy_y = []
enemy_x_change = []
for i in range(num_of_enemies):
    enemy_x_change.append(1)
enemy_y_change = 0
enemy_ship = pygame.image.load("UFO.png")
create_enemies()

# player variables
player_x = 370
player_y = 480
space_ship = pygame.image.load("spaceship.png")
player_x_change = 0

# bullet variables
bullet_x = []
bullet_y = []
bullet_y_change = 1
bullet = pygame.image.load("triangle.png")

# settings button
settings = pygame.image.load("settings.png")
settings_active = False

# main loop
while running:

    # setting up the background
    screen.fill((0, 0, 0))

    # if settings window is active
    #while settings_active:
        # event loop
     #   for event in pygame.event.get():
      #      if event.type == pygame.QUIT:
       #         running = False
        #        settings_active = False
        #pygame.display.update()

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset()
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                player_x_change = -1
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player_x_change = 1
            if event.key == pygame.K_SPACE:
                fire_bullet(player_x, player_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if event.pos[0] >= 0 and event.pos[0] <= settings.get_width() and event.pos[1] >= 600-settings.get_height() and event.pos[1] <= 600:
                    print("Settings button clicked")
                    settings_window()

    # placing the player
    screen.blit(space_ship, (player_x, player_y))

    # placing the bullets
    for i in range(len(bullet_x)):
        screen.blit(bullet, (bullet_x[i], bullet_y[i]))
        bullet_y[i] -= bullet_y_change
        # removing bullets, if they go out of the screen
        if bullet_y[i] <= 0:
            bullet_x.pop(i)
            bullet_y.pop(i)
            break
    
    # placing the enemies
    for i in range(len(enemy_x)):
        screen.blit(enemy_ship, (enemy_x[i], enemy_y[i]))
        enemy_x[i] = enemy_x[i] + enemy_x_change[i]
        # moving the enemies down, if they reach the boundary
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 1
            enemy_y[i] += enemy_ship.get_height()
        elif enemy_x[i] >= 800 - enemy_ship.get_width():
            enemy_x_change[i] = -1
            enemy_y[i] += enemy_ship.get_height()

    # placing the score and lives on the screen
    font = pygame.font.Font("freesansbold.ttf", 32)
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    lives_text = font.render("Lives: " + str(lives), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (600, 10))

    # placing the settings button
    screen.blit(settings, (0, 600-settings.get_height()))

    # moving the player
    player_x += player_x_change

    # checking space ship boundaries
    if player_x <= 0:
        player_x = 0
    elif player_x >= 800 - space_ship.get_width():
        player_x = 800 - space_ship.get_width()

    # update the screen
    pygame.display.update()

pygame.quit()