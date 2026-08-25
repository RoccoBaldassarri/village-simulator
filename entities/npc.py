import random
from enum import Enum, auto

from core.pathfinding import bfs_path
from entities.inventory import Inventory


class NPCState(Enum):
    IDLE = auto()
    MOVING = auto()


class NPC:
    INVENTORY_PRINT_INTERVAL_SECONDS = 2.0
    ASSUMED_FPS = 60

    def __init__(self, npc_id: int, col: int, row: int, tile_size: int, texture, speed: float = 3.0):
        self.id = npc_id
        self.tile_size = tile_size
        self.texture = texture
        self.speed = speed
        self.col = col
        self.row = row

        self.x = float(col * tile_size)
        self.y = float(row * tile_size)

        self.target_x = self.x
        self.target_y = self.y

        self.state = NPCState.IDLE

        self.stats = {
            "hunger": random.uniform(0, 20),
            "boredom": random.uniform(0, 20),
        }

        self.path = []
        self.inventory = Inventory()
        self.pending_item_target = None
        self._inventory_print_timer = 0.0

    def update(self, dt: float, world):
        self._update_stats(dt)
        self._update_inventory_debug_timer(dt)
        self._run_fsm(world)

    def draw(self, surface):
        surface.blit(self.texture, (self.x, self.y))

    def _update_stats(self, dt: float):
        self.stats["hunger"] += 0.05 * dt
        self.stats["boredom"] += 0.08 * dt

    def _update_inventory_debug_timer(self, dt: float):
        self._inventory_print_timer += dt / self.ASSUMED_FPS
        if self._inventory_print_timer >= self.INVENTORY_PRINT_INTERVAL_SECONDS:
            self._inventory_print_timer -= self.INVENTORY_PRINT_INTERVAL_SECONDS
            print(f"[NPC {self.id}] Inventario -> {self.inventory}")

    def _run_fsm(self, world):
        if self.state == NPCState.IDLE:
            self._handle_idle(world)
        elif self.state == NPCState.MOVING:
            self._handle_moving(world)

    def _handle_idle(self, world):
        target_item = world.get_nearest_item(self.col, self.row)
        if target_item is not None:
            path = self._compute_path_to((target_item.col, target_item.row), world)
            if path:
                self.path = path
                self.pending_item_target = target_item
                self.state = NPCState.MOVING
            return
        
        if self.stats["boredom"] < 40:
            return

        destination = self._pick_random_destination(world)
        path = self._compute_path_to(destination, world)
        if path:
            self.path = path
            self.pending_item_target = None
            self.state = NPCState.MOVING
            self.stats["boredom"] = 0

    def _handle_moving(self, world):
        if self.x == self.target_x and self.y == self.target_y:
            if not self.path:
                self._on_path_completed(world)
                return

            next_col, next_row = self.path[0]

            if world.can_move_to(next_col, next_row, mover=self):
                self.path.pop(0)
                self.col, self.row = next_col, next_row
                self.target_x = float(next_col * self.tile_size)
                self.target_y = float(next_row * self.tile_size)
            else:
                self.path = []
                self.pending_item_target = None
                self.state = NPCState.IDLE
                return

        self._step_towards_target()

    def _on_path_completed(self, world):
        if self.pending_item_target is not None:
            still_there = world.get_item_at(self.col, self.row)
            if still_there is self.pending_item_target:
                world.collect_item(still_there)
                self.inventory.add_item(still_there)
            self.pending_item_target = None
        self.state = NPCState.IDLE

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

    def _pick_random_destination(self, world) -> tuple:
        cols, rows = world.get_map_dimensions()
        return random.randint(0, cols - 1), random.randint(0, rows - 1)

    def _compute_path_to(self, destination: tuple, world) -> list:
        cols, rows = world.get_map_dimensions()
        return bfs_path(
            start=(self.col, self.row),
            goal=destination,
            is_walkable=world.is_static_walkable,
            cols=cols,
            rows=rows,
        )