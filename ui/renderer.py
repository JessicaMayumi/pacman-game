import pygame
import time
from typing import Tuple, List
from game.grid import Grid

class Renderer:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.cell_size = 25
        self.window_size = self.grid.size * self.cell_size
        self.screen = pygame.display.set_mode((self.window_size, self.window_size + 50))
        pygame.display.set_caption("Pac-Man AI")
        
        self.COR_FUNDO = (204, 238, 255)
        self.COR_PAREDE = (0, 50, 100)
        self.COR_FRUTA = (1, 146, 0)
        self.COR_PACMAN = (255, 255, 0)
        self.COR_FANTASMA = (255, 0, 0)
        self.COR_LINHA = (255, 255, 255)
        self.COR_TEXTO = (255, 255, 255)
        
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)
        
    def renderizar(self, pacman_pos: Tuple[int, int], ghost_pos: Tuple[int, int]):
        self.screen.fill(self.COR_FUNDO)
        
        self._desenhar_grid()
        self._desenhar_pacman(pacman_pos)
        self._desenhar_fantasma(ghost_pos)
        self._desenhar_info()
        
        pygame.display.flip()
        
    def _desenhar_grid(self):
        for i in range(self.grid.size):
            for j in range(self.grid.size):
                x = j * self.cell_size
                y = i * self.cell_size
                
                if self.grid.grid[i][j] == 2:
                    pygame.draw.rect(self.screen, self.COR_PAREDE, 
                                  (x, y, self.cell_size, self.cell_size))
                elif self.grid.grid[i][j] == 1:
                    pygame.draw.rect(self.screen, self.COR_FUNDO, 
                                  (x, y, self.cell_size, self.cell_size))
                    center_x = x + self.cell_size // 2
                    center_y = y + self.cell_size // 2
                    pygame.draw.circle(self.screen, self.COR_FRUTA, 
                                     (center_x, center_y), 5)
                
                pygame.draw.rect(self.screen, self.COR_LINHA, 
                              (x, y, self.cell_size, self.cell_size), 1)
                
    def _desenhar_pacman(self, pos: Tuple[int, int]):
        x = pos[1] * self.cell_size + self.cell_size // 2
        y = pos[0] * self.cell_size + self.cell_size // 2
        pygame.draw.circle(self.screen, self.COR_PACMAN, (x, y), 8)
        
    def _desenhar_fantasma(self, pos: Tuple[int, int]):
        x = pos[1] * self.cell_size + self.cell_size // 2
        y = pos[0] * self.cell_size + self.cell_size // 2
        pygame.draw.circle(self.screen, self.COR_FANTASMA, (x, y), 8)
        
    def _desenhar_info(self):
        info_y = self.window_size + 10
        
        frutas_texto = f"Frutas: {self.grid.frutas_coletadas}/{self.grid.total_frutas}"
        text_surface = self.font.render(frutas_texto, True, self.COR_TEXTO)
        self.screen.blit(text_surface, (10, info_y))
        
        turno_texto = "Turno: Pac-Man" if self.grid.turno_pacman else "Turno: Fantasma"
        text_surface = self.font.render(turno_texto, True, self.COR_TEXTO)
        self.screen.blit(text_surface, (200, info_y))
        
    def mostrar_mensagem(self, mensagem: str):
        self.screen.fill(self.COR_FUNDO)
        
        text_surface = self.font.render(mensagem, True, self.COR_TEXTO)
        text_rect = text_surface.get_rect(center=(self.window_size//2, self.window_size//2))
        self.screen.blit(text_surface, text_rect)
        
        pygame.display.flip()
        
    def animar_movimento(self, pos_antiga: Tuple[int, int], pos_nova: Tuple[int, int], 
                        cor: Tuple[int, int, int], duracao: float = 0.2):
        frames = 10
        delay = duracao / frames
        
        for frame in range(frames + 1):
            progresso = frame / frames
            
            x_antiga = pos_antiga[1] * self.cell_size + self.cell_size // 2
            y_antiga = pos_antiga[0] * self.cell_size + self.cell_size // 2
            x_nova = pos_nova[1] * self.cell_size + self.cell_size // 2
            y_nova = pos_nova[0] * self.cell_size + self.cell_size // 2
            
            x_atual = x_antiga + (x_nova - x_antiga) * progresso
            y_atual = y_antiga + (y_nova - y_antiga) * progresso
            
            self.screen.fill(self.COR_FUNDO)
            self._desenhar_grid()
            
            pygame.draw.circle(self.screen, cor, (int(x_atual), int(y_atual)), 10)
            
            pygame.display.flip()
            time.sleep(delay)
            
    def fechar(self):
        pygame.quit()
