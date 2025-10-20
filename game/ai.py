from typing import Tuple, List, Set
from .grid import Grid
import heapq

class MinimaxAI:
    def __init__(self, grid: Grid):
        self.grid = grid
        
    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def encontrar_caminho(self, inicio: Tuple[int, int], objetivo: Tuple[int, int]) -> List[Tuple[int, int]]:
        if inicio == objetivo:
            return [inicio]
        
        fila = [(0, inicio, [inicio])]
        visitados = set()
        
        while fila:
            custo, pos_atual, caminho = heapq.heappop(fila)
            
            if pos_atual in visitados:
                continue
                
            visitados.add(pos_atual)
            
            if pos_atual == objetivo:
                return caminho
            
            movimentos_validos = self.grid.get_valid_moves(pos_atual)
            
            for proxima_pos in movimentos_validos:
                if proxima_pos not in visitados:
                    novo_caminho = caminho + [proxima_pos]
                    novo_custo = custo + 1 + self.manhattan_distance(proxima_pos, objetivo)
                    heapq.heappush(fila, (novo_custo, proxima_pos, novo_caminho))
        
        return [inicio]
    
    def calcular_melhor_movimento(self, pacman_pos: Tuple[int, int], ghost_pos: Tuple[int, int]) -> Tuple[int, int]:
        caminho = self.encontrar_caminho(ghost_pos, pacman_pos)
        
        if len(caminho) > 1:
            return caminho[1]
        
        movimentos_validos = self.grid.get_valid_moves(ghost_pos)
        if movimentos_validos:
            return movimentos_validos[0]
        
        return ghost_pos
