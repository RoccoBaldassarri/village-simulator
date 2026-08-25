import json
import pygame


class MapManager:
    PLACEHOLDER_COLORS = {
        "grass": (86, 156, 86),
        "dirt": (139, 106, 68),
        "rock": (110, 110, 118),
    }

    def __init__(self, map_path: str, tile_textures_paths: dict):
        self.map_path = map_path

        self._load_map_data()
        self._load_tile_definitions()

        self.textures = self._load_textures(tile_textures_paths)
        self.map_surface = self._prerender_map()

    def _load_map_data(self):
        try:
            with open(self.map_path, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(f"MapManager: impossibile caricare '{self.map_path}': {e}")

        self.tile_size = data["tile_size"]
        self.cols = data["cols"]
        self.rows = data["rows"]
        self.grid = data["grid"]

    def _load_tile_definitions(self):
        self.tile_definitions = {
            "grass": {"walkable": True},
            "dirt": {"walkable": True},
            "rock": {"walkable": False},
        }

    def _load_textures(self, tile_textures_paths: dict) -> dict:
        textures = {}
        for tile_type, path in tile_textures_paths.items():
            try:
                image = pygame.image.load(path).convert_alpha()
                textures[tile_type] = pygame.transform.scale(image, (self.tile_size, self.tile_size))
            except (pygame.error, FileNotFoundError):
                textures[tile_type] = self._make_placeholder_texture(tile_type)
        return textures

    def _make_placeholder_texture(self, tile_type: str) -> pygame.Surface:
        color = self.PLACEHOLDER_COLORS.get(tile_type, (150, 150, 150))
        surface = pygame.Surface((self.tile_size, self.tile_size))
        surface.fill(color)
        pygame.draw.rect(surface, (0, 0, 0), surface.get_rect(), width=1)
        return surface

    def _prerender_map(self) -> pygame.Surface:
        surface = pygame.Surface((self.cols * self.tile_size, self.rows * self.tile_size))
        for row_idx, row in enumerate(self.grid):
            for col_idx, tile in enumerate(row):
                texture = self.textures[tile["type"]]
                surface.blit(texture, (col_idx * self.tile_size, row_idx * self.tile_size))
        return surface

    def get_map_surface(self) -> pygame.Surface:
        return self.map_surface

    def is_inside_bounds(self, col: int, row: int) -> bool:
        return 0 <= col < self.cols and 0 <= row < self.rows

    def is_walkable(self, col: int, row: int) -> bool:
        if not self.is_inside_bounds(col, row):
            return False
        tile_type = self.grid[row][col]["type"]
        return self.tile_definitions.get(tile_type, {}).get("walkable", False)