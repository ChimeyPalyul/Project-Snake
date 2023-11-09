import pygame, random, sys
from pygame.math import Vector2
from users import Score, engine, add_score
from sqlalchemy.orm import Session
def game(user):
    score = 0
    class MOUSE:
        def __init__(self):
            self.randomize()

        def make_mouse(self):
            mouse_rect = pygame.Rect(int(self.position.x * cell_size), int(self.position.y * cell_size), cell_size,cell_size)
            screen.blit(usable_rodent,mouse_rect)
            # pygame.draw.rect(screen,(126,166,114), mouse_rect)

        def randomize(self):
            self.x = random.randint(0, cell_number - 1)
            self.y = random.randint(0, cell_number - 1)
            self.position = Vector2(self.x, self.y)

    class Snake:
        def __init__(self):
            self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
            self.direction = Vector2(1,0)
            self.new_tail = False

            self.snake_head_down = pygame.image.load("Graphics/snake1_head_down.png").convert_alpha()
            self.snake_head_up = pygame.image.load("Graphics/snake1_head.png").convert_alpha()
            self.snake_head_left = pygame.image.load('Graphics/snake1_head_left.png').convert_alpha()
            self.snake_head_right = pygame.image.load('Graphics/snake1_head_right.png').convert_alpha()
            
            self.usable_snake_head_down = pygame.transform.scale(self.snake_head_down, (40,40))
            self.usable_snake_head_right = pygame.transform.scale(self.snake_head_right, (40,40))
            self.usable_snake_head_up = pygame.transform.scale(self.snake_head_up, (40,40))
            self.usable_snake_head_left = pygame.transform.scale(self.snake_head_left, (40,40))

            self.snake_tail_left = pygame.image.load("Graphics/snake1_left_tail.png").convert_alpha()
            self.snake_tail_right = pygame.image.load("Graphics/snake1_right_tail.png").convert_alpha()
            self.snake_tail_down = pygame.image.load("Graphics/snake1_down_tail.png").convert_alpha()
            self.snake_tail_up = pygame.image.load('Graphics/snake1_tail.png').convert_alpha()

            self.usable_snake_tail_left = pygame.transform.scale(self.snake_tail_left, (40,40))
            self.usable_snake_tail_right = pygame.transform.scale(self.snake_tail_right, (40,40))
            self.usable_snake_tail_down = pygame.transform.scale(self.snake_tail_down, (40,40))
            self.usable_snake_tail_up = pygame.transform.scale(self.snake_tail_up, (40,40))

            #usable_snake_tail = pygame.transform.scale(snake_tail, (40,40))
            self.body_vertical = pygame.image.load('Graphics/snake_body.png').convert_alpha()
            self.body_horizontal = pygame.image.load('Graphics/snake_left_body.png').convert_alpha()
        
            self.usable_body_vertical = pygame.transform.scale(self.body_vertical, (40,50))
            self.usable_body_horizontal = pygame.transform.scale(self.body_horizontal, (40,40))

        def make_pysnake(self):
            self.update_head_graphics()
            self.update_tail_graphics()

            for index, block in enumerate(self.body):
                x_pos = int(block.x * cell_size)
                y_pos = int(block.y * cell_size)
                block_rect = pygame.Rect(x_pos, y_pos,cell_size,cell_size)

                if index == 0:
                    screen.blit(self.head,block_rect)
                elif index == len(self.body) -1:
                    screen.blit(self.tail,block_rect)
                else:
                    last_block = self.body[index + 1] - block
                    next_block = self.body[index - 1] - block
                    if last_block.x == next_block.x:
                        screen.blit(self.usable_body_vertical,block_rect)
                    if last_block.y == next_block.y:
                        screen.blit(self.usable_body_horizontal,block_rect)

                    

        def update_head_graphics(self):
            head_relation = self.body[1] - self.body[0]
            if head_relation == Vector2(1,0): self.head = self.usable_snake_head_left
            elif head_relation == Vector2(-1,0): self.head = self.usable_snake_head_right
            elif head_relation == Vector2(0,1): self.head = self.usable_snake_head_up
            elif head_relation == Vector2(0,-1): self.head = self.usable_snake_head_down

        def update_tail_graphics(self):
            tail_relation = self.body[-2] - self.body[-1]
            if tail_relation == Vector2(1,0): self.tail = self.usable_snake_tail_right
            elif tail_relation == Vector2(-1,0): self.tail = self.usable_snake_tail_left
            elif tail_relation == Vector2(0,1): self.tail = self.usable_snake_tail_down
            elif tail_relation == Vector2(0,-1): self.tail = self.usable_snake_tail_up
            

        def move_snake(self):
            if self.new_tail == True:
                body_copy = self.body[:]
                body_copy.insert(0,body_copy[0] + self.direction)   
                self.body = body_copy[:]
                self.new_tail = False
            else:
                body_copy = self.body[:-1]
                body_copy.insert(0,body_copy[0] + self.direction)   
                self.body = body_copy[:] 
        
        def add_tail(self):
            self.new_tail = True

        def reset(self):
            self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
            self.direction = Vector2(0,0)
            print(Main.total)
            
            

    class Main:
        total = score
        def __init__(self, user):
            self.snake = Snake()
            self.mouse = MOUSE()
            Main.total = 0
            self.user = user
            

        def update(self):
            self.snake.move_snake()
            self.on_collision()
            self.fail()
        
        def draw_elements(self):
            self.draw_grass()
            self.mouse.make_mouse()
            self.snake.make_pysnake()
            self.keep_score()

        def on_collision(self):
            if self.mouse.position == self.snake.body[0]:
                self.mouse.randomize()
                self.snake.add_tail()
                Main.total += 1
            
            for block in self.snake.body[1:]:
                if block == self.mouse.position:
                    self.mouse.randomize()

        def fail(self):
            if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
                self.game_over()
            for block in self.snake.body[1:]:
                if block == self.snake.body[0]:
                    self.game_over()

        
        def game_over(self):
            print(Main.total)
            add_score(self.user.username, Main.total)
            self.snake.reset()


        def keep_score(self):
            score_text = str(len(self.snake.body) -3)
            score_surface = game_font.render(score_text, True, (56,74,12))
            score_x = int(cell_size * cell_number - 60)
            score_y = int(cell_size * cell_number -40)
            score_rect = score_surface.get_rect(center = (score_x, score_y))
            screen.blit(score_surface, score_rect)
        
        def draw_grass(self):
            grass_color = (167, 209, 61)
            for row in range(cell_number):
                if row % 2 == 0:
                    for col in range(cell_number):
                        if col % 2 == 0: 
                            grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size,cell_size)
                            pygame.draw.rect(screen, grass_color, grass_rect)
                else:
                    if row % 2 == 0:
                        for col in range(cell_number):
                            if col % 2 != 0: 
                                grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size,cell_size)
                                pygame.draw.rect(screen, grass_color, grass_rect)


    pygame.init()
    cell_size = 40
    cell_number = 20
    screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
    clock = pygame.time.Clock()
    rodent = pygame.image.load('Graphics/rat_pic_2.png').convert_alpha()
    usable_rodent = pygame.transform.scale(rodent,(40,40))
    game_font = pygame.font.Font(None, 25)
    pygame.display.set_caption("Pysnake")

    SCREENUPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREENUPDATE, 200)

    main_game = Main(user)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREENUPDATE:
                    main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                        if main_game.snake.direction.y != 1:
                            main_game.snake.direction = Vector2(0,-1)
                elif event.key == pygame.K_RIGHT:
                        if main_game.snake.direction.x != -1:
                            main_game.snake.direction = Vector2(1,0)
                elif event.key == pygame.K_DOWN:
                        if main_game.snake.direction.y != -1:
                            main_game.snake.direction = Vector2(0,1)
                elif event.key == pygame.K_LEFT:
                        if main_game.snake.direction.x != 1:
                            main_game.snake.direction = Vector2(-1,0)
                

        screen.fill((175,215,70))
        main_game.draw_elements()
        pygame.display.update()

    pygame.quit()
