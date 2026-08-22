import os
import json
import sys
import pygame

#load the map from the json
with open("assets/map/test_map.json", "r") as file:
    map_data = json.load(file)

TILE_SIZE = map_data["tile_size"]
GRID_COLS = map_data["cols"]
GRID_ROWS = map_data["rows"]
grid = map_data["grid"]

SCREEN_WIDTH = GRID_COLS * TILE_SIZE
SCREEN_HEIGHT = GRID_ROWS * TILE_SIZE

npc_col = 2
npc_row = 0

# npc pixel position 
npc_x = npc_col * TILE_SIZE
npc_y = npc_row * TILE_SIZE

def render_full_map(textures, map_surface):
        for row_idx, row in enumerate(grid):
            for col_idx, tile in enumerate(row):
                texture = textures[tile["type"]]
                map_surface.blit(texture, (col_idx * TILE_SIZE, row_idx * TILE_SIZE))

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Village Simulator - Tilemap")
    clock = pygame.time.Clock()

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

    textures = {
        "grass": pygame.transform.scale(
            pygame.image.load(grass_path).convert_alpha(), (TILE_SIZE, TILE_SIZE)
        ),
        "dirt": pygame.transform.scale(
            pygame.image.load(dirt_path).convert_alpha(), (TILE_SIZE, TILE_SIZE)
        )
    }


    # pre renderd background
    map_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    render_full_map(grid, row, textures, map_surface)

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

if __name__ == "__main__":
    main()