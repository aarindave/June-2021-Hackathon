# Imports the Pygame module.
import pygame
# Imports the constants of Pygame to improve readability.
from pygame.locals import *

# Initializes the font and sound modules of Pygame.
pygame.font.init()
pygame.mixer.init()

# Sets the width and height of the window.
WIDTH = 800
HEIGHT = 800

# Sets 1/100 of the width and height of the window to be used as a unit of measurement.
WIDTH_SPACING = WIDTH // 100
HEIGHT_SPACING = HEIGHT // 100

# Sets the position and status of the mouse
mouse_x = 0
mouse_y = 0
mouse_down = False

levels = [1, 1, 1, 1]

# Sets the initial popularity of the game
popularity = 2.5

# Sets the net worth and rate of profit.
profit = 0
profit_rate = 0.005

page = "menu"
inactive = False

# Loads and resizes the server icon.
server = pygame.image.load("server.png")
server = pygame.transform.scale(server, (50, 50))

# Loads and resizes the security icon.
security = pygame.image.load("security.png")
security = pygame.transform.scale(security, (50, 50))

# Loads and resizes the advertisement icon.
ad = pygame.image.load("ad.png")
ad = pygame.transform.scale(ad, (50, 50))

# Loads and resizes the webinar icon.
webinar = pygame.image.load("webinar.png")
webinar = pygame.transform.scale(webinar, (50, 50))

# Loads the click sound effect.
click = pygame.mixer.Sound("click.mp3")

# Creates a Pygame window with a width and height of 800 pixels.
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Sets the caption or title of the Pygame window appropriately.
pygame.display.set_caption("Xbit Cryptocurrency Business Simulator")


# This function resets all of the global variables to be used in every time you play the game.
def reset():
    global mouse_x, mouse_y, mouse_down, levels, popularity, profit, profit_rate, page, inactive

    mouse_x = 0
    mouse_y = 0
    mouse_down = False

    levels = [1, 1, 1, 1]
    popularity = 2.5

    profit = 0
    profit_rate = 0.005

    page = "menu"
    inactive = False


