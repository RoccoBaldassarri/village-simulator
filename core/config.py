import os

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

MAP_PATH = os.path.join("assets", "map", "test_map.json")

TILE_TEXTURES = {
    "grass": os.path.join("assets", "images", "grass1.png"),
    "dirt": os.path.join("assets", "images", "dirt.png"),
    "rock": os.path.join("assets", "images", "rock.png"),
}

NPC_TEXTURE_PATH = os.path.join("assets", "images", "npc_test.png")
