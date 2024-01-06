import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
pygame.init()
import random

pygame.display.set_caption("Shooter game")
screenWidth = 450
screenHeight = 640
window = pygame.display.set_mode((screenWidth, screenHeight))
backgroundImage = pygame.image.load(os.path.join(os.sys.path[0])+"/Assets/Background/background.png")
fps = 144

# Check for closing window
def closeWindowCheck():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global gaming
            gaming = False

# Player class
class playerClass():
    def __init__(self, y, width, height):
        self.playerImage = pygame.transform.scale(pygame.image.load(os.path.join(os.sys.path[0])+"/Assets/Player/player1.png"), (width, height))
        self.width = width
        self.height = height
        self.x = screenWidth/2-self.width/2
        self.y = y
        self.velocity = 800
        self.colour = (255, 0, 0)

    def controls(self):
        if pressedKeys[pygame.K_LEFT]:
            if self.x > self.velocity*dt:
                self.x -= self.velocity*dt
            else:
                self.x = 0
        elif pressedKeys[pygame.K_RIGHT]:
            if self.x < screenWidth-self.width-self.velocity*dt:
                self.x += self.velocity*dt
            else:
                self.x = screenWidth-self.width
        if pressedKeys[pygame.K_SPACE]:
            global projectileTimer
            if projectileTimer <= 0:
                projectileTimer = 20
                projectileList.append(projectileClass(player.x+player.width/2-16))
    def draw(self):
        window.blit(self.playerImage, (player.x, player.y))

class projectileClass():
    def __init__(self, x):
        self.projectileImage = pygame.image.load(os.path.join(os.sys.path[0])+"/Assets/Projectile/projectile.png")
        self.x = x
        self.y = player.y
        self.width = 33
        self.height = 54
        self.velocity = 1600
        self.hitbox = (self.x+self.width/2, self.y+self.height/3)
    def movement(self, projectile):
        if self.y > -99:
            self.y -= self.velocity*dt
        else:
            projectileList.pop(projectileList.index(projectile))
    def draw(self, window):
        window.blit(self.projectileImage, (self.x, self.y))
        self.hitbox = (self.x+self.width/2, self.y+self.height/3)
        if hitboxesOn == True:
            pygame.draw.circle(window, (255, 0, 0), self.hitbox, 16, 2)

class enemyClass():
    def __init__(self, velocity):
        self.enemyImage = pygame.image.load(os.path.join(os.sys.path[0])+"/Assets/Enemy/enemy.png")
        self.width = 65
        self.height = 99
        self.x = random.randint(player.width, screenWidth-player.width)
        self.y = -(self.height + random.randint(0, 60))
        self.velocity = velocity
        self.hitbox = (self.x+10, self.y, self.width-20, self.height-40)
    def movement(self):
        global running
        if self.y > screenHeight:
            running = False
        self.y += self.velocity*dt
    def draw(self):
        window.blit(self.enemyImage, (self.x, self.y))
        self.hitbox = (self.x+10, self.y, self.width-20, self.height-40)
        if hitboxesOn == True:
            pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

# Update changes
def updateChanges():
    player.controls()       # Move player
    for projectile in projectileList:       # Move projectiles
        projectile.movement(projectile)
    for enemy in enemyList:       # Move enemies
        enemy.movement()
    global projectileTimer      # Update projectile timer
    if projectileTimer > -20:
        projectileTimer -= 1
    collisionDetection()        # Detect collisions

# Collision detection
def collisionDetection():
    global enemyNumber
    killed = False
    for projectile in projectileList:
        for enemy in enemyList:
            if projectile.y - 16 < enemy.hitbox[1] + enemy.hitbox[3] and projectile.y + 16 > enemy.hitbox[1]:
                if projectile.x + 16 > enemy.hitbox[0] and projectile.x - 16 < enemy.hitbox[0] + enemy.hitbox[2]:
                    try:
                        enemyList.pop(enemyList.index(enemy))
                        projectileList.pop(projectileList.index(projectile))
                        enemyNumber = enemyNumber+1/(enemyNumber*10)
                    except:
                        pass
    if bool(enemyList) == False:
        global score
        global enemySpeed
        score += 1
        for i in range(int(enemyNumber)):
            enemyList.append(enemyClass(enemySpeed))
            enemySpeed += 8

# Updating graphics
def updateGraphics():
    window.blit(backgroundImage, (0, 0))        # Set background
    for projectile in projectileList:       # Draw projectiles
        projectile.draw(window)
    for enemy in enemyList:
        enemy.draw()
    player.draw()
    my_font = pygame.font.SysFont('Comic Sans MS', 25)
    text_surface = my_font.render("Score: "+str(score), False, (0, 0, 153))
    window.blit(text_surface, (10,0))
    pygame.display.update()

gaming = True
while gaming == True:
    # Generation
    player = playerClass(540, 90, 84)
    projectileList = []
    projectileTimer = 0
    enemyList = []
    enemySpeed = 400
    enemyList.append(enemyClass(enemySpeed))
    hitboxesOn = False
    score = 0
    enemyNumber = 1.5

    # Main loop
    running = True
    while running:
        dt = pygame.time.Clock().tick(fps)/1000
        pressedKeys = pygame.key.get_pressed()
        closeWindowCheck()
        collisionDetection()
        updateChanges()
        updateGraphics()
    print(f"Oh no! You missed one! Your score is {score}! Try again!")
pygame.quit()
