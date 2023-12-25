import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def gen(num):
    return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])

def draw_grid(positions):
    for position in positions:
        column, row = position
        top_left = (column * TILE_SIZE, row * TILE_SIZE)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Random color for each cell
        pygame.draw.rect(window, color, (*top_left, TILE_SIZE, TILE_SIZE))

def adjust_grid(positions):
    all_neighbors = set()
    new_positions = set()

    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) in [2,3]:
            new_positions.add(position)  

    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) == 3:
            new_positions.add(position)  

    return new_positions  

def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            if dx == 0 and dy ==0:
                continue

            neighbors.append((x+dx,y+dy))

    return neighbors

def main():
    running = True
    playing = True
    positions = set()
    count = 0
    update_freq = 50

    while running:
        clock.tick(FPS)

        if playing:
            count += 1

        if count >= update_freq:
            count = 0
            positions = adjust_grid(positions)

        pygame.display.set_caption("playing" if playing else 'paused')


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col,row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing
                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count == 0
                if event.key == pygame.K_g:
                    positions = gen(random.randrange(2,5)*GRID_WIDTH)


        window.fill('white')
        draw_grid(positions)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()