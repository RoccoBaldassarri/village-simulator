import json
import pygame

from core.game_state import GameState

TOOLBAR_HEIGHT = 60


class MapEditor:
    TILE_OPTIONS = ["grass", "dirt", "rock"]
    TILE_COLORS = {
        "grass": (86, 156, 86),
        "dirt": (139, 106, 68),
        "rock": (110, 110, 118),
    }

    def __init__(self, display_manager, map_path: str):
        self.display = display_manager
        self.map_path = map_path
        self.next_state = None

        self.tile_size, self.cols, self.rows, self.grid = self._load_map(map_path)
        self.selected_tile = "grass"

        self.tile_buttons = self._build_toolbar_buttons()
        self.save_button = pygame.Rect(display_manager.width - 170, 10, 150, 40)

    def _load_map(self, map_path: str):
        with open(map_path, "r") as f:
            data = json.load(f)
        grid = [[cell["type"] for cell in row] for row in data["grid"]]
        return data["tile_size"], data["cols"], data["rows"], grid

    def _save_and_exit(self):
        data = {
            "tile_size": self.tile_size,
            "cols": self.cols,
            "rows": self.rows,
            "grid": [[{"type": tile_type} for tile_type in row] for row in self.grid],
        }
        with open(self.map_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[MapEditor] Map saved in '{self.map_path}'")
        self.next_state = GameState.MENU

    def _build_toolbar_buttons(self) -> dict:
        buttons = {}
        x = 10
        for tile_type in self.TILE_OPTIONS:
            buttons[tile_type] = pygame.Rect(x, 10, 100, 40)
            x += 110
        return buttons

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return

        pos = event.pos

        for tile_type, rect in self.tile_buttons.items():
            if rect.collidepoint(pos):
                self.selected_tile = tile_type
                return

        if self.save_button.collidepoint(pos):
            self._save_and_exit()
            return

        self._handle_grid_click(pos)

    def _handle_grid_click(self, pos):
        x, y = pos
        y -= TOOLBAR_HEIGHT
        if y < 0:
            return

        col, row = x // self.tile_size, y // self.tile_size
        if 0 <= col < self.cols and 0 <= row < self.rows:
            self.grid[row][col] = self.selected_tile

    def update(self, dt):
        pass

    def draw(self):
        self.display.clear((15, 15, 20))
        self._draw_grid()
        self._draw_toolbar()

    def _draw_grid(self):
        screen = self.display.get_screen()
        for row_idx, row in enumerate(self.grid):
            for col_idx, tile_type in enumerate(row):
                rect = pygame.Rect(
                    col_idx * self.tile_size,
                    TOOLBAR_HEIGHT + row_idx * self.tile_size,
                    self.tile_size,
                    self.tile_size,
                )
                pygame.draw.rect(screen, self.TILE_COLORS[tile_type], rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, width=1)

    def _draw_toolbar(self):
        screen = self.display.get_screen()
        pygame.draw.rect(screen, (40, 40, 45), (0, 0, self.display.width, TOOLBAR_HEIGHT))

        for tile_type, rect in self.tile_buttons.items():
            is_selected = tile_type == self.selected_tile
            self.display.draw_button(
                rect, tile_type,
                font=self.display.font_small,
                bg_color=(90, 90, 95) if is_selected else (55, 55, 60),
            )

        self.display.draw_button(
            self.save_button, "Save and exit",
            font=self.display.font_small, bg_color=(50, 110, 60),
        )
