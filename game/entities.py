import random
from typing import Tuple
from .grid import Grid

class PacMan:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.posicao = self._spawn_aleatorio()
        self.frutas_coletadas = 0
        
    def _spawn_aleatorio(self):
        area_laranja = self.grid.get_pacman_spawn_area()
        return random.choice(area_laranja)
    
    def mover(self, nova_posicao: Tuple[int, int]):
        if nova_posicao in self.grid.get_valid_moves(self.posicao):
            self.posicao = nova_posicao
            if self.grid.collect_fruit(nova_posicao):
                self.frutas_coletadas += 1
            return True
        return False
    
    def get_posicao(self):
        return self.posicao

class Ghost:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.posicao = self._spawn_aleatorio()
    
    def _spawn_aleatorio(self):
        area_rosa = self.grid.get_ghost_spawn_area()
        return random.choice(area_rosa)
        
    def mover(self, nova_posicao: Tuple[int, int]):
        if nova_posicao in self.grid.get_valid_moves(self.posicao):
            self.posicao = nova_posicao
            return True
        return False
    
    def get_posicao(self):
        return self.posicao
