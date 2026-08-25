import pygame

from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, MAP_PATH
from core.game_state import GameState
from managers.display_manager import DisplayManager
from ui.main_menu import MainMenu
from ui.map_editor import MapEditor
from ui.gameplay_scene import GameplayScene


def create_scene(state: GameState, display: DisplayManager):
    if state == GameState.MENU:
        return MainMenu(display)
    if state == GameState.MAP_EDITOR:
        return MapEditor(display, MAP_PATH)
    if state == GameState.SIMULATION:
        return GameplayScene(display)
    raise ValueError(f"Stato di gioco sconosciuto: {state}")


def main():
    display = DisplayManager(SCREEN_WIDTH, SCREEN_HEIGHT, "Village Simulator")

    current_state = GameState.MENU
    scene = create_scene(current_state, display)

    running = True
    while running:
        dt = display.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                scene.handle_event(event)

        scene.update(dt)
        scene.draw()
        display.flip()

        if scene.next_state is not None and scene.next_state != current_state:
            current_state = scene.next_state
            scene = create_scene(current_state, display)

    pygame.quit()


if __name__ == "__main__":
    main()