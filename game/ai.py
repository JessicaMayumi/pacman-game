from typing import Tuple, List
from .grid import Grid

class MinimaxAI:
    def __init__(self, grid: Grid):
        self.grid = grid
        
    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def calcular_melhor_movimento(self, pacman_pos: Tuple[int, int], ghost_pos: Tuple[int, int]) -> Tuple[int, int]:
        movimentos_validos = self.grid.get_valid_moves(ghost_pos)
        
        if not movimentos_validos:
            return ghost_pos
            
        melhor_movimento = movimentos_validos[0]
        menor_distancia = self.manhattan_distance(pacman_pos, melhor_movimento)
        
        for movimento in movimentos_validos:
            distancia = self.manhattan_distance(pacman_pos, movimento)
            if distancia < menor_distancia:
                menor_distancia = distancia
                melhor_movimento = movimento
                
        return melhor_movimento
