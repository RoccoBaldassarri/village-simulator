import random
from enum import Enum, auto


class NPCState(Enum):
    """Stati della FSM. Punto di estensione per il futuro (es. SEEKING_FOOD)."""
    IDLE = auto()
    MOVING = auto()


class NPC:
    """
    Un singolo abitante del villaggio.

    Possiede DUE sistemi di coordinate:
      - col/row: posizione LOGICA sulla griglia (usata per collisioni e pathfinding).
      - x/y:     posizione FLUIDA in pixel (usata per il rendering e l'interpolazione
                 di movimento a 60 FPS, così lo spostamento tra due tile appare
                 uno scorrimento morbido e non un "teletrasporto").

    Comunicazione:
      - L'NPC NON conosce MapManager, PhysicsManager o NPCManager. Parla
        esclusivamente con l'oggetto `world` (la facade WorldManager) che
        gli viene passato in update(). Questo mantiene l'NPC completamente
        disaccoppiato dai dettagli implementativi del mondo.
    """

    def __init__(self, npc_id: int, col: int, row: int, tile_size: int, texture, speed: float = 3.0):
        self.id = npc_id
        self.tile_size = tile_size
        self.texture = texture
        self.speed = speed  # pixel per frame durante l'interpolazione

        # Posizione logica (griglia)
        self.col = col
        self.row = row

        # Posizione fluida (pixel) — parte allineata alla cella di spawn
        self.x = float(col * tile_size)
        self.y = float(row * tile_size)

        # Pixel target della cella verso cui l'NPC si sta muovendo in questo istante
        self.target_x = self.x
        self.target_y = self.y

        # Stato FSM
        self.state = NPCState.IDLE

        # Statistiche interne che guidano il comportamento
        self.stats = {
            "hunger": random.uniform(0, 20),
            "boredom": random.uniform(0, 20),
        }

        # Coda di passi (col, row) ancora da percorrere per raggiungere una destinazione
        self.path = []

    # ------------------------------------------------------------------ #
    # Ciclo di vita per frame (chiamato da NPCManager)
    # ------------------------------------------------------------------ #

    def update(self, dt: float, world):
        self._update_stats(dt)
        self._run_fsm(world)

    def draw(self, surface):
        surface.blit(self.texture, (self.x, self.y))

    # ------------------------------------------------------------------ #
    # Statistiche
    # ------------------------------------------------------------------ #

    def _update_stats(self, dt: float):
        self.stats["hunger"] += 0.05 * dt
        self.stats["boredom"] += 0.08 * dt

    # ------------------------------------------------------------------ #
    # Finite State Machine
    # ------------------------------------------------------------------ #

    def _run_fsm(self, world):
        if self.state == NPCState.IDLE:
            self._handle_idle(world)
        elif self.state == NPCState.MOVING:
            self._handle_moving(world)

    def _handle_idle(self, world):
        """
        MVP: se la noia supera una soglia, l'NPC decide di vagare verso una
        cella casuale. In futuro questa è la funzione da espandere per far
        scegliere all'NPC comportamenti diversi in base alle statistiche
        (es. hunger alto -> cerca un oggetto "cibo" interagibile).
        """
        if self.stats["boredom"] < 40:
            return

        destination = self._pick_random_destination(world)
        path = self._compute_naive_path(destination)

        if path:
            self.path = path
            self.state = NPCState.MOVING
            self.stats["boredom"] = 0

    def _handle_moving(self, world):
        # Se la posizione in pixel ha raggiunto il target della cella corrente,
        # bisogna decidere il prossimo passo (o tornare IDLE se il path è finito).
        if self.x == self.target_x and self.y == self.target_y:
            if not self.path:
                self.state = NPCState.IDLE
                return

            next_col, next_row = self.path[0]

            # Requisito chiave: PRIMA di impegnarsi a muoversi verso la prossima
            # cella, si richiede sempre conferma al mondo (PhysicsManager tramite
            # la facade). Questo copre il caso in cui, nel frattempo, un altro
            # NPC abbia occupato quella cella.
            if world.can_move_to(next_col, next_row, mover=self):
                self.path.pop(0)
                self.col, self.row = next_col, next_row
                self.target_x = float(next_col * self.tile_size)
                self.target_y = float(next_row * self.tile_size)
            else:
                # Passo bloccato: per l'MVP l'NPC abbandona il percorso e torna
                # IDLE. In futuro qui si può ricalcolare un path alternativo.
                self.path = []
                self.state = NPCState.IDLE
                return

        self._step_towards_target()

    # ------------------------------------------------------------------ #
    # Movimento pixel-per-pixel (interpolazione)
    # ------------------------------------------------------------------ #

    def _step_towards_target(self):
        self.x = self._move_axis(self.x, self.target_x)
        self.y = self._move_axis(self.y, self.target_y)

    def _move_axis(self, current: float, target: float) -> float:
        if current == target:
            return current
        step = self.speed if target > current else -self.speed
        if abs(step) >= abs(target - current):
            return target
        return current + step

    # ------------------------------------------------------------------ #
    # Pathfinding (placeholder MVP)
    # ------------------------------------------------------------------ #

    def _pick_random_destination(self, world) -> tuple:
        cols, rows = world.get_map_dimensions()
        return random.randint(0, cols - 1), random.randint(0, rows - 1)

    def _compute_naive_path(self, destination: tuple) -> list:
        """
        Path "ingenuo": una linea a gradini in stile Manhattan, senza
        evitamento ostacoli. Basta sostituire il corpo di questo metodo con
        un vero algoritmo (es. A*) per fare l'upgrade: il resto della FSM
        (_handle_moving) non deve cambiare, perché continua a consumare
        `self.path` un passo alla volta con la stessa interfaccia.
        """
        path = []
        col, row = self.col, self.row
        dest_col, dest_row = destination

        while col != dest_col:
            col += 1 if dest_col > col else -1
            path.append((col, row))

        while row != dest_row:
            row += 1 if dest_row > row else -1
            path.append((col, row))

        return path
