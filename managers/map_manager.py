import json
import pygame


class MapManager:
    """
    L'Archivista Statico.

    Responsabilità:
      - Caricare i dati grezzi della mappa dal JSON (griglia, dimensioni, tile_size).
      - Pre-renderizzare l'intera mappa su un'unica Surface (ottimizzazione: non
        ridisegniamo ogni tile ad ogni frame, lo facciamo una sola volta all'avvio).
      - Esporre lo stato STATICO dei blocchi (es. is_walkable), cioè tutto ciò che
        dipende solo dal terreno e non dal contenuto dinamico del mondo (NPC, oggetti).

    Comunicazione:
      - Viene interrogato da PhysicsManager per i controlli statici di collisione.
      - Non conosce l'esistenza di NPC, PhysicsManager o altro: è un modulo "a valle",
        completamente indipendente dal resto del gioco.
    """

    def __init__(self, map_path: str, tile_textures_paths: dict):
        self.map_path = map_path

        self._load_map_data()
        self._load_tile_definitions()

        self.textures = self._load_textures(tile_textures_paths)
        self.map_surface = self._prerender_map()

    # ------------------------------------------------------------------ #
    # Caricamento dati
    # ------------------------------------------------------------------ #

    def _load_map_data(self):
        try:
            with open(self.map_path, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(f"MapManager: impossibile caricare '{self.map_path}': {e}")

        self.tile_size = data["tile_size"]
        self.cols = data["cols"]
        self.rows = data["rows"]
        self.grid = data["grid"]  # lista di liste di dict {"type": "..."}

    def _load_tile_definitions(self):
        """
        Proprietà statiche per ogni tipo di tile.

        Questo è il punto di estensione pensato per il futuro: aggiungere un
        nuovo tipo di terreno (es. "water") o una nuova proprietà (es. "cost"
        per il pathfinding) richiede di toccare SOLO questo dizionario, nessun
        altro file del progetto.
        """
        self.tile_definitions = {
            "grass": {"walkable": True},
            "dirt": {"walkable": True},
            # Esempio di estensione futura:
            # "water": {"walkable": False},
            # "wall":  {"walkable": False},
        }

    def _load_textures(self, tile_textures_paths: dict) -> dict:
        textures = {}
        try:
            for tile_type, path in tile_textures_paths.items():
                image = pygame.image.load(path).convert_alpha()
                textures[tile_type] = pygame.transform.scale(
                    image, (self.tile_size, self.tile_size)
                )
        except pygame.error as e:
            raise RuntimeError(f"MapManager: errore caricamento texture tile: {e}")
        return textures

    def _prerender_map(self) -> pygame.Surface:
        """
        Disegna l'intera griglia UNA SOLA VOLTA su una Surface dedicata,
        dimensionata esattamente sulla mappa (cols * tile_size, rows * tile_size).
        Ad ogni frame verrà fatto un singolo blit di questa Surface, invece di
        ridisegnare centinaia di tile singolarmente.
        """
        surface = pygame.Surface((self.cols * self.tile_size, self.rows * self.tile_size))
        for row_idx, row in enumerate(self.grid):
            for col_idx, tile in enumerate(row):
                texture = self.textures[tile["type"]]
                surface.blit(texture, (col_idx * self.tile_size, row_idx * self.tile_size))
        return surface

    # ------------------------------------------------------------------ #
    # Interfaccia pubblica (usata da PhysicsManager e WorldManager)
    # ------------------------------------------------------------------ #

    def get_map_surface(self) -> pygame.Surface:
        return self.map_surface

    def is_inside_bounds(self, col: int, row: int) -> bool:
        return 0 <= col < self.cols and 0 <= row < self.rows

    def is_walkable(self, col: int, row: int) -> bool:
        """
        Controllo STATICO: dipende solo dal tipo di terreno.
        Non sa nulla di NPC o altre entità: quella parte è compito del
        PhysicsManager, che compone questo risultato con il controllo dinamico.
        """
        if not self.is_inside_bounds(col, row):
            return False
        tile_type = self.grid[row][col]["type"]
        return self.tile_definitions.get(tile_type, {}).get("walkable", False)
