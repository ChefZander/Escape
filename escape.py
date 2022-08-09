# ESCAPE
# by https://github.com/ChefZander
# licensed under LGPL v2.1

print("[Escape] Starting")
from site import ENABLE_USER_SITE
import pygame
from pygame.locals import *
from pygame import *
import sys, random

ENABLE_DEBUG_OUTPUT = False

def dbg(msg):
    if ENABLE_DEBUG_OUTPUT: print("[DEBUG]" + msg)
def randCoord():
    return (random.randint(0,639), random.randint(0,480))

dbg("[Main] Init Colors")
WHITE =     (255, 255, 255)
BLUE =      (  0,   0, 255)
GREEN =     (  0, 255,   0)
RED =       (255,   0,   0)
BLACK =     (  0,   0,   0)

dbg("[Main] Init GameObject")
class GameObject:
    def __init__(self, name="") -> None:
        pass#dbg(f"[Engine] initializing game object, given name \"{name}\"")
    def draw(self): pass
dbg("[Main] Init Player")
class Player(GameObject):
    def __init__(self, name="Player") -> None:
        super().__init__(name)
    def draw(self):
        p = pygame.mouse.get_pos()
        pygame.draw.circle(screen, WHITE, p, 10)
dbg("[Main] Init CircleEnemy")
class CircleEnemy(GameObject):
    phase = 0
    phaseTick = 0
    x,y = 0,0
    def __init__(self, x, y, name="CircleEnemy", lifetime=60) -> None:
        super().__init__(name)
        self.x, self.y = x, y
        self.lifetime = lifetime
    def draw(self):
        self.phaseTick += 1
        if self.phaseTick == self.lifetime:
            self.phase += 1
        if self.phaseTick == self.lifetime + 60:
            self.phase += 1
        
        if self.phase == 0:
            pygame.draw.circle(screen, BLUE, (self.x, self.y), 20)
        elif self.phase == 1:
            pygame.draw.circle(screen, RED, (self.x, self.y), 25)
dbg("[Main] Init LineEnemy")
class LineEnemy(GameObject):
    phase = 0
    phaseTick = 0
    x,y = 0,0
    def __init__(self, c1, c2, name="LineEnemy", lifetime=60) -> None:
        super().__init__(name)
        self.c1 = c1
        self.c2 = c2
        self.lifetime = lifetime
    def draw(self):
        self.phaseTick += 1
        if self.phaseTick == self.lifetime:
            self.phase += 1
        if self.phaseTick == self.lifetime + 60:
            self.phase += 1
        
        if self.phase == 0:
            pygame.draw.line(screen, BLUE, self.c1, self.c2, width=10)
        elif self.phase == 1:
            pygame.draw.line(screen, RED, self.c1, self.c2, width=15)

dbg("[PyGame] initializing")
dbg("[PyGame] pygame init")
pygame.init()
dbg("[PyGame] pygame font init")
pygame.font.init()

dbg("[PyGame] pygame display setup")
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Escape")

dbg("[Engine] init objects normal")
objects = []
for i in range(5):
    objects.append(CircleEnemy(random.randint(0,639), random.randint(0,480), lifetime=random.randint(30,120)))
objects.append(LineEnemy(randCoord(), randCoord(), lifetime=random.randint(30,120)))

dbg("[Engine] init objects drawcall priority")
priorityObjects = []
priorityObjects.append(Player())

dbg("[Engine] launching main game loop")
fc = 0
while True:
    for event in pygame.event.get():
        if event.type is QUIT:
            dbg("[Engine] received event quit")
            print("[Escape] Shutting down.")
            dbg("[PyGame] quitting")
            pygame.quit()
            dbg("[Main] exiting")
            sys.exit()
    c:Color = screen.get_at(pygame.mouse.get_pos())
    if c==Color(RED):
        print("[Escape] You Died!")
        dbg("[Engine] sending quit event")
        pygame.event.post(pygame.event.Event(QUIT, {}))
    screen.fill(BLACK)
    for o in priorityObjects:
        o.draw()
    for o in objects:
        o.draw()
        if isinstance(o, CircleEnemy):
            if o.phase == 2:
                objects.remove(o)
                objects.append(CircleEnemy(random.randint(0,639), random.randint(0,480), lifetime=random.randint(30,120)))
        if isinstance(o, LineEnemy):
            if o.phase == 2:
                objects.remove(o)
                objects.append(LineEnemy(randCoord(), randCoord(), lifetime=random.randint(30,120)))
    fc += 1
    if fc % 100 == 0:
        if random.randint(0, 1) == 0:
            objects.append(LineEnemy(randCoord(), randCoord(), lifetime=random.randint(30,120)))
        else:
            objects.append(CircleEnemy(random.randint(0,639), random.randint(0,480), lifetime=random.randint(30,120)))
    pygame.display.flip()
    pygame.display.update()
    pygame.time.delay(20)