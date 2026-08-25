class PhysicsManager:
    """
    Il Validatore / Motore di Collisione.

    Non possiede dati propri: si limita a interrogare MapManager (regole
    statiche del terreno) e NPCManager (occupazione dinamica) e a comporre
    le due risposte in un unico verdetto tramite can_move_to().

    Comunicazione:
      - Riceve riferimenti a MapManager e NPCManager al momento della creazione
        (dependency injection), non li istanzia da solo.
      - È l'UNICO punto del codice autorizzato a rispondere alla domanda
        "posso muovermi qui?". NPC (e in futuro il player) non devono MAI
        controllare direttamente grid o liste di NPC: passano sempre da qui,
        di norma tramite la facade WorldManager.
    """

    def __init__(self, map_manager, npc_manager):
        self.map_manager = map_manager
        self.npc_manager = npc_manager

    def can_move_to(self, col: int, row: int, mover=None) -> bool:
        """
        `mover` è l'entità che sta chiedendo di muoversi (tipicamente un NPC):
        serve a NPCManager per escludere l'entità stessa dal controllo di
        occupazione quando verifica la propria tile di partenza.
        """
        # 1) Controllo statico: il terreno è calpestabile?
        if not self.map_manager.is_walkable(col, row):
            return False

        # 2) Controllo dinamico: la tile è libera da altri NPC?
        if self.npc_manager.is_tile_occupied(col, row, excluding=mover):
            return False

        return True
