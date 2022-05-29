from cmath import pi
from re import I
import sys, pygame, math, random
from time import sleep
from enum import Enum

WINDOWWITH = 800
WINDOWHEIGHT = 600
pygame.init()

class Direction(Enum):
    NO_DERECTION = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    UP_LEFT = 5
    UP_RIGHT = 6
    DOWN_LEFT = 7
    DOWN_RIGHT = 8




class Block:

    def __init__(self) -> None:
        # The reference point is the upper left corner.
        self.color = pygame.Color(64, 224, 205)
        self.x = WINDOWWITH // 2
        self.y = WINDOWHEIGHT // 2
        self.width = 15
        self.height = 15
        self.speed = 3.5
        self.direction = Direction.NO_DERECTION

    def move_on(self):
        def move_x(x):
            if self.x + x > 0 and self.x + x + self.width < WINDOWWITH:
                self.x += x
            else:
                pass
        def move_y(y):
            if self.y + y > 0 and self.y + y + self.height < WINDOWHEIGHT:
                self.y += y
            else:
                pass
        sin45 = math.sin(pi / 2)
        if self.direction != Direction.NO_DERECTION:
            # Determine if the Block can move.
            if self.direction == Direction.UP:
                move_y(-self.speed)
            if self.direction == Direction.DOWN:
                move_y(self.speed)
            if self.direction == Direction.LEFT:
                move_x(-self.speed)
            if self.direction == Direction.RIGHT:
                move_x(self.speed)
            if self.direction == Direction.UP_LEFT:
                move_x(-self.speed * sin45)
                move_y(-self.speed * sin45)
            if self.direction == Direction.UP_RIGHT:
                move_x(self.speed * sin45)
                move_y(-self.speed * sin45)
            if self.direction == Direction.DOWN_LEFT:
                move_x(-self.speed * sin45)
                move_y(self.speed * sin45)
            if self.direction == Direction.DOWN_RIGHT:
                move_x(self.speed * sin45)
                move_y(self.speed * sin45)

    def set_direction(self, direction):
        self.direction = direction


class Bullet:

    def __init__(self) -> None:
        self.color = pygame.Color(255, 0, 0)
        self.height = 3
        self.width = 3
        self.speed = 4
        self.placed_randomly()

    def placed_randomly(self):
        r = random.randrange(0, 2 * (WINDOWHEIGHT + WINDOWWITH))
        if r < WINDOWHEIGHT:
            self.x = 0
            self.y = r
        elif r < WINDOWHEIGHT * 2:
            self.x = WINDOWWITH
            self.y = r - WINDOWWITH
        elif r < WINDOWHEIGHT * 2 + WINDOWWITH:
            self.x = r - WINDOWHEIGHT * 2
            self.y = 0
        else:
            self.x = r - WINDOWHEIGHT * 2 + WINDOWWITH
            self.y = WINDOWHEIGHT

        angle = random.random() * 2 * pi
        self.speed_x = self.speed * math.cos(angle)
        self.speed_y = self.speed * math.sin(angle)

    def move_on(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x < 0 or self.x > WINDOWWITH or self.y < 0 or self.y > WINDOWHEIGHT:
            self.placed_randomly()


def game_init():
    global screen, clock, block, bullet_amount, bullet_list, pause, score, time
    screen = pygame.display.set_mode((WINDOWWITH, WINDOWHEIGHT))  # size
    clock = pygame.time.Clock()
    block = Block()
    bullet_amount = 20
    bullet_list = [Bullet() for _ in range(bullet_amount)]
    pause = False
    score = 0
    time = 0


game_init()


def game_over():
    global screen, pause
    pause = True
    f1 = pygame.font.Font(
        r'C:\Users\45101\AppData\Local\Microsoft\Windows\Fonts\minecraft.ttf',
        60)
    text = f1.render("GAME OVER!", False, (255, 0, 0), (0, 0, 0))
    f2 = pygame.font.Font(
        r'C:\Users\45101\AppData\Local\Microsoft\Windows\Fonts\minecraft.ttf',
        30)
    score_text = f2.render("YOUR SCORE: %.1f" % score, False, (255, 0, 0),
                           (0, 0, 0))
    f3 = pygame.font.Font(
        r'C:\Users\45101\AppData\Local\Microsoft\Windows\Fonts\minecraft.ttf',
        20)
    promot_text = f3.render("Press SPACE to restart . . .", False, (255, 0, 0),
                           (0, 0, 0))
    textRect = text.get_rect()
    score_textRect = score_text.get_rect()
    promot_textRect = promot_text.get_rect()
    textRect.center = (WINDOWWITH // 2, 100)
    score_textRect.center = (WINDOWWITH // 2, 150)
    promot_textRect.center = (WINDOWWITH // 2, 500)
    screen.blit(text, textRect)
    screen.blit(score_text, score_textRect)
    screen.blit(promot_text, promot_textRect)
    # Show the text immediately.
    pygame.display.update()


def jugde_collision():
    for i in range(bullet_amount):
        if (bullet_list[i].x > block.x
                and bullet_list[i].x < block.x + block.width
                and bullet_list[i].y > block.y
                and bullet_list[i].y < block.y + block.height):
            game_over()


def bullet_increase():
    global bullet_list, bullet_amount
    bullet_list += [Bullet() for _ in range(2)]
    bullet_amount += 2


def update():
    global score, time
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_UP] and keys_pressed[pygame.K_LEFT]:
        block.set_direction(Direction.UP_LEFT)
    elif keys_pressed[pygame.K_UP] and keys_pressed[pygame.K_RIGHT]:
        block.set_direction(Direction.UP_RIGHT)
    elif keys_pressed[pygame.K_DOWN] and keys_pressed[pygame.K_LEFT]:
        block.set_direction(Direction.DOWN_LEFT)
    elif keys_pressed[pygame.K_DOWN] and keys_pressed[pygame.K_RIGHT]:
        block.set_direction(Direction.DOWN_RIGHT)
    elif keys_pressed[pygame.K_UP]:
        block.set_direction(Direction.UP)
    elif keys_pressed[pygame.K_DOWN]:
        block.set_direction(Direction.DOWN)
    elif keys_pressed[pygame.K_LEFT]:
        block.set_direction(Direction.LEFT)
    elif keys_pressed[pygame.K_RIGHT]:
        block.set_direction(Direction.RIGHT)
    else:
        block.set_direction(Direction.NO_DERECTION)

    if time % 60 == 0:
        bullet_increase()
    block.move_on()
    [bullet_list[i].move_on() for i in range(bullet_amount)]
    screen.fill('black')
    pygame.draw.rect(screen, block.color,
                     (block.x, block.y, block.width, block.height), 0)
    [
        pygame.draw.rect(screen, bullet_list[i].color,
                         (bullet_list[i].x, bullet_list[i].y,
                          bullet_list[i].width, bullet_list[i].height), 0)
        for i in range(bullet_amount)
    ]
    jugde_collision()
    score += 0.1
    time += 1


while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not pause:
        update()
    else:
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            game_init()

    pygame.display.update()