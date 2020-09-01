import pygame
import os
import time
import random
pygame.font.init()


# Width and Height of the screen. aka how big it is
WIDTH, HEIGHT = 700, 700

# Displaying the window itself
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#the name of the window
pygame.display.set_caption("Space Invaders")

# Loading the Images

redSpaceShip = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
greenSpaceShip = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
blueSpaceShip = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Loding the Player ship
yellowSpaceShip = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

#Loading the Lasers
redLaser = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
greenLaser = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
blueLaser = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))

#Player Laser
yellowLaser = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

#Load Background Image
backgroundImage = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

class Ship():
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = yellowSpaceShip
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
            return self.ship_img.get_width()

    def get_height(self):
            return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.player_img = yellowSpaceShip
        self.laser_img = yellowLaser
        self.mask = pygame.mask.from_surface(self.player_img)
        self.max_health = health



class EnemyShip(Ship):
    COLOR_MAP = {
            "red": (redSpaceShip, redLaser),
            "blue": (greenSpaceShip, greenLaser),
            "green": (blueSpaceShip, blueLaser)
                }

    def __init__(self, x, y,color, health=100):

        super().__init__( x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

def main():
    run = True
    fps = 900
    level = 0
    lives = 3
    main_font = pygame.font.SysFont("Arial", 50)

    enemies = []

    waveLength = 5

    enemy_vel = 1

    player_vel = 5

    player = Player(300, 650)

    clock = pygame.time.Clock()

    def redraw_Window():
        # Drawing the background image
        WIN.blit(backgroundImage, (0,0))

        #drawing the text
        lives_label = main_font.render(f"Lives: {lives}", 1 , (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1 , (255,255,255))
        WIN.blit(lives_label, (10,10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        pygame.display.update()
    
    while run:
        clock.tick(fps)

        #starts a new level when you finished the last one
        if len(enemies) == 0:
            level += 1
            waveLength += 5

            for i in range(waveLength):
                enemy = EnemyShip(random.randrange(50, WIDTH-100), random.randrange(-1500,-100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)
                

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: #moving left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: #moving right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: #moving forward
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT: #moving downward
            player.y += player_vel

        for enemy in enemies:
            enemy.move(enemy_vel)

        redraw_Window()
main()