import pygame, random, sys
from pygame.math import Vector2

class MOUSE:
    def __init__(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.position = Vector2(self.x, self.y)

    def make_mouse(self):
        mouse_rect = pygame.Rect(self.position.x * cell_size, self.position.y * cell_size, cell_size,cell_size)
        pygame.draw.rect(screen, (126,166,114),mouse_rect)

class Snake:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(6,10), Vector2(7,10)]
        self.direction = Vector2(1,0)
    def make_pysnake(self):
        for block in self.body:
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos,cell_size,cell_size)
            pygame.draw.rect(screen,(126, 111,144), block_rect)

    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0,body_copy[0] + self.direction)   
        self.body = body_copy[:] 

pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
pygame.display.set_caption("Pysnake")


mouse = MOUSE()
snake = Snake()

SCREENUPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREENUPDATE, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREENUPDATE:
                snake.move_snake()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                    snake.direction = Vector2(0,-1)
            elif event.key == pygame.K_RIGHT:
                    snake.direction == Vector2(1,0)
            elif event.key == pygame.K_DOWN:
                    snake.direction = Vector2(0,1)
            elif event.key == pygame.K_LEFT:
                    snake.direction == Vector2(-1,0)
            

    screen.fill(pygame.Color((175, 215,70)))
    mouse.make_mouse()
    snake.make_pysnake()
    pygame.display.update()

pygame.quit()