# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.algorithm import minimax, abNegamax, avgmax, random_move

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

# Heuristic choice
# 'standard' = original heuristic
# 'bad' = bad gameplay heuristic
# 'equalize' = equalize number of pieces
# 'combined' = combination of the three
HEURISTIC = 'standard'

# AI choice
# - standard
# - custom
# - avgmax
# - random
AI_TYPE = 'standard'

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)
        
        if game.turn == WHITE:
            if AI_TYPE == 'standard':
                value, new_board = minimax(game.get_board(), 4, WHITE, game, 'standard')
            elif AI_TYPE == 'custom':
                value, new_board = minimax(game.get_board(), 4, WHITE, game, 'combined')
            elif AI_TYPE == 'avgmax':
                value, new_board, _ = avgmax(game.get_board(), 4, WHITE, game, HEURISTIC)
            elif AI_TYPE == 'random':
                new_board = random_move(game.get_board(), game)

            game.ai_move(new_board)

        try:
            winner = game.winner()
            if winner != None:
                if winner == WHITE:
                    print("Congrats White!")
                if winner == RED:
                    print("Congrats Red!")
                    
                run = False
                pygame.quit()
        except AttributeError:
            print("Congrats! " + winner)
            continue
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()
    
    pygame.quit()

main()