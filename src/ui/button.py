import pygame
from pygame.locals import *

class Button:
    def __init__(self, cx, cy, w, h, base_color, text="", font=None, icon=None, corner=14):
        self.rect = pygame.Rect(cx - w//2, cy - h//2, w, h)
        self.base_color = base_color
        self.color = base_color
        self.text = text
        self.font = font
        self.icon = icon
        self.corner = corner
        self.hovered = False
        self.pulse = 0.0

    def update_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.hovered:
            self.pulse = min(1.0, self.pulse + 0.06)
        else:
            self.pulse = max(0.0, self.pulse - 0.06)

    def draw(self, screen):
        r = int(self.base_color[0] + 40 * self.pulse)
        g = int(self.base_color[1] + 40 * self.pulse)
        b = int(self.base_color[2] + 40 * self.pulse)
        draw_color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
        pygame.draw.rect(screen, draw_color, self.rect, border_radius=self.corner)
        # inner glow
        inner = self.rect.inflate(-6, -6)
        glow_surf = pygame.Surface((inner.w, inner.h), pygame.SRCALPHA)
        glow = 40 + int(120 * self.pulse)
        glow_color = (draw_color[0], draw_color[1], draw_color[2], glow)
        pygame.draw.rect(glow_surf, glow_color, glow_surf.get_rect(), border_radius=self.corner-4)
        screen.blit(glow_surf, inner.topleft)
        if self.text and self.font:
            txt = self.font.render(self.text, True, (255,255,255))
            screen.blit(txt, txt.get_rect(center=self.rect.center))
        if self.icon:
            icon_rect = self.icon.get_rect()
            icon_rect.topright = (self.rect.right - 12, self.rect.top + 10)
            screen.blit(self.icon, icon_rect)

    def clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