# This displays text easily in a variety of contexts.
def show_text(text, x, y, color, size, center=False, center_x=False, center_y=False):
    font_object = pygame.font.Font("/System/Library/Fonts/Avenir.ttc", size)
    text_object = font_object.render(text, False, color)
    if center:
        screen.blit(text_object, (x - text_object.get_width() // 2, y - text_object.get_height() // 2))
    elif center_x:
        screen.blit(text_object, (x - text_object.get_width() // 2, y))
    elif center_y:
        screen.blit(text_object, (x, y - text_object.get_height() // 2))
    else:
        screen.blit(text_object, (x, y))


# This functions draws a rectangle using the center position.
def center_rect(x, y, width, height, color, border_radius=-1, text=""):
    rectangle = pygame.draw.rect(screen, color, (x - width // 2, y - height // 2, width, height), 0, border_radius)
    show_text(text, x, y, "white", height // 2, True)
    return rectangle


# This function operates what you see on the title or menu screen.
def menu():
    # Displays the title of the game.
    show_text("Xbit Cryptocurrency Simulation", WIDTH_SPACING * 50, HEIGHT_SPACING * 10, "white", 50, True)

    # Displays the play button.
    play = center_rect(WIDTH_SPACING * 50, HEIGHT_SPACING * 25, 200, 75, "green", 10, "Play")
    # Displays the instructions button.
    instructions = center_rect(WIDTH_SPACING * 50, HEIGHT_SPACING * 40, 200, 75, "gold1", 10, "Instructions")

    # If the mouse is held down that frame.
    if mouse_down:
        if play.collidepoint(mouse_x, mouse_y):
            # Resets all of the global variables.
            reset()
            # Plays the click sound effect.
            click.play()
            return "main"
        elif instructions.collidepoint(mouse_x, mouse_y):
            # Plays the click sound effect.
            click.play()
            return "instructions"
    return "menu"


# This function operates what you see on the main screen.
def main():
    global profit, profit_rate, popularity, levels, inactive

    # This shows our profit rounded to two decimal places.
    show_text("Net Worth: ${:.2f}".format(profit), WIDTH_SPACING, HEIGHT_SPACING, "white", 40)

    # This draws the bar to indicate how much popularity we have visually.
    pygame.draw.rect(screen, "darkgreen", (0, HEIGHT_SPACING * 10, WIDTH_SPACING * 100, 50))
    pygame.draw.rect(screen, "green", (0, HEIGHT_SPACING * 10, WIDTH_SPACING * popularity, 50))

    # This gives the percentage of popularity.
    show_text(f"Popularity: {round(popularity, 1)}%", WIDTH_SPACING * 2, HEIGHT_SPACING * 10.75, "white", 25)

    # This displays the four options.
    upgrade_servers = pygame.draw.rect(screen, "gray30", (WIDTH_SPACING, HEIGHT_SPACING * 20, 350, 50), 0, 10)
    upgrade_security = pygame.draw.rect(screen, "gray30", (WIDTH_SPACING, HEIGHT_SPACING * 27, 350, 50), 0, 10)
    increase_ads = pygame.draw.rect(screen, "gray30", (WIDTH_SPACING, HEIGHT_SPACING * 34, 350, 50), 0, 10)
    host_webinar = pygame.draw.rect(screen, "gray30", (WIDTH_SPACING, HEIGHT_SPACING * 41, 350, 50), 0, 10)

    # This displays the text of the buttons.
    show_text(f"Upgrade Servers: ${levels[0]}", WIDTH_SPACING * 2, HEIGHT_SPACING * 23, "white", 25, center_y=True)
    show_text(f"Upgrade Security: ${levels[1]*5}", WIDTH_SPACING * 2, HEIGHT_SPACING * 30, "white", 25, center_y=True)
    show_text(f"Increases Ads: ${levels[2]*10}", WIDTH_SPACING * 2, HEIGHT_SPACING * 37, "white", 25, center_y=True)
    show_text(f"Host a Webinar: ${levels[3]*20}", WIDTH_SPACING * 2, HEIGHT_SPACING * 44, "white", 25, center_y=True)

    # This displays the icons for each option to the screen.
    screen.blit(server, upgrade_servers.topright)
    screen.blit(security, upgrade_security.topright)
    screen.blit(ad, (increase_ads.right + 5, increase_ads.top))
    screen.blit(webinar, host_webinar.topright)

    # This displays the text to show the financial tips
    tip_bar = pygame.draw.rect(screen, "white", (WIDTH_SPACING * 55, HEIGHT_SPACING * 20, WIDTH_SPACING * 42, HEIGHT_SPACING * 70), 0, 10)
    show_text("Finance Tips", tip_bar.centerx, tip_bar.top + 30, "black", 40, True)
    show_text("You may seem off to a bad", tip_bar.left + 10, tip_bar.top + 60, "black", 20)
    show_text("start. However, all great", tip_bar.left + 10, tip_bar.top + 90, "black", 20)
    show_text("businesses start out small!", tip_bar.left + 10, tip_bar.top + 120, "black", 20)
    show_text("The secret to a great business", tip_bar.left + 10, tip_bar.top + 150, "black", 20)
    show_text("is to be patient! Being", tip_bar.left + 10, tip_bar.top + 180, "black", 20)
    show_text("patient provides you with", tip_bar.left + 10, tip_bar.top + 210, "black", 20)
    show_text("more money and choices for", tip_bar.left + 10, tip_bar.top + 240, "black", 20)
    show_text("you to choose from! Also,", tip_bar.left + 10, tip_bar.top + 270, "black", 20)
    show_text("timing is essential as getting", tip_bar.left + 10, tip_bar.top + 300, "black", 20)
    show_text("something too early or too", tip_bar.left + 10, tip_bar.top + 330, "black", 20)
    show_text("late leads to financial", tip_bar.left + 10, tip_bar.top + 360, "black", 20)
    show_text("consequences in later life.", tip_bar.left + 10, tip_bar.top + 390, "black", 20)
    show_text("Apply these tips in the simple", tip_bar.left + 10, tip_bar.top + 420, "black", 20)
    show_text("simulation I have made for", tip_bar.left + 10, tip_bar.top + 450, "black", 20)
    show_text("you. Good luck and spend!", tip_bar.left + 10, tip_bar.top + 480, "black", 20)

    # If the mouse is held down that frame.
    if mouse_down:
        if upgrade_servers.collidepoint(mouse_x, mouse_y):
            profit -= levels[0]
            # Increase the profit rate by 0.02.
            profit_rate += 0.02
            # Sets the inactivity of the company to False.
            inactive = False
            levels[0] += 1
            # Plays the click sound effect.
            click.play()
        elif upgrade_security.collidepoint(mouse_x, mouse_y):
            profit -= levels[1]*5
            # Increase the profit rate by 0.05.
            profit_rate += 0.05
            # Sets the inactivity of the company to False.
            inactive = False
            levels[1] += 2
            # Plays the click sound effect.
            click.play()
        elif increase_ads.collidepoint(mouse_x, mouse_y):
            profit -= levels[2]*10
            # Increase the profit rate by 0.1.
            profit_rate += 0.1
            # Sets the inactivity of the company to False.
            inactive = False
            levels[2] += 3
            # Plays the click sound effect.
            click.play()
        elif host_webinar.collidepoint(mouse_x, mouse_y):
            profit -= levels[3]*20
            # Increase the profit rate by 0.2.
            profit_rate += 0.2
            # Sets the inactivity of the company to False.
            inactive = False
            levels[3] += 4
            # Plays the click sound effect.
            click.play()

    # Increases the net worth by the profit rate.
    profit += profit_rate

    # If the net worth or popularity falls below 0.
    if profit <= 0 or popularity <= 0:
        # Returns "end" to signify the end of the game.
        return "end"

    # If the company is inactive.
    if inactive:
        # Decrease the popularity by 0.01%
        popularity -= 0.01
        # If the popularity falls below zero.
        if popularity < 0:
            # Returns "end" to signify the end of the game.
            return "end"
    elif popularity * 5 < sum(levels):
        popularity += 0.05 * (sum(levels) - popularity)
        if popularity >= 100:
            # Returns "win" to signify the end of the game.
            return "win"
    elif popularity * 5 >= sum(levels):
        inactive = True
    return "main"


def instructions():
    # This displays the instructions.
    show_text("How to Play", WIDTH_SPACING, HEIGHT_SPACING, "white", 48)
    show_text("Gain revenue by waiting!", WIDTH_SPACING, HEIGHT_SPACING * 10, "white", 24)
    show_text("Upgrade to increase your popularity, capacity, and revenue!", WIDTH_SPACING, HEIGHT_SPACING * 15, "white", 24)
    show_text("Don't reach bankruptcy ($0 or less)!", WIDTH_SPACING, HEIGHT_SPACING * 20, "white", 24)
    show_text("Don't reach 0% popularity!", WIDTH_SPACING, HEIGHT_SPACING * 25, "white", 24)
    show_text("Get 100% popularity to win!", WIDTH_SPACING, HEIGHT_SPACING * 30, "white", 24)

    # This creates a play button.
    play = center_rect(WIDTH_SPACING * 15, HEIGHT_SPACING * 40, 200, 75, "green", 10, "Play")
    # This creates a back button.
    back = center_rect(WIDTH_SPACING * 45, HEIGHT_SPACING * 40, 200, 75, "red", 10, "Back")

    # If the mouse is held down.
    if mouse_down:
        # If the mouse is touching the play button.
        if play.collidepoint(mouse_x, mouse_y):
            # Resets all of the global variables.
            reset()
            # Plays the click sound effect.
            click.play()
            # Returns "main" to signify to switch pages.
            return "main"
        # If the mouse is touching the back button.
        elif back.collidepoint(mouse_x, mouse_y):
            # Plays the click sound effect.
            click.play()
            # Returns "menu" to signify to switch pages.
            return "menu"

    return "instructions"


def end(win=False):
    # If you win the game.
    if win:
        # Shows a congratulations message.
        show_text("Congratulations! You Won!", WIDTH_SPACING * 50, HEIGHT_SPACING * 30, "green", 50, True)
    # Otherwise, if you lost of the game.
    else:
        # Shows a defeat message.
        show_text("Game Over! Try Again!", WIDTH_SPACING * 50, HEIGHT_SPACING * 30, "red", 50, True)

    # Displays the play button.
    play = center_rect(WIDTH_SPACING * 50, HEIGHT_SPACING * 50, 200, 75, "green", 10, "Play")
    # Displays the back button.
    back = center_rect(WIDTH_SPACING * 50, HEIGHT_SPACING * 65, 200, 75, "red", 10, "Back")

    # If the mouse is held down that frame.
    if mouse_down:
        # If the mouse is touching the play button.
        if play.collidepoint(mouse_x, mouse_y):
            # Resets all of the global variables.
            reset()
            # Plays the click sound effect.
            click.play()
            # Returns "main" to signify to switch pages.
            return "main"
        elif back.collidepoint(mouse_x, mouse_y):
            # Plays the click sound effect.
            click.play()
            # Returns "menu" to signify to switch pages.
            return "menu"

    # Returns "end" to signify the end of the game.
    return "end"


# Setup a clock to control the frame rate of the program.
clock = pygame.time.Clock()

# This is the game loop where all of the events and game logic is controlled.
while True:
    # Iterate through each event in the list of Pygame events.
    for event in pygame.event.get():
        # If the quit button was clicked.
        if event.type == QUIT:
            # Quits the Pygame module.
            pygame.quit()
            # Exits the program.
            exit()
        # If the mouse is being pressed.
        elif event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            mouse_down = True

    # Fill the background with a solid, blue color.
    screen.fill("deepskyblue2")

    # If we are at the start screen.
    if page == "menu":
        page = menu()
    # If we are playing the game.
    elif page == "main":
        page = main()
    # If we are at the instructions page.
    elif page == "instructions":
        page = instructions()
    # If the game ended due to victory or defeat.
    elif page in ["end", "win"]:
        page = end(page == "win")

    # Resets the mouse down variable to ensure each action upon mouse click occurs once.
    mouse_down = False
    # Updates the entire Pygame window to show all of the updated elements.
    pygame.display.update()
    # Slows down the frame rate to roughly 30 frames per second.
    clock.tick(30)
