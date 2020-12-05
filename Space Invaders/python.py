# Importing the libraries
import pygame
import os
import time
import random
pygame.font.init()


# Defining the Width and Height of the screen
WIDTH, HEIGHT = 700, 700

# Displaying the window itself
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# The name of the window
pygame.display.set_caption("Space Invaders")

# Loading the enemy ship Images

redSpaceShip = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
greenSpaceShip = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
blueSpaceShip = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Loding the Player ship
yellowSpaceShip = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Loading the Lasers
redLaser = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
greenLaser = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
blueLaser = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))

# Player Laser
yellowLaser = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Load Background Image
backgroundImage = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))


#-------------------------- Making the laser Class --------------------------------------

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        for Laser in self.Lasers:
            Laser.draw(window)

    def collision(self, object):
        return collide(self, object)
        
    def move_lasers(self, vel, objects):
        self.cooldown()
        for Laser in self.Lasers:
            Laser.move(vel)
        if Laser.off_screen(HEIGHT):
            self.Lasers.remove(Laser)
        #elif Laser.collision()

    def move(self, vel):
        self.y += vel

    def off_screen(self, Height):
        return self.y <= Height and self.y >= 0



#------------------- Making the ship class ----------------------

class Ship:
    COOLDOWN = 30
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = yellowSpaceShip
        self.Laser_img = None
        self.Lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 0.6

    def Shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.Laser_img)
            self.Lasers.append(laser)
            self.cool_down_counter = 0.6

    def get_width(self):
            return self.ship_img.get_width()

    def get_height(self):
            return self.ship_img.get_height()



#-------- Making the player ship class(inherits from the ship class) --------------------

class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.player_img = yellowSpaceShip
        self.Laser_img = yellowLaser
        self.mask = pygame.mask.from_surface(self.player_img)
        self.max_health = health


#------- Making the Enemy ship class(inherits from the ship class) ----------------------

class EnemyShip(Ship):
    COLOR_MAP = {
            "red": (redSpaceShip, redLaser),
            "blue": (greenSpaceShip, greenLaser),
            "green": (blueSpaceShip, blueLaser)
                }

    def __init__(self, x, y,color, health=100):

        super().__init__( x, y, health)
        self.ship_img, self.Laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel


# Definint the collide function

def collide(object1, object2):
    offset_x = object2.x - object1.x
    offset_y = object2.y - object1.y
    return object1.mask.overlap(object2.mask, (offset_x, offset_y)) != None



#---------------------------- Defining the main function ---------------------------------

def main():
    run = True
    fps = 60
    level = 0
    lives = 3
    main_font = pygame.font.SysFont("Arial", 50)
    lost_font = pygame.font.SysFont("Arial", 65)

    enemies = []

    waveLength = 5

    enemyVelocity = 1

    playerVelocity = 5

    player = Player(300, 650)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_Window():
        # Drawing the background image
        WIN.blit(backgroundImage, (0,0))

        # Drawing the text
        lives_label = main_font.render(f"Lives: {lives}", 1 , (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1 , (255,255,255))
        WIN.blit(lives_label, (10,10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("GAME OVER", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/ 2 - lost_label.get_width()/2, 350))

        pygame.display.update()
    
    while run:
        clock.tick(fps)
        redraw_Window()
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > fps * 1.5:
                run = False
            else:
                continue

        #starts a new level when you finished the last one
        if len(enemies) == 0:
            level += 1
            waveLength += 5

            for i in range(waveLength):
                enemy = EnemyShip(random.randrange(50, WIDTH-100), random.randrange(-1700,-100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)
                


        # Stopping running on quitting the window
        for quitEvent in pygame.event.get():
            if quitEvent.type == pygame.QUIT:
                run = False

        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_a] and player.x - playerVelocity > 0: #moving left
            player.x -= playerVelocity
        if keyPressed[pygame.K_d] and player.x + playerVelocity + player.get_width() < WIDTH: #moving right
            player.x += playerVelocity
        if keyPressed[pygame.K_w] and player.y - playerVelocity > 0: #moving forward
            player.y -= playerVelocity
        if keyPressed[pygame.K_s] and player.y + playerVelocity + player.get_height() < HEIGHT: #moving downward
            player.y += playerVelocity
        if keyPressed[pygame.K_SPACE]:
            player.Shoot()

        for enemy in enemies[:]:
            enemy.move(enemyVelocity)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        redraw_Window()

# Calling the main function
main()