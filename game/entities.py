import random
from typing import Tuple, List
from .grid import Grid

class PacMan:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.posicao = self._spawn_aleatorio()
        self.frutas_coletadas = 0
        
    def _spawn_aleatorio(self) -> Tuple[int, int]:
        cantos = self.grid.get_corner_positions()
        return random.choice(cantos)
    
    def mover(self, nova_posicao: Tuple[int, int]) -> bool:
        if nova_posicao in self.grid.get_valid_moves(self.posicao):
            self.posicao = nova_posicao
            if self.grid.collect_fruit(nova_posicao):
                self.frutas_coletadas += 1
            return True
        return False
    
    def get_posicao(self) -> Tuple[int, int]:
        return self.posicao

class Ghost:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.posicao = grid.get_center_position()
        
    def mover(self, nova_posicao: Tuple[int, int]) -> bool:
        if nova_posicao in self.grid.get_valid_moves(self.posicao):
            self.posicao = nova_posicao
            return True
        return False
    
    def get_posicao(self) -> Tuple[int, int]:
        return self.posicao
