import pygame
import random
import os
from pygame.locals import *

from ui.button import Button
from vfx.particle import Particle

class CyberTycoon:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.WIDTH, self.HEIGHT = 800, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Cyber Tycoon")
        self.clock = pygame.time.Clock()

        # fonts with fallback
        try:
            self.title_font = pygame.font.Font("/System/Library/Fonts/Avenir.ttc", 48)
            self.text_font = pygame.font.Font("/System/Library/Fonts/Avenir.ttc", 20)
            self.ui_font = pygame.font.Font("/System/Library/Fonts/Avenir.ttc", 22)
        except Exception:
            self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
            self.text_font = pygame.font.SysFont("Arial", 20)
            self.ui_font = pygame.font.SysFont("Arial", 22)

        # load assets
        self.assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
        self.images_dir = os.path.join(self.assets_dir, "images")
        self.sounds_dir = os.path.join(self.assets_dir, "sounds")
        self.server = self.safe_load_image("server.png", (48,48))
        self.security = self.safe_load_image("security.png", (48,48))
        self.ad = self.safe_load_image("ad.png", (48,48))
        self.webinar = self.safe_load_image("webinar.png", (48,48))
        self.click_sound = self.safe_load_sound("click.mp3")

        # game state
        self.levels = [1,1,1,1]
        self.popularity = 2.5
        self.displayed_popularity = 2.5
        self.profit = 0.0
        self.displayed_profit = 0.0
        self.profit_rate = 0.005
        self.inactive = False
        self.page = "menu"

        # UI and particles
        self.particles = []
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_down = False

        # background streams for cyber aesthetic
        self.streams = [random.randint(0, self.HEIGHT) for _ in range(120)]

        # buttons placeholder
        self.main_buttons = []

        # timers
        self.event_timer = 0

    def safe_load_image(self, filename, size=None):
        path = os.path.join(self.images_dir, filename)
        try:
            img = pygame.image.load(path).convert_alpha()
            if size:
                img = pygame.transform.smoothscale(img, size)
            return img
        except Exception:
            # return simple placeholder surface if missing
            surf = pygame.Surface(size or (48,48), pygame.SRCALPHA)
            pygame.draw.rect(surf, (100,100,100), surf.get_rect(), border_radius=8)
            return surf

    def safe_load_sound(self, filename):
        path = os.path.join(self.sounds_dir, filename)
        try:
            return pygame.mixer.Sound(path)
        except Exception:
            # return silent fallback
            class Silent:
                def play(self, *a, **k): pass
            return Silent()

    ## utility drawing

    def lerp(self, a, b, t):
        return a + (b - a) * t

    def draw_neon_gradient(self):
        # vertical gradient base
        for i in range(self.HEIGHT):
            r = int(6 + i * 0.02)
            g = int(10 + i * 0.03)
            b = int(20 + i * 0.08)
            pygame.draw.line(self.screen, (r, g, b), (0, i), (self.WIDTH, i))
        # subtle vignette
        vignette = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.draw.ellipse(vignette, (0, 0, 0, 120), (-self.WIDTH*0.2, -self.HEIGHT*0.2, int(self.WIDTH*1.4), int(self.HEIGHT*1.4)))
        self.screen.blit(vignette, (0,0))

    def draw_streams(self):
        for i, y in enumerate(self.streams):
            x = int(i * (self.WIDTH / len(self.streams)))
            color = (0, 120 + (i % 6)*20, 180 + (i % 4)*12)
            pygame.draw.line(self.screen, color, (x, y), (x, y+18), 2)
            # drift
            if random.random() < 0.4:
                self.streams[i] += random.randint(2,6)
            if self.streams[i] > self.HEIGHT + 20:
                self.streams[i] = -random.randint(0, 40)

    def draw_header(self):
        # Main title
        title = self.title_font.render("Cyber Tycoon", True, (0, 255, 200))
        self.screen.blit(title, title.get_rect(center=(self.WIDTH//2, 60)))
        # Subtitle directly under title
        subtitle = self.text_font.render("Manage nodes, security, marketing, and webinars", True, (180, 200, 220))
        self.screen.blit(subtitle, subtitle.get_rect(center=(self.WIDTH//2, 110)))


    ## page builders

    def build_main_buttons(self):
        # button definitions: label_template, cost_calc, rate_inc, level_idx, icon_surface
        specs = [
            ("Upgrade Nodes", lambda: int(self.levels[0]), 0.02, 0, self.server),
            ("Upgrade Security", lambda: int(self.levels[1]*5), 0.05, 1, self.security),
            ("Launch Marketing", lambda: int(self.levels[2]*10), 0.1, 2, self.ad),
            ("Host Webinar", lambda: int(self.levels[3]*20), 0.2, 3, self.webinar)
        ]
        self.main_buttons = []
        base_y = 250
        for i, (label, cost_fn, rate_inc, idx, icon) in enumerate(specs):
            cost = cost_fn()
            btn = Button(self.WIDTH//2, base_y + i*78, 420, 64, (28,28,36), f"{label}  •  ${cost}", font=self.ui_font, icon=icon)
            self.main_buttons.append((btn, rate_inc, idx, cost))

    def page_menu(self):
        self.draw_neon_gradient()
        self.draw_streams()
        self.draw_header()
        # Center menu buttons
        play = Button(self.WIDTH//2, 240, 300, 84, (0,150,130), "Play", font=self.ui_font)
        instr = Button(self.WIDTH//2, 340, 300, 84, (210,170,30), "Instructions", font=self.ui_font)
        for b in [play, instr]:
            b.update_hover((self.mouse_x, self.mouse_y))
            b.draw(self.screen)
        # Handle clicks
        if self.mouse_down:
            if play.clicked((self.mouse_x, self.mouse_y)):
                self.reset_state()
                if hasattr(self.click_sound, "play"): 
                    self.click_sound.play()
                return "main"
            if instr.clicked((self.mouse_x, self.mouse_y)):
                if hasattr(self.click_sound, "play"): 
                    self.click_sound.play()
                return "instructions"
        return "menu"

    def page_instructions(self):
        self.draw_neon_gradient()
        self.draw_streams()
        self.draw_header()
        lines = [
            "How to Play",
            "Gain revenue by waiting. Use upgrades to increase revenue and popularity.",
            "If profit <= $0 you lose. If popularity <= 0 you lose.",
            "Reach 100% popularity to win.",
            "Random events may help or harm your company.",
        ]
        y = 140
        self.draw_text_block(lines, 56, y)
        # two buttons
        play = Button(self.WIDTH//3, 700, 220, 64, (0,160,0), "Play", font=self.ui_font)
        back = Button(self.WIDTH*2//3, 700, 220, 64, (160,20,20), "Back", font=self.ui_font)
        for b in [play, back]:
            b.update_hover((self.mouse_x, self.mouse_y))
            b.draw(self.screen)
        if self.mouse_down:
            if play.clicked((self.mouse_x, self.mouse_y)):
                self.reset_state()
                if hasattr(self.click_sound, "play"): self.click_sound.play()
                return "main"
            if back.clicked((self.mouse_x, self.mouse_y)):
                if hasattr(self.click_sound, "play"): self.click_sound.play()
                return "menu"
        return "instructions"

    def page_main(self):
        self.draw_neon_gradient()
        self.draw_streams()

        # update displayed profit/popularity smoothly
        self.displayed_profit = self.lerp(self.displayed_profit, self.profit, 0.08)
        self.displayed_popularity = self.lerp(self.displayed_popularity, self.popularity, 0.06)

        # popularity bar panel
        panel_rect = pygame.Rect(24, 78, self.WIDTH - 48, 120)
        pygame.draw.rect(self.screen, (18,18,24), panel_rect, border_radius=14)
        # popularity bar
        bar_bg = pygame.Rect(40, 118, self.WIDTH - 80, 36)
        pygame.draw.rect(self.screen, (28,28,36), bar_bg, border_radius=10)
        fill_w = int(max(0, min(1.0, self.displayed_popularity / 100.0)) * bar_bg.width)
        fill_rect = pygame.Rect(bar_bg.x, bar_bg.y, fill_w, bar_bg.h)
        pygame.draw.rect(self.screen, (0,220,170), fill_rect, border_radius=10)
        pop_label = self.ui_font.render(f"Popularity: {self.displayed_popularity:.1f} %", True, (220, 240, 255))
        self.screen.blit(pop_label, (40, 86))
        # profit label in panel
        profit_label = self.ui_font.render(f"Net Worth: ${self.displayed_profit:.2f}", True, (220,240,255))
        self.screen.blit(profit_label, (self.WIDTH - profit_label.get_width() - 40, 86))

        # build buttons and draw them
        self.build_main_buttons()
        for btn, rate_inc, idx, cost in self.main_buttons:
            btn.update_hover((self.mouse_x, self.mouse_y))
            btn.draw(self.screen)
            if self.mouse_down and btn.clicked((self.mouse_x, self.mouse_y)):
                # buy action
                self.profit -= cost
                self.profit_rate += rate_inc
                self.inactive = False
                self.levels[idx] += (idx + 1)
                if hasattr(self.click_sound, "play"): self.click_sound.play()
                # particle burst
                for _ in range(14):
                    color = (0, 220, 200, 180)
                    self.particles.append(Particle(self.mouse_x, self.mouse_y, color))

        # profit accumulation and mechanics
        self.profit += self.profit_rate  # passive gain

        # inactivity/popularity logic
        if self.inactive:
            self.popularity -= 0.01
        elif self.popularity * 5 < sum(self.levels):
            self.popularity += 0.05 * (sum(self.levels) - self.popularity)
            if self.popularity >= 100:
                return "win"
        else:
            self.inactive = True

        # random events occasionally
        self.event_timer += 1
        if random.random() < 0.002:
            event = random.choice(["hack", "bonus", "media"])
            if event == "hack":
                self.profit *= 0.86
                for _ in range(18):
                    self.particles.append(Particle(random.randint(100, 700), random.randint(180, 520), (255, 100, 100)))
            elif event == "bonus":
                self.profit += 8
                for _ in range(10):
                    self.particles.append(Particle(random.randint(100, 700), random.randint(180, 520), (120, 255, 200)))
            else:
                self.popularity += 3
                for _ in range(8):
                    self.particles.append(Particle(random.randint(100, 700), random.randint(180, 520), (100, 180, 255)))

        # update particles
        for p in self.particles[:]:
            p.update()
            p.draw(self.screen)
            if p.life <= 0 or p.radius <= 0.4:
                try:
                    self.particles.remove(p)
                except ValueError:
                    pass

        # lose condition
        return "end" if self.profit <= 0 or self.popularity <= 0 else "main"


    def page_end(self, win=False):
        self.draw_neon_gradient()
        self.draw_streams()
        self.draw_header()
        message = "Victory. Company Ascendant." if win else "Defeat. Company Collapsed."
        color = (120, 255, 200) if win else (255, 120, 120)
        msg_surf = self.title_font.render(message, True, color)
        self.screen.blit(msg_surf, msg_surf.get_rect(center=(self.WIDTH//2, 180)))
        # action buttons
        again = Button(self.WIDTH//3, 620, 260, 72, (0,180,120), "Play Again", font=self.ui_font)
        menu = Button(self.WIDTH*2//3, 620, 260, 72, (200,40,60), "Menu", font=self.ui_font)
        for b in [again, menu]:
            b.update_hover((self.mouse_x, self.mouse_y))
            b.draw(self.screen)
        # visual confetti for win
        if win and random.random() < 0.25:
            for _ in range(6):
                self.particles.append(Particle(random.randint(80, 720), random.randint(200, 420), (random.randint(100,255), random.randint(160,255), 255)))
        # particle updates
        for p in self.particles[:]:
            p.update()
            p.draw(self.screen)
            if p.life <= 0:
                try:
                    self.particles.remove(p)
                except ValueError:
                    pass
        if self.mouse_down:
            if again.clicked((self.mouse_x, self.mouse_y)):
                self.reset_state()
                if hasattr(self.click_sound, "play"): self.click_sound.play()
                return "main"
            if menu.clicked((self.mouse_x, self.mouse_y)):
                if hasattr(self.click_sound, "play"): self.click_sound.play()
                return "menu"
        return "end"

    ## helper functions

    def draw_text_block(self, lines, x, start_y, leading=36):
        for i, line in enumerate(lines):
            col = (180, 220, 240) if i > 0 else (220, 255, 255)
            surf = self.text_font.render(line, True, col)
            self.screen.blit(surf, (x, start_y + i*leading))

    def reset_state(self):
        self.levels = [1,1,1,1]
        self.popularity = self.displayed_popularity = 2.5
        self.profit = self.displayed_profit = 0.0
        self.profit_rate = 0.005
        self.inactive = False
        self.particles.clear()
        # reset streams to random positions for visual variety
        self.streams = [random.randint(0, self.HEIGHT) for _ in range(len(self.streams))]

    ## main loop

    def run(self):
        while True:
            self.screen.fill((0,0,0))
            # event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    self.mouse_x, self.mouse_y = event.pos
                    self.mouse_down = True
                elif event.type == MOUSEMOTION:
                    self.mouse_x, self.mouse_y = event.pos

            # page routing
            if self.page == "menu":
                self.page = self.page_menu()
            elif self.page == "instructions":
                self.page = self.page_instructions()
            elif self.page == "main":
                self.page = self.page_main()
            elif self.page in ["end", "win"]:
                win = (self.page == "win")
                new_page = self.page_end(win)
                self.page = new_page or self.page

            # reset click state each frame
            self.mouse_down = False

            # draw streams on top for faint overlay
            self.draw_streams()
            pygame.display.flip()
            self.clock.tick(30)

if __name__ == "__main__":
    CyberTycoon().run()
