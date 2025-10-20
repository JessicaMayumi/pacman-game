import pygame
import time
from typing import Tuple, List
from game.grid import Grid

class Renderer:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.cell_size = 35
        self.window_size = self.grid.size * self.cell_size
        self.info_width = 300
        self.screen = pygame.display.set_mode((self.window_size + self.info_width, self.window_size))
        pygame.display.set_caption("Pac-Man AI")
        
        self.COR_FUNDO = (204, 238, 255)
        self.COR_PAREDE = (0, 50, 100)
        self.COR_FRUTA = (1, 146, 0)
        self.COR_PACMAN = (255, 255, 0)
        self.COR_FANTASMA = (255, 0, 0)
        self.COR_LINHA = (255, 255, 255)
        self.COR_TEXTO = (255, 255, 255)
        self.COR_AREA_PACMAN = (255, 165, 0, 100)
        self.COR_AREA_FANTASMA = (255, 20, 147, 100)
        
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)
        
    def renderizar(self, pacman_pos: Tuple[int, int], ghost_pos: Tuple[int, int]):
        game_area = pygame.Rect(0, 0, self.window_size, self.window_size)
        self.screen.fill(self.COR_FUNDO, game_area)
        
        self._desenhar_grid()
        self._desenhar_areas_spawn()
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
                    pygame.draw.circle(self.screen, self.COR_FRUTA, (center_x, center_y), 6)
                
    def _desenhar_areas_spawn(self):
        area_pacman = self.grid.get_pacman_spawn_area()
        for i, j in area_pacman:
            x = j * self.cell_size
            y = i * self.cell_size
            overlay = pygame.Surface((self.cell_size, self.cell_size))
            overlay.set_alpha(100)
            overlay.fill((255, 165, 0))  # Laranja
            self.screen.blit(overlay, (x, y))
        
        area_fantasma = self.grid.get_ghost_spawn_area()
        for i, j in area_fantasma:
            x = j * self.cell_size
            y = i * self.cell_size
            overlay = pygame.Surface((self.cell_size, self.cell_size))
            overlay.set_alpha(100)
            overlay.fill((255, 20, 147))  # Rosa
            self.screen.blit(overlay, (x, y))
                
    def _desenhar_pacman(self, pos: Tuple[int, int]):
        x = pos[1] * self.cell_size + self.cell_size // 2
        y = pos[0] * self.cell_size + self.cell_size // 2
        pygame.draw.circle(self.screen, self.COR_PACMAN, (x, y), 10)
        
    def _desenhar_fantasma(self, pos: Tuple[int, int]):
        x = pos[1] * self.cell_size + self.cell_size // 2
        y = pos[0] * self.cell_size + self.cell_size // 2
        pygame.draw.circle(self.screen, self.COR_FANTASMA, (x, y), 10)
        
    def _desenhar_info(self):
        info_rect = pygame.Rect(self.window_size, 0, self.info_width, self.window_size)
        pygame.draw.rect(self.screen, (25, 25, 25), info_rect)
        pygame.draw.rect(self.screen, (80, 80, 80), info_rect, 2)
        
        info_y = 20
        
        titulo_font = pygame.font.Font(None, 32)
        titulo = titulo_font.render("PAC-MAN AI", True, (255, 255, 0))
        titulo_rect = titulo.get_rect(center=(self.window_size + self.info_width//2, info_y))
        self.screen.blit(titulo, titulo_rect)
        
        linha_y = info_y + 40
        pygame.draw.line(self.screen, (60, 60, 60), (self.window_size + 20, linha_y), (self.window_size + self.info_width - 20, linha_y), 2)
        
        stats_y = linha_y + 20
        
        frutas_texto = f"FRUTAS: {self.grid.frutas_coletadas}/{self.grid.total_frutas}"
        frutas_font = pygame.font.Font(None, 22)
        text_surface = frutas_font.render(frutas_texto, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.window_size + 20, stats_y))
        
        turno_texto = f"TURNO: {'PAC-MAN' if self.grid.turno_pacman else 'FANTASMA'}"
        turno_color = (255, 255, 0) if self.grid.turno_pacman else (255, 100, 100)
        text_surface = frutas_font.render(turno_texto, True, turno_color)
        self.screen.blit(text_surface, (self.window_size + 20, stats_y + 30))
        
        pacman_pontos = f"PAC-MAN: {self.grid.frutas_coletadas * 10} PONTOS"
        text_surface = frutas_font.render(pacman_pontos, True, (255, 255, 0))
        self.screen.blit(text_surface, (self.window_size + 20, stats_y + 60))
        
        fantasma_frutas = f"FANTASMA: {self.grid.total_frutas - self.grid.frutas_coletadas} RESTANTES"
        text_surface = frutas_font.render(fantasma_frutas, True, (255, 100, 100))
        self.screen.blit(text_surface, (self.window_size + 20, stats_y + 90))
        
        instrucoes_y = stats_y + 130
        instrucoes = "CONTROLES:"
        instrucoes_font = pygame.font.Font(None, 18)
        text_surface = instrucoes_font.render(instrucoes, True, (180, 180, 180))
        self.screen.blit(text_surface, (self.window_size + 20, instrucoes_y))
        
        controles = "SETAS ou WASD"
        text_surface = instrucoes_font.render(controles, True, (180, 180, 180))
        self.screen.blit(text_surface, (self.window_size + 20, instrucoes_y + 25))
        
        sair = "ESC para SAIR"
        text_surface = instrucoes_font.render(sair, True, (180, 180, 180))
        self.screen.blit(text_surface, (self.window_size + 20, instrucoes_y + 50))
        
    def mostrar_mensagem(self, mensagem: str):
        overlay = pygame.Surface((self.window_size, self.window_size))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        box_width = 400
        box_height = 150
        box_x = (self.window_size - box_width) // 2
        box_y = (self.window_size - box_height) // 2
        
        pygame.draw.rect(self.screen, (50, 50, 50), (box_x, box_y, box_width, box_height))
        pygame.draw.rect(self.screen, (255, 255, 0), (box_x, box_y, box_width, box_height), 3)
        
        if "VITÓRIA" in mensagem:
            titulo = "VITÓRIA!"
            cor_titulo = (0, 255, 0)
        else:
            titulo = "DERROTA!"
            cor_titulo = (255, 0, 0)
        
        titulo_font = pygame.font.Font(None, 36)
        titulo_surface = titulo_font.render(titulo, True, cor_titulo)
        titulo_rect = titulo_surface.get_rect(center=(self.window_size//2, box_y + 40))
        self.screen.blit(titulo_surface, titulo_rect)
        
        msg_font = pygame.font.Font(None, 24)
        msg_surface = msg_font.render(mensagem, True, (255, 255, 255))
        msg_rect = msg_surface.get_rect(center=(self.window_size//2, box_y + 80))
        self.screen.blit(msg_surface, msg_rect)
        
        continue_font = pygame.font.Font(None, 20)
        continue_text = "Pressione qualquer tecla para sair..."
        continue_surface = continue_font.render(continue_text, True, (200, 200, 200))
        continue_rect = continue_surface.get_rect(center=(self.window_size//2, box_y + 110))
        self.screen.blit(continue_surface, continue_rect)
        
        pygame.display.flip()
        
    def animar_movimento(self, pos_antiga: Tuple[int, int], pos_nova: Tuple[int, int], 
                        cor: Tuple[int, int, int], duracao: float = 0.1):
        frames = 5
        delay = duracao / frames
        
        for frame in range(frames + 1):
            progresso = frame / frames
            
            x_antiga = pos_antiga[1] * self.cell_size + self.cell_size // 2
            y_antiga = pos_antiga[0] * self.cell_size + self.cell_size // 2
            x_nova = pos_nova[1] * self.cell_size + self.cell_size // 2
            y_nova = pos_nova[0] * self.cell_size + self.cell_size // 2
            
            x_atual = x_antiga + (x_nova - x_antiga) * progresso
            y_atual = y_antiga + (y_nova - y_antiga) * progresso
            
            game_area = pygame.Rect(0, 0, self.window_size, self.window_size)
            self.screen.fill(self.COR_FUNDO, game_area)
            self._desenhar_grid()
            
            pygame.draw.circle(self.screen, cor, (int(x_atual), int(y_atual)), 10)
            
            pygame.display.flip()
            time.sleep(delay)
            
    def fechar(self):
        pygame.quit()
