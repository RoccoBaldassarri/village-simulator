class Item:
    name = "item"
    def __init__(self, col: int, row: int):
        self.col = col
        self.row = row

    def draw(self, surface, tile_size: int):
        raise NotImplementedError("Item subclasses must implements Draw()")