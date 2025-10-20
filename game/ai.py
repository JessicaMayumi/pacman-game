from typing import Tuple
from .grid import Grid
import heapq

class MinimaxAI:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.max_depth = 3
        
    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def a_star_distance(self, inicio: Tuple[int, int], objetivo: Tuple[int, int]):
        if inicio == objetivo:
            return 0
        
        fila = [(0, inicio)]
        visitados = set()
        
        while fila:
            custo, pos_atual = heapq.heappop(fila)
            
            if pos_atual in visitados:
                continue
                
            visitados.add(pos_atual)
            
            if pos_atual == objetivo:
                return custo
            
            movimentos_validos = self.grid.get_valid_moves(pos_atual)
            
            for proxima_pos in movimentos_validos:
                if proxima_pos not in visitados:
                    novo_custo = custo + 1 + self.manhattan_distance(proxima_pos, objetivo)
                    heapq.heappush(fila, (novo_custo, proxima_pos))
        
        return self.manhattan_distance(inicio, objetivo)
    
    def evaluate_position(self, pacman_pos: Tuple[int, int], ghost_pos: Tuple[int, int]):
        distance = self.a_star_distance(ghost_pos, pacman_pos)
        return -distance
    
    def minimax(self, pacman_pos: Tuple[int, int], ghost_pos: Tuple[int, int], depth: int, is_maximizing: bool, alpha: int = -float('inf'), beta: int = float('inf')):
        if depth == 0 or self.a_star_distance(ghost_pos, pacman_pos) == 0:
            return self.evaluate_position(pacman_pos, ghost_pos)
        
        if is_maximizing:
            max_eval = -float('inf')
            movimentos_validos = self.grid.get_valid_moves(ghost_pos)
            
            for movimento in movimentos_validos:
                eval_score = self.minimax(pacman_pos, movimento, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                if beta <= alpha:
                    break
            
            return max_eval
        else:
            min_eval = float('inf')
            movimentos_validos = self.grid.get_valid_moves(pacman_pos)
            
            for movimento in movimentos_validos:
                eval_score = self.minimax(movimento, ghost_pos, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                if beta <= alpha:
                    break
            
            return min_eval
    
    def calcular_melhor_movimento(self, pacman_pos: Tuple[int, int], ghost_pos: Tuple[int, int]):
        movimentos_validos = self.grid.get_valid_moves(ghost_pos)
        
        if not movimentos_validos:
            return ghost_pos
        
        melhor_movimento = movimentos_validos[0]
        melhor_score = -float('inf')
        
        for movimento in movimentos_validos:
            score = self.minimax(pacman_pos, movimento, self.max_depth - 1, False)
            if score > melhor_score:
                melhor_score = score
                melhor_movimento = movimento
        
        return melhor_movimento
