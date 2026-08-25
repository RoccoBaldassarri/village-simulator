import pygame

from core.game_state import GameState

class MainMenu:
    def __init__(self, display_manager):
        self.display = display_manager
        self.next_state = None

        w, h = display_manager.width, display_manager.height
        btn_w, btn_h = 280, 60
        cx = w // 2 - btn_w // 2

        self.start_button = pygame.Rect(cx, h // 2 - 40, btn_w, btn_h)
        self.editor_button = pygame.Rect(cx, h // 2 + 40, btn_w, btn_h)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.start_button.collidepoint(event.pos):
                self.next_state = GameState.SIMULATION
            elif self.editor_button.collidepoint(event.pos):
                self.next_state = GameState.MAP_EDITOR

    def update(self, dt):
        pass

    def draw(self):
        self.display.clear((25, 25, 35))
        self.display.draw_text(
            "Village Simulator",
            (self.display.width // 2 - 150, 120),
            font=self.display.font_large,
        )

        mouse_pos = pygame.mouse.get_pos()
        self.display.draw_button(
            self.start_button, "Start",
            hover=self.start_button.collidepoint(mouse_pos),
        )
        self.display.draw_button(
            self.editor_button, "Map editor",
            hover=self.editor_button.collidepoint(mouse_pos),
        )
