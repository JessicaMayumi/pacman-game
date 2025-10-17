import random
from typing import List, Tuple, Optional

class Grid:
    def __init__(self):
        self.size = 28
        self.grid = self._criar_layout()
        self.turno_pacman = True
        self.frutas_coletadas = 0
        self.total_frutas = self._contar_frutas()
        
    def _criar_layout(self) -> List[List[int]]:
        grid = [
                    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,2],
                    [2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],
                    [2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],
                    [2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
                    [2,0,2,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,2,2,0,2],
                    [2,0,2,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,2,2,0,2],
                    [2,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,2],
                    [2,2,2,0,2,2,0,2,2,0,2,2,2,0,0,2,2,2,0,2,2,0,2,2,0,2,2,2],
                    [2,2,2,0,2,2,0,2,2,0,2,2,2,0,0,2,2,2,0,2,2,0,2,2,0,2,2,2],
                    [2,0,0,0,2,2,0,2,2,0,2,2,0,0,0,0,2,2,0,2,2,0,2,2,0,0,0,2],
                    [2,0,2,2,2,2,0,2,2,0,2,2,0,0,0,0,2,2,0,2,2,0,2,2,2,2,0,2],
                    [2,0,2,2,2,2,0,2,2,0,2,2,0,0,0,0,2,2,0,2,2,0,2,2,2,2,0,2],
                    [2,0,2,2,2,2,0,0,0,0,2,2,2,2,2,2,2,2,0,0,0,0,2,2,2,2,0,2],
                    [2,0,2,2,2,2,0,2,2,0,0,0,0,2,2,0,0,0,0,2,2,0,2,2,2,2,0,2],
                    [2,0,2,2,2,2,0,2,2,0,2,2,0,2,2,0,2,2,0,2,2,0,2,2,2,2,0,2],
                    [2,0,0,0,2,2,0,2,2,0,0,0,0,2,2,0,0,0,0,2,2,0,2,2,0,0,0,2],
                    [2,2,2,0,2,2,0,2,2,0,2,2,0,2,2,0,2,2,0,2,2,0,2,2,0,2,2,2],
                    [2,2,2,0,2,2,0,2,2,0,2,2,0,2,2,0,2,2,0,2,2,0,2,2,0,2,2,2],
                    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
                    [2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],
                    [2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,0,2,2,2,2,2,0,2,2,2,2,0,2],
                    [2,0,0,0,2,2,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,2,2,0,0,0,2],
                    [2,2,2,0,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,0,2,2,2],
                    [2,2,2,0,2,2,0,2,2,0,2,2,2,2,2,2,2,2,0,2,2,0,2,2,0,2,2,2],
                    [2,2,2,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,2,2,2],
                    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],

        ]
        
        for i in range(self.size):
            for j in range(self.size):
                if grid[i][j] == 0:
                    grid[i][j] = 1
                    
        return grid
    
    def _contar_frutas(self) -> int:
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 1:
                    count += 1
        return count
    
    def is_wall(self, pos: Tuple[int, int]) -> bool:
        x, y = pos
        if not self._posicao_valida(pos):
            return True
        return self.grid[x][y] == 2
    
    def _posicao_valida(self, pos: Tuple[int, int]) -> bool:
        x, y = pos
        return 0 <= x < self.size and 0 <= y < self.size
    
    def get_valid_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        x, y = pos
        moves = []
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dx, dy in directions:
            new_pos = (x + dx, y + dy)
            if not self.is_wall(new_pos):
                moves.append(new_pos)
                
        return moves
    
    def collect_fruit(self, pos: Tuple[int, int]) -> bool:
        x, y = pos
        if self.grid[x][y] == 1:
            self.grid[x][y] = 0
            self.frutas_coletadas += 1
            return True
        return False
    
    def is_game_over(self, pacman_pos: Tuple[int, int], ghost_pos: Tuple[int, int]) -> Tuple[bool, str]:
        if self.frutas_coletadas >= self.total_frutas:
            return True, "vitória"
            
        if pacman_pos == ghost_pos:
            return True, "derrota"
            
        return False, ""
    
    def get_corner_positions(self) -> List[Tuple[int, int]]:
        return [(2, 2), (2, 9), (9, 2), (9, 9)]
    
    def get_center_position(self) -> Tuple[int, int]:
        return (5, 5)
    
    def alternar_turno(self):
        self.turno_pacman = not self.turno_pacman
    
    def get_grid_state(self) -> List[List[int]]:
        return [row[:] for row in self.grid]
