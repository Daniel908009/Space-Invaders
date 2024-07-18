# necessary imports
import pygame
import time
import tkinter
import threading

# function to reset the game
def reset():
    global enemy_x, enemy_y, enemy_x_change, player_x, player_y, player_x_change, bullet_x, bullet_y, score, lives, enemy_y_change
    enemy_x = []
    enemy_y = []
    enemy_x_change = []
    for i in range(num_of_enemies):
        enemy_x_change.append(1)
    enemy_y_change = 0
    create_enemies()
    player_x = screen_width // 2 - space_ship.get_width() // 2
    player_y = screen_height - space_ship.get_height()
    player_x_change = 0
    bullet_x = []
    bullet_y = []
    score = 0
    lives = 3

# function to fire a bullet
def fire_bullet(x, y):
    bullet_x.append(x+space_ship.get_width()/2-bullet.get_width()/2)
    bullet_y.append(y)

# function to apply the settings
def apply_settings(mode, difficulty, resizability, num_of_enemiesf, livesf, fire_ratef):
    global num_of_enemies, mode_active, difficulty_active, screen_width, screen_height, lives, fire_rate
    if int(num_of_enemiesf.get()) > 0:
        num_of_enemies = int(num_of_enemiesf.get())
    else:
        return
    if int(livesf.get()) > 0:
        lives = int(livesf.get())
    else:
        return
    if float(fire_ratef.get()) >= 0:
        fire_rate = float(fire_ratef.get())
    if resizability.get():
        global screen, mode_active, difficulty_active
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    else:
        screen = pygame.display.set_mode((screen_width, screen_height))
    if mode.get() == "One wave":
        mode_active = "One wave"
    elif mode.get() == "Endless":
        mode_active = "Endless"
    if difficulty.get() == "Easy":
        difficulty_active = "Easy"
    elif difficulty.get() == "Scalable":
        difficulty_active = "Scalable"
    elif difficulty.get() == "Impossible":
        difficulty_active = "Impossible"
    reset()

# function to create a settings window
def settings_window():
    window = tkinter.Tk()
    window.title("Settings")
    window.geometry("550x300")
    window.resizable(False, False)
    window.iconbitmap("settings.ico")
    # creating a frame for the settings
    frame = tkinter.Frame(window)
    frame.pack()
    # creating a label for the mode setting
    mode_label = tkinter.Label(frame, text="Mode:")
    mode_label.grid(row=0, column=0)
    # creating a option menu for the mode setting
    mode_options = ["One wave", "Endless"]
    mode_var = tkinter.StringVar(window)
    mode_var.set(mode_active)
    mode_option_menu = tkinter.OptionMenu(frame, mode_var, *mode_options)
    mode_option_menu.grid(row=0, column=1)
    # creating a label for the difficulty setting
    difficulty_label = tkinter.Label(frame, text="Difficulty:")
    difficulty_label.grid(row=1, column=0)
    # creating a option menu for the difficulty setting
    difficulty_options = ["Easy", "Scalable", "Impossible"]
    difficulty_var = tkinter.StringVar(window)
    difficulty_var.set(difficulty_active)
    difficulty_option_menu = tkinter.OptionMenu(frame, difficulty_var, *difficulty_options)
    difficulty_option_menu.grid(row=1, column=1)
    # creating a label for the resizability setting
    resizability_label = tkinter.Label(frame, text="Resizability:")
    resizability_label.grid(row=2, column=0)
    # creating a check button for the resizability setting
    resizability_var = tkinter.IntVar()
    resizability_check_button = tkinter.Checkbutton(frame, variable=resizability_var)
    resizability_check_button.grid(row=2, column=1)
    # creating a label for the number of enemies setting
    num_of_enemies_label = tkinter.Label(frame, text="Number of enemies:")
    num_of_enemies_label.grid(row=3, column=0)
    # creating a entry for the number of enemies setting
    num_of_enemies_var = tkinter.StringVar()
    num_of_enemies_var.set(str(num_of_enemies))
    num_of_enemies_entry = tkinter.Entry(frame, textvariable=num_of_enemies_var)
    num_of_enemies_entry.grid(row=3, column=1)
    # creating a label for instructions
    instructions_label = tkinter.Label(frame, text="*More is recommended for one wave mode")
    instructions_label.grid(row=4, column=0, columnspan=2)
    # creating a label for lives setting
    lives_label = tkinter.Label(frame, text="Number of lives:")
    lives_label.grid(row=5, column=0)
    # creating a entry for the number of lives setting
    lives_var = tkinter.StringVar()
    lives_var.set(str(lives))
    lives_entry = tkinter.Entry(frame, textvariable=lives_var)
    lives_entry.grid(row=5, column=1)
    # creating a label for instructions
    instructions_label = tkinter.Label(frame, text="*More is recommended for harder difficulties")
    instructions_label.grid(row=6, column=0, columnspan=2)
    # creating a label for the fire rate setting
    fire_rate_label = tkinter.Label(frame, text="Fire rate:")
    fire_rate_label.grid(row=7, column=0)
    # creating a entry for the fire rate setting
    fire_rate_var = tkinter.StringVar()
    fire_rate_var.set(str(fire_rate))
    fire_rate_entry = tkinter.Entry(frame, textvariable=fire_rate_var)
    fire_rate_entry.grid(row=7, column=1)
    # creating apply button
    apply_button = tkinter.Button(window, text="Apply", command=lambda:apply_settings(mode_var, difficulty_var, resizability_var, num_of_enemies_var, lives_var, fire_rate_var))
    apply_button.pack()
    window.mainloop()

