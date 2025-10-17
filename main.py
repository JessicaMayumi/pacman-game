import pygame
import sys
from game.grid import Grid
from game.entities import PacMan, Ghost
from game.ai import MinimaxAI
from ui.renderer import Renderer

def main():
    pygame.init()
    
    grid = Grid()
    pacman = PacMan(grid)
    ghost = Ghost(grid)
    ai = MinimaxAI(grid)
    renderer = Renderer(grid)
    
    clock = pygame.time.Clock()
    movimento_pendente = None
    
    print("Controles:")
    print("Setas ou WASD para mover o Pac-Man")
    print("ESC para sair")
    print("Objetivo: Colete todas as frutas antes do fantasma te pegar!")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif grid.turno_pacman:
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        movimento_pendente = (-1, 0)
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        movimento_pendente = (1, 0)
                    elif event.key in [pygame.K_LEFT, pygame.K_a]:
                        movimento_pendente = (0, -1)
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        movimento_pendente = (0, 1)
        
        if movimento_pendente and grid.turno_pacman:
            nova_pos = (pacman.posicao[0] + movimento_pendente[0], 
                       pacman.posicao[1] + movimento_pendente[1])
            
            if pacman.mover(nova_pos):
                grid.alternar_turno()
                movimento_pendente = None
                
                game_over, resultado = grid.is_game_over(pacman.posicao, ghost.posicao)
                if game_over:
                    if resultado == "vitória":
                        renderer.mostrar_mensagem("VITÓRIA! Você coletou todas as frutas!")
                    else:
                        renderer.mostrar_mensagem("DERROTA! O fantasma te pegou!")
                    
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                                waiting = False
                                running = False
                    break
        
        if not grid.turno_pacman:
            pos_antiga = ghost.posicao
            melhor_movimento = ai.calcular_melhor_movimento(pacman.posicao, ghost.posicao)
            
            if ghost.mover(melhor_movimento):
                renderer.animar_movimento(pos_antiga, ghost.posicao, renderer.COR_FANTASMA)
                grid.alternar_turno()
                
                game_over, resultado = grid.is_game_over(pacman.posicao, ghost.posicao)
                if game_over:
                    if resultado == "vitória":
                        renderer.mostrar_mensagem("VITÓRIA! Você coletou todas as frutas!")
                    else:
                        renderer.mostrar_mensagem("DERROTA! O fantasma te pegou!")
                    
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                                waiting = False
                                running = False
                    break
        
        renderer.renderizar(pacman.posicao, ghost.posicao)
        
        clock.tick(60)
    
    renderer.fechar()
    sys.exit()

if __name__ == "__main__":
    main()
