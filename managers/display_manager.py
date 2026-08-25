import pygame


class DisplayManager:
    def __init__(self, width: int, height: int, caption: str = "Village Simulator"):
        pygame.init()
        pygame.font.init()

        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()

        self.font_small = pygame.font.SysFont("arial", 18)
        self.font_medium = pygame.font.SysFont("arial", 28)
        self.font_large = pygame.font.SysFont("arial", 48)

    def get_screen(self) -> pygame.Surface:
        return self.screen

    def clear(self, color=(20, 20, 20)):
        self.screen.fill(color)

    def flip(self):
        pygame.display.flip()

    def tick(self, fps: int = 60) -> float:
        return self.clock.tick(fps) / 1000.0 * fps

    def draw_text(self, text: str, pos, font=None, color=(255, 255, 255)):
        font = font or self.font_medium
        surface = font.render(text, True, color)
        self.screen.blit(surface, pos)
        return surface.get_rect(topleft=pos)

    def draw_button(self, rect: pygame.Rect, text: str, font=None,
                     bg_color=(60, 60, 60), text_color=(255, 255, 255), hover=False):
        color = tuple(min(c + 30, 255) for c in bg_color) if hover else bg_color
        pygame.draw.rect(self.screen, color, rect, border_radius=6)
        pygame.draw.rect(self.screen, (200, 200, 200), rect, width=2, border_radius=6)

        font = font or self.font_medium
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
