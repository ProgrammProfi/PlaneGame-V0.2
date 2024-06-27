import pygame
import player
from math import ceil

# Настройка
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("PlaneGame")
icon = pygame.image.load("img/icon.png")
font = pygame.font.Font("fonts/poppins/Poppins-Black.ttf", 20)
rnw = pygame.image.load("img/BG/runway.png")
aps = pygame.image.load("img/BG/approachsouth.png")
apn = pygame.image.load("img/BG/approachnorth.png")
ebg = pygame.image.load("img/BG/EmpBG.png")
fors = pygame.image.load("img/BG/bgforest.png")
pygame.display.set_icon(icon)

# Переменные
world = ["rw", "an", "fr", "fr", "fr", "fr", "fr", "fr", "fr", "fr", "fr", "fr", "fr", "fr", "fr", "fr", "fr", "fr",
         "fr", "as"]
wi = 0
wi2 = 1
bgc = "rnw"
bgc2 = "apn"

bgx = 0
bgx2 = 1000
GROUND = 615
colorgr = (50, 168, 82)
colorbl = (50, 168, 148)
colorgra = (153, 153, 153)

# Основной цикл
pre = False
pre2 = False
pre3 = False
running = True
while running:

    # Вывод изображений
    screen.blit(ebg, (0, 0))

    if world[wi] == "rw":
        bgc = rnw
    elif world[wi] == "an":
        bgc = apn
    elif world[wi] == "as":
        bgc = aps
    elif world[wi] == "fr":
        bgc = fors
    screen.blit(bgc, (bgx, 0))

    if world[wi2] == "rw":
        bgc2 = rnw
    elif world[wi2] == "an":
        bgc2 = apn
    elif world[wi2] == "as":
        bgc2 = aps
    elif world[wi2] == "fr":
        bgc2 = fors
    screen.blit(bgc2, (bgx2, 0))

    screen.blit(player.Plane.planeim, (100, player.Plane.y))
    speedtxt = font.render(f"Thr: {str(player.Plane.trotl)}%", True, colorgra)
    fspeedtxt = font.render(f"Spd: {str(ceil(player.Plane.speed))}", True, colorgra)
    fueltxt = font.render(f"Fuel: {str(ceil(player.Plane.fuel))}", True, colorgra)
    if player.Plane.engine:
        engt = "ON"
    else:
        engt = "OFF"
    engtxt = font.render(f"Eng: {engt}", True, colorgra)
    flapstxt = font.render(f"Flaps: {str(player.Plane.flaps)}", True, colorgra)
    screen.blit(speedtxt, (890, 2))
    screen.blit(fspeedtxt, (890, 22))
    screen.blit(engtxt, (890, 42))
    screen.blit(fueltxt, (890, 62))
    screen.blit(flapstxt, (890, 82))

    # Логика
    if not player.Plane.engine:
        player.Plane.trotl = 0
    if player.Plane.speed - 10 > player.Plane.trotl:
        player.Plane.speed -= 0.05
    elif player.Plane.speed < player.Plane.trotl:
        player.Plane.speed += player.Plane.trotl / 1000 - player.Plane.flaps / 200

    if player.Plane.fuel <= 0:
        player.Plane.engine = False
    if player.Plane.fuel > 0:
        if player.Plane.engine:
            player.Plane.fuel -= 0.005
    else:
        player.Plane.fuel = 0

    if player.Plane.spoilers:
        player.Plane.speed -= 0.05


    def fly_up():
        if (40 - player.Plane.flaps * 2) < player.Plane.speed < 40:
            player.Plane.y -= 1
            player.Plane.speed -= 0.05
        elif player.Plane.speed >= 40:
            player.Plane.y -= 2
            player.Plane.speed -= 0.05


    def fly_down():
        player.Plane.y += 2
        if player.Plane.speed < 100:
            player.Plane.speed += 0.1

    if player.Plane.speed < (30 - player.Plane.flaps * 2) and player.Plane.y < GROUND:
        player.Plane.y += 1

    if player.Plane.y > GROUND:
        player.Plane.y = GROUND

    if player.Plane.speed > 100:
        player.Plane.speed = 100
    if player.Plane.speed < 0:
        player.Plane.speed = 0

    bgx -= player.Plane.speed / 10
    bgx2 -= player.Plane.speed / 10
    if bgx <= -1000:
        bgx = 1000
        if wi == 18:
            wi = 0
        else:
            wi += 2
    if bgx2 <= -1000:
        bgx2 = 1000
        if wi2 == 19:
            wi2 = 1
        else:
            wi2 += 2

    # Нажатия на клавиши
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.Plane.y > 10:
        fly_up()
    if keys[pygame.K_DOWN] and player.Plane.y < GROUND:
        fly_down()
    if keys[pygame.K_q] and player.Plane.trotl < 100 and player.Plane.engine:
        player.Plane.trotl += 1
    if keys[pygame.K_a] and player.Plane.trotl > 0:
        player.Plane.trotl -= 1
    if keys[pygame.K_1] and not pre and player.Plane.fuel > 0:
        if player.Plane.engine:
            player.Plane.engine = False
        else:
            player.Plane.engine = True
        pre = True
    if not keys[pygame.K_1]:
        pre = False
    if keys[pygame.K_w] and not pre2 and player.Plane.flaps < 5:
        player.Plane.flaps += 1
        pre2 = True
    if keys[pygame.K_s] and not pre3 and player.Plane.flaps > 0:
        player.Plane.flaps -= 1
        pre3 = True
    if not keys[pygame.K_w]:
        pre2 = False
    if not keys[pygame.K_s]:
        pre3 = False
    if keys[pygame.K_z]:
        player.Plane.spoilers = True
    else:
        player.Plane.spoilers = False

    pygame.display.update()

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
            pygame.quit()

    clock.tick(60)
