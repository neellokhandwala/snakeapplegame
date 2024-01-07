import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (	186, 22, 12)
GREEN = (0, 73, 83)

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([0, 1, 2, 3])  # 0: UP, 1: DOWN, 2: LEFT, 3: RIGHT
        self.color = GREEN

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction_to_vector()
        new = (((cur[0] + (x * GRID_SIZE)) % WIDTH), (cur[1] + (y * GRID_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([0, 1, 2, 3])

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], GRID_SIZE, GRID_SIZE))

    def direction_to_vector(self):
        if self.direction == 0:
            return 0, -1
        elif self.direction == 1:
            return 0, 1
        elif self.direction == 2:
            return -1, 0
        elif self.direction == 3:
            return 1, 0

# Apple class
class Apple:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                         random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

# Main function
def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    # Load background image
    background = pygame.image.load("lawn.jpeg")  # Replace "background.jpg" with your image file
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    snake = Snake()
    apple = Apple()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if snake.direction != 1:
                        snake.direction = 0
                elif event.key == pygame.K_DOWN:
                    if snake.direction != 0:
                        snake.direction = 1
                elif event.key == pygame.K_LEFT:
                    if snake.direction != 3:
                        snake.direction = 2
                elif event.key == pygame.K_RIGHT:
                    if snake.direction != 2:
                        snake.direction = 3

        snake.update()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Draw background
        surface.blit(background, (0, 0))

        snake.render(surface)
        apple.render(surface)
        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
