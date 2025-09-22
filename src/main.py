import pygame
from pygame.locals import *

class XbitSimulator:
    def __init__(self):
        # Initialize Pygame modules
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        # Screen setup
        self.WIDTH, self.HEIGHT = 800, 800
        self.WIDTH_SPACING = self.WIDTH // 100
        self.HEIGHT_SPACING = self.HEIGHT // 100
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Xbit Cryptocurrency Business Simulator")

        # Mouse state
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_down = False

        # Game state
        self.levels = [1, 1, 1, 1]
        self.popularity = 2.5
        self.profit = 0
        self.profit_rate = 0.005
        self.page = "menu"
        self.inactive = False

        # Assets
        self.server = pygame.transform.scale(pygame.image.load("assets/images/server.png"), (50, 50))
        self.security = pygame.transform.scale(pygame.image.load("assets/images/security.png"), (50, 50))
        self.ad = pygame.transform.scale(pygame.image.load("assets/images/ad.png"), (50, 50))
        self.webinar = pygame.transform.scale(pygame.image.load("assets/images/webinar.png"), (50, 50))
        self.click_sound = pygame.mixer.Sound("assets/sounds/click.mp3")

        # Clock
        self.clock = pygame.time.Clock()

    # ----------------------------
    # Utility Methods
    # ----------------------------
    def reset(self):
        self.mouse_x = self.mouse_y = 0
        self.mouse_down = False
        self.levels = [1, 1, 1, 1]
        self.popularity = 2.5
        self.profit = 0
        self.profit_rate = 0.005
        self.page = "menu"
        self.inactive = False

    def show_text(self, text, x, y, color, size, center=False, center_x=False, center_y=False):
        font_object = pygame.font.Font("/System/Library/Fonts/Avenir.ttc", size)
        text_object = font_object.render(text, False, color)
        if center:
            self.screen.blit(text_object, (x - text_object.get_width() // 2, y - text_object.get_height() // 2))
        elif center_x:
            self.screen.blit(text_object, (x - text_object.get_width() // 2, y))
        elif center_y:
            self.screen.blit(text_object, (x, y - text_object.get_height() // 2))
        else:
            self.screen.blit(text_object, (x, y))

    def center_rect(self, x, y, width, height, color, border_radius=-1, text=""):
        rect = pygame.draw.rect(self.screen, color, (x - width // 2, y - height // 2, width, height), 0, border_radius)
        if text:
            self.show_text(text, x, y, "white", height // 2, center=True)
        return rect

    # Game Pages
    def menu(self):
        self.show_text("Xbit Cryptocurrency Simulation", self.WIDTH_SPACING*50, self.HEIGHT_SPACING*10, "white", 50, True)
        play_btn = self.center_rect(self.WIDTH_SPACING*50, self.HEIGHT_SPACING*25, 200, 75, "green", 10, "Play")
        instr_btn = self.center_rect(self.WIDTH_SPACING*50, self.HEIGHT_SPACING*40, 200, 75, "gold1", 10, "Instructions")

        if self.mouse_down:
            if play_btn.collidepoint(self.mouse_x, self.mouse_y):
                self.reset()
                self.click_sound.play()
                return "main"
            elif instr_btn.collidepoint(self.mouse_x, self.mouse_y):
                self.click_sound.play()
                return "instructions"
        return "menu"

    def main(self):
        # Show net worth and popularity bar
        self.show_text(f"Net Worth: ${self.profit:.2f}", self.WIDTH_SPACING, self.HEIGHT_SPACING, "white", 40)
        pygame.draw.rect(self.screen, "darkgreen", (0, self.HEIGHT_SPACING*10, self.WIDTH_SPACING*100, 50))
        pygame.draw.rect(self.screen, "green", (0, self.HEIGHT_SPACING*10, self.WIDTH_SPACING* self.popularity, 50))
        self.show_text(f"Popularity: {round(self.popularity,1)}%", self.WIDTH_SPACING*2, self.HEIGHT_SPACING*10.75, "white", 25)

        # Buttons for upgrades
        btns = [
            ("Upgrade Servers", self.levels[0], 0.02, 1, self.server),
            ("Upgrade Security", self.levels[1]*5, 0.05, 2, self.security),
            ("Increase Ads", self.levels[2]*10, 0.1, 3, self.ad),
            ("Host Webinar", self.levels[3]*20, 0.2, 4, self.webinar)
        ]

        for i, (label, cost, rate_inc, level_idx, icon) in enumerate(btns):
            y_pos = self.HEIGHT_SPACING*(20 + 7*i)
            rect = pygame.draw.rect(self.screen, "gray30", (self.WIDTH_SPACING, y_pos, 350, 50), 0, 10)
            self.show_text(f"{label}: ${cost}", self.WIDTH_SPACING*2, y_pos+25, "white", 25, center_y=True)
            self.screen.blit(icon, rect.topright)
            if self.mouse_down and rect.collidepoint(self.mouse_x, self.mouse_y):
                self.profit -= cost
                self.profit_rate += rate_inc
                self.inactive = False
                self.levels[level_idx-1] += level_idx
                self.click_sound.play()

        # Profit accumulation and popularity adjustment
        self.profit += self.profit_rate
        if self.profit <= 0 or self.popularity <= 0:
            return "end"

        if self.inactive:
            self.popularity -= 0.01
            if self.popularity < 0:
                return "end"
        elif self.popularity * 5 < sum(self.levels):
            self.popularity += 0.05 * (sum(self.levels) - self.popularity)
            if self.popularity >= 100:
                return "win"
        else:
            self.inactive = True

        return "main"

    def instructions(self):
        self.show_text("How to Play", self.WIDTH_SPACING, self.HEIGHT_SPACING, "white", 48)
        instructions = [
            "Gain revenue by waiting!",
            "Upgrade to increase your popularity, capacity, and revenue!",
            "Don't reach bankruptcy ($0 or less)!",
            "Don't reach 0% popularity!",
            "Get 100% popularity to win!"
        ]
        for i, line in enumerate(instructions):
            self.show_text(line, self.WIDTH_SPACING, self.HEIGHT_SPACING*(10 + 5*i), "white", 24)

        play_btn = self.center_rect(self.WIDTH_SPACING*15, self.HEIGHT_SPACING*40, 200, 75, "green", 10, "Play")
        back_btn = self.center_rect(self.WIDTH_SPACING*45, self.HEIGHT_SPACING*40, 200, 75, "red", 10, "Back")

        if self.mouse_down:
            if play_btn.collidepoint(self.mouse_x, self.mouse_y):
                self.reset()
                self.click_sound.play()
                return "main"
            elif back_btn.collidepoint(self.mouse_x, self.mouse_y):
                self.click_sound.play()
                return "menu"
        return "instructions"

    def end(self, win=False):
        if win:
            self.show_text("Congratulations! You Won!", self.WIDTH_SPACING*50, self.HEIGHT_SPACING*30, "green", 50, True)
        else:
            self.show_text("Game Over! Try Again!", self.WIDTH_SPACING*50, self.HEIGHT_SPACING*30, "red", 50, True)

        play_btn = self.center_rect(self.WIDTH_SPACING*50, self.HEIGHT_SPACING*50, 200, 75, "green", 10, "Play")
        back_btn = self.center_rect(self.WIDTH_SPACING*50, self.HEIGHT_SPACING*65, 200, 75, "red", 10, "Back")

        if self.mouse_down:
            if play_btn.collidepoint(self.mouse_x, self.mouse_y):
                self.reset()
                self.click_sound.play()
                return "main"
            elif back_btn.collidepoint(self.mouse_x, self.mouse_y):
                self.click_sound.play()
                return "menu"
        return "end"
    
    # Main Loop
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == MOUSEBUTTONDOWN:
                    self.mouse_x, self.mouse_y = event.pos
                    self.mouse_down = True

            self.screen.fill("deepskyblue2")

            if self.page == "menu":
                self.page = self.menu()
            elif self.page == "main":
                self.page = self.main()
            elif self.page == "instructions":
                self.page = self.instructions()
            elif self.page in ["end", "win"]:
                self.page = self.end(self.page == "win")

            self.mouse_down = False
            pygame.display.update()
            self.clock.tick(30)


if __name__ == "__main__":
    XbitSimulator().run()