# function to create enemies
def create_enemies():
    global enemy_x, enemy_y, num_of_enemies, screen_width
    possitions = screen_width // num_of_enemies
    for i in range(num_of_enemies):
        enemy_x.append(possitions*i)
        enemy_y.append(50)

# function to create a single enemy, used when an enemy is killed
def create_enemy():
    global enemy_x, enemy_y, enemy_x_change, base_speed
    enemy_x.append(0)
    enemy_y.append(50)
    enemy_x_change.append(base_speed)
    if difficulty_active == "Scalable":
        for i in range(len(enemy_x_change)):
            if enemy_x_change[i] > 0:
                enemy_x_change[i] = base_speed * 1.01
            else:
                enemy_x_change[i] = base_speed * -1.01
        base_speed = base_speed * 1.01

    elif difficulty_active == "Impossible":
        for i in range(len(enemy_x_change)):
            if enemy_x_change[i] > 0:
                enemy_x_change[i] = base_speed * 1.1
            else:
                enemy_x_change[i] = base_speed * -1.1
        base_speed = base_speed * 1.1
    else:
        for i in range(len(enemy_x_change)):
            if enemy_x_change[i] > 0:
                enemy_x_change[i] = base_speed
            else:
                enemy_x_change[i] = base_speed * -1

# function to create the game over screen
def game_over_screen():
    global running, player_x_change, bullet_y_change, enemy_x_change
    # stopping everything
    player_x_change = 0
    bullet_y_change = 0
    for i in range(len(enemy_x_change)):
        enemy_x_change[i] = 0

    # game over screen loop
    while running:
        screen.fill((0, 0, 0))
        font = pygame.font.Font("freesansbold.ttf", 64)
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, (200, 250))
        # displaying final score
        final_score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(final_score_text, (300, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset()

# function to determine whether player can fire a bullet or not
def bullet_state():
    global bullet_a, fire_rate
    while running:
        if bullet_a == False:
            time.sleep(fire_rate)
            bullet_a = True
        time.sleep(0.01)

# function to spawn enemies in one wave mode, this is different from endless because in this mode enemies spawn with a delay in between them (if that makes sense)
# this function is not yet implemented
def one_wave_spawn():
    one_way_enemies_created = False
    all_enemies_moving = False
    global enemy_x_change
    # setting the speeds of all the enemies to 0, they will not move until they will be activated
    for i in range(len(enemy_x_change)):
        enemy_x_change[i] = 0
    while running:
        if mode_active == "One wave":
            global enemy_x, enemy_y, num_of_enemies
            if one_way_enemies_created == False:
                # creating enemies outside of the screen
                for i in range(num_of_enemies):
                    enemy_x.append(0)
                    enemy_y.append(50)
                one_way_enemies_created = True
            if all_enemies_moving == False:
                # starting the movement of the enemies one by one with a delay
                for i in range(num_of_enemies):
                    enemy_x[i] += base_speed
                    time.sleep(1)
                all_enemies_moving = True
        else:
            time.sleep(1)

# Initialize the game
pygame.init()

# screen variables
screen_width = 800
screen_height = 600

# setting up the screen
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(pygame.image.load("icon.png"))
screen = pygame.display.set_mode((screen_width, screen_height))

# variables
running = True
score = 0
lives = 3

# enemy variables
num_of_enemies = 5
enemy_x = []
enemy_y = []
enemy_x_change = []
base_speed = 1
for i in range(num_of_enemies):
    enemy_x_change.append(base_speed)
enemy_y_change = 0
enemy_ship = pygame.image.load("UFO.png")
create_enemies()

# player variables
space_ship = pygame.image.load("spaceship.png")
player_x = screen_width // 2 - space_ship.get_width() // 2
player_y = screen_height - space_ship.get_height()
player_x_change = 0
mode_active = "Endless"
difficulty_active = "Easy"
fire_rate = 0.5

# bullet variables
bullet_x = []
bullet_y = []
bullet_a = True
bullet_y_change = 1
bullet = pygame.image.load("triangle.png")

# settings button
settings = pygame.image.load("settings.png")
settings_active = False

                # setting up the threads
# thread to determine whether player can fire a bullet or not
fire_bullet_thread = threading.Thread(target=bullet_state)
fire_bullet_thread.start()
# thread for the one wave mode
one_wave_thread = threading.Thread(target=one_wave_spawn)

# main loop
while running:
    
    # setting up the spawn of enemies if the mode is one wave
    if mode_active == "One wave" and one_wave_thread.is_alive() == False:
        one_wave_thread.start()

    # setting up the background
    screen.fill((0, 0, 0))

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
                if bullet_a:
                    fire_bullet(player_x, player_y)
                    bullet_a = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if event.pos[0] >= 0 and event.pos[0] <= settings.get_width() and event.pos[1] >= 600-settings.get_height() and event.pos[1] <= 600:
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
            enemy_x_change[i] = base_speed
            enemy_y[i] += enemy_ship.get_height()
            if enemy_y[i] >= screen_height-space_ship.get_height():
                lives -= 1
                enemy_y[i] = 50
                enemy_x[i] = 0
                if lives == 0:
                    # game over screen
                    game_over_screen()
        elif enemy_x[i] >= screen_width - enemy_ship.get_width():
            enemy_x_change[i] = base_speed * -1
            enemy_y[i] += enemy_ship.get_height()
            if enemy_y[i] >= screen_height-space_ship.get_height():
                lives -= 1
                enemy_y[i] = 50
                enemy_x[i] = 0
                if lives == 0:
                    # game over screen
                    game_over_screen()

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
    elif player_x >= screen_width - space_ship.get_width():
        player_x = screen_width - space_ship.get_width()

    # checking collision between bullet and enemy
    for i in range(len(bullet_x)):
        for j in range(len(enemy_x)):
            try:
                if bullet_x[i] >= enemy_x[j] and bullet_x[i] <= enemy_x[j] + enemy_ship.get_width() and bullet_y[i] >= enemy_y[j] and bullet_y[i] <= enemy_y[j] + enemy_ship.get_height():
                    score += 1
                    bullet_x.pop(i)
                    bullet_y.pop(i)
                    enemy_x.pop(j)
                    enemy_y.pop(j)
                    enemy_x_change.pop(j)
                    if mode_active == "One wave":
                        pass
                    elif mode_active == "Endless":
                        create_enemy()
                    break
            except:
                pass

    # update the screen
    pygame.display.update()

pygame.quit()