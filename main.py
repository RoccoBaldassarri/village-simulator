import os
import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Village Simulator - Tilemap")
clock = pygame.time.Clock()

TILE_SIZE = 64

grass_path = os.path.join("assets", "images", "grass1.png")
dirt_path = os.path.join("assets", "images", "dirt.png")
npc_path = os.path.join("assets", "images", "npc_test.png")

try:
    grass_original = pygame.image.load(grass_path).convert_alpha()
    grass_tile = pygame.transform.scale(grass_original, (TILE_SIZE, TILE_SIZE))

    dirt_original = pygame.image.load(dirt_path).convert_alpha()
    dirt_tile = pygame.transform.scale(dirt_original, (TILE_SIZE, TILE_SIZE))
    
    
    npc_original = pygame.image.load(npc_path).convert_alpha()
    npc_image = pygame.transform.scale(npc_original, (TILE_SIZE, TILE_SIZE))

except pygame.error as e:
    print(f"Error: {e}")
    pygame.quit()
    exit()

# map test
map_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

npc_col = 2
npc_row = 0

# npc pixel position 
npc_x = npc_col * TILE_SIZE
npc_y = npc_row * TILE_SIZE

# pre renderd background
map_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

for row_index, row in enumerate(map_data):
    for col_index, tile_type in enumerate(row):
        x = col_index * TILE_SIZE
        y = row_index * TILE_SIZE
        
        if tile_type == 0:
            map_surface.blit(grass_tile, (x, y))
        elif tile_type == 1:
            map_surface.blit(dirt_tile, (x, y))


running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(map_surface, (0, 0))

    screen.blit(npc_image, (npc_x, npc_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()