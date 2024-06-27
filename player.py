import pygame

pygame.init()


class Plane:
    def __init__(self):
        pass

    y = 615
    trotl = 0
    speed = 0
    fuel = 100.0
    flaps = 0
    spoilers = False
    gear = False
    gearBrakes = False
    engine = False
    planeim = pygame.image.load("img/plane.png")
