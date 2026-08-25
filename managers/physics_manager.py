class PhysicsManager:
    def __init__(self, map_manager, npc_manager):
        self.map_manager = map_manager
        self.npc_manager = npc_manager

    def can_move_to(self, col: int, row: int, mover=None) -> bool:
        if not self.map_manager.is_walkable(col, row):
            return False
        if self.npc_manager.is_tile_occupied(col, row, excluding=mover):
            return False

        return True