#Star Wars by @rafaelborri

#pygame
import pygame

#Sounds initalizating
pygame.mixer.init()

#Fond initalization
pygame.font.init()


#Window wariables
WIDTH = 900
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
BG = pygame.image.load("space.PNG")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
WINDOW = pygame.display.set_mode(SIZE)
pygame.display.set_caption("STAR WARS by @rafaelborri")

RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#Speed
FPS = 60
VEL = 5

#Space ships wariables
SPACESHIP_WIDTH = 80
SPACESHIP_HEIGHT = 60

#Bullet wariables
BULLET_VEL = 15
MAX_BULLET_YELLOW = 1
MAX_BULLET_RED = 1

#Font for health
HEALTH_FONT = pygame.font.SysFont("arial", 40)

#Font of win
WIN_FONT = pygame.font.SysFont("arial", 100)

#Sound of bullet
BULLET_SOUND = pygame.mixer.Sound("laser.wav")

#Sound of hitting rocket
HITTING_SOUND = pygame.mixer.Sound("explosion.wav")

#Yellow spaceship settings
YELLOW_SPACESHIP_IMAGE = pygame.image.load("spaceship_yellow.png")
yellow_spaceship = pygame.transform.rotate(YELLOW_SPACESHIP_IMAGE, 270)
yellow_spaceship = pygame.transform.scale(yellow_spaceship, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

#Red spaceship settings
RED_SPACESHIP_IMAGE = pygame.image.load("spaceship_red.png")
red_spaceship = pygame.transform.rotate(RED_SPACESHIP_IMAGE, 90)
red_spaceship = pygame.transform.scale(red_spaceship, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

#Split line
SPLIT = pygame.Rect(WIDTH / 2 - 5, 0, 10, HEIGHT)

#Yellow spaceship control
def yellow_control(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x > 0:
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x < WIDTH / 2 - SPACESHIP_WIDTH:
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y > 0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y < HEIGHT - SPACESHIP_HEIGHT:
        yellow.y += VEL

#Red spaceship control
def red_control(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x > WIDTH / 2:
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x < WIDTH - SPACESHIP_WIDTH:
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y < HEIGHT - SPACESHIP_HEIGHT:
        red.y += VEL



#Handeling bullets
def handle_bullets(bullets_yellow, bullets_red, yellow, red, health_yellow, health_red):
    for bullet in bullets_yellow:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            bullets_yellow.remove(bullet)
            pygame.event.post(pygame.event.Event(RED_HIT))
            HITTING_SOUND.play()
        elif bullet.x > WIDTH:
            bullets_yellow.remove(bullet)

    for bullet in bullets_red:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            bullets_red.remove(bullet)
            health_yellow -= 1
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            HITTING_SOUND.play()
        elif bullet.x < 0:
            bullets_red.remove(bullet)

#Drawing winner text
def drawWiner(text, color):
    win_text = WIN_FONT.render(text, True, color)
    WINDOW.blit(win_text, (WIDTH - WIDTH/2 - win_text.get_width()/2, HEIGHT - HEIGHT/2 - win_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

#Setting the window every frame
def drawWindow(yellow, red, bullets_yellow, bullets_red, health_yellow, health_red):
    WINDOW.blit(BG, (0, 0))

    health_text_yellow = HEALTH_FONT.render("HEALTH: " + str(health_yellow), True, WHITE)
    health_text_red  = HEALTH_FONT.render("HEALTH: " + str(health_red), True, WHITE)
    WINDOW.blit(health_text_yellow, (10, 10))
    WINDOW.blit(health_text_red, (WIDTH - health_text_red.get_width() - 10, 10))
    WINDOW.blit(yellow_spaceship, (yellow.x, yellow.y))
    WINDOW.blit(red_spaceship, (red.x, red.y))
    pygame.draw.rect(WINDOW, BLACK, SPLIT)

    for bullet in bullets_yellow:
        pygame.draw.rect(WINDOW, YELLOW, bullet)
    for bullet in bullets_red:
        pygame.draw.rect(WINDOW, RED, bullet)

    pygame.display.update()

#main
def main():
    yellow = pygame.Rect(WIDTH / 4 - SPACESHIP_WIDTH / 2, HEIGHT / 2 - SPACESHIP_HEIGHT / 2, SPACESHIP_WIDTH,
                         SPACESHIP_HEIGHT)
    red = pygame.Rect((WIDTH / 4) * 3 - SPACESHIP_WIDTH / 2, HEIGHT / 2 - SPACESHIP_HEIGHT / 2, SPACESHIP_WIDTH,
                      SPACESHIP_HEIGHT)

    bullets_yellow = []
    bullets_red = []

    health_yellow = 10
    health_red = 10

    win_text = ""
    win_color = (0, 0, 0)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == RED_HIT:
                health_red -= 1
            elif event.type == YELLOW_HIT:
                health_yellow -= 1
        keys_pressed = pygame.key.get_pressed()


        if keys_pressed[pygame.K_LSHIFT] and len(bullets_yellow) < MAX_BULLET_YELLOW:
            bullet = pygame.Rect(yellow.x + SPACESHIP_WIDTH, yellow.y.real + SPACESHIP_HEIGHT//2, 10, 5)
            bullets_yellow.append(bullet)
            BULLET_SOUND.play()
        max_bullet_yellow = 100
        if keys_pressed[pygame.K_q] and keys_pressed[pygame.K_e] and len(bullets_yellow) < max_bullet_yellow:
                bullet = pygame.Rect(yellow.x + SPACESHIP_WIDTH, yellow.y.real + SPACESHIP_HEIGHT // 2, 10, 5)
                bullets_yellow.append(bullet)
                BULLET_SOUND.play()
        if keys_pressed[pygame.K_RSHIFT] and len(bullets_red) < MAX_BULLET_RED:
            bullet = pygame.Rect(red.x - SPACESHIP_WIDTH, red.y + SPACESHIP_HEIGHT//2, 10, 5)
            bullets_red.append(bullet)
            BULLET_SOUND.play()
        max_yellow_bullets = 100
        if keys_pressed[pygame.K_m] and keys_pressed[pygame.K_n] and len(bullets_red) < max_yellow_bullets:
            bullet = pygame.Rect(red.x - SPACESHIP_WIDTH, red.y + SPACESHIP_HEIGHT//2, 10, 5)
            bullets_red.append(bullet)
            BULLET_SOUND.play()




        if health_yellow < 1 or health_red < 1:
            if health_yellow < 1:
                win_text = "Red Wins!"
                win_color = RED
            else:
                win_text = "Yellow Wins! "
                win_color = YELLOW
            drawWiner(win_text, win_color)
            break

        handle_bullets(bullets_yellow, bullets_red, yellow, red, health_yellow, health_red)
        yellow_control(keys_pressed, yellow)
        red_control(keys_pressed, red)
        drawWindow(yellow, red, bullets_yellow, bullets_red, health_yellow, health_red)
    pygame.quit()

#chacking if you can run it
if __name__ == "__main__":
    main()
