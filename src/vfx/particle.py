import pygame
import random
from pygame.locals import *

class Particle:
    def __init__(self, x, y, color, life=45):
        self.x = x
        self.y = y
        self.radius = random.uniform(2, 5)
        self.color = color
        self.vx = random.uniform(-2.0, 2.0)
        self.vy = random.uniform(-3.0, -0.5)
        self.life = life

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.99
        self.vy += 0.08
        self.radius *= 0.985
        self.life -= 1

    def draw(self, screen):
        if self.life > 0 and self.radius > 0:
            surf = pygame.Surface((int(self.radius*2)+4, int(self.radius*2)+4), pygame.SRCALPHA)
            pygame.draw.circle(surf, self.color, (surf.get_width()//2, surf.get_height()//2), max(1, int(self.radius)))
            screen.blit(surf, (int(self.x - surf.get_width()//2), int(self.y - surf.get_height()//2)))
