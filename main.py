import os
import pygame

from managers.world_manager import WorldManager

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

MAP_PATH = os.path.join("assets", "map", "test_map.json")
TILE_TEXTURES = {
    "grass": os.path.join("assets", "images", "grass1.png"),
    "dirt": os.path.join("assets", "images", "dirt.png"),
}
NPC_TEXTURE_PATH = os.path.join("assets", "images", "npc_test.png")


def main():
    """
    Il Direttore d'Orchestra.

    Contiene SOLO: inizializzazione di pygame, creazione della facade
    WorldManager, game loop a 60 FPS, gestione eventi, e la sequenza
    update()/draw(). Nessuna logica di mappa, fisica o NPC vive qui.
    """
    pygame.init()
    #screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Village Simulator - MVP")
    clock = pygame.time.Clock()

    # --- Inizializzazione: un'unica facade costruisce tutto il mondo ---
    try:
        worldManager = WorldManager(MAP_PATH, TILE_TEXTURES, NPC_TEXTURE_PATH)
    except RuntimeError as e:
        print(f"Errore fatale durante la costruzione del mondo: {e}")
        pygame.quit()
        return

    # NPC di prova per validare end-to-end la pipeline spawn -> FSM -> collisioni -> draw
    worldManager.spawn_npc(col=2, row=0)
    worldManager.spawn_npc(col=5, row=3)

    running = True
    while running:
        # dt normalizzato: 1.0 = un frame a 60 FPS, così self.speed nell'NPC
        # resta indipendente dal framerate reale.
        dt = clock.tick(FPS) / 1000.0 * FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        worldManager.update(dt)

        screen.fill((0, 0, 0))
        worldManager.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()