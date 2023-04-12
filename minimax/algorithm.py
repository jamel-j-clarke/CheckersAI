from copy import deepcopy
import pygame
import random

RED = (255,0,0)
WHITE = (255, 255, 255)
#alpha = float('-inf')
#beta = float('inf')

def random_move(position, game):
    moves = get_all_moves(position, WHITE, game)
    return random.choice(moves)

def minimax(position, depth, max_player, game, heuristic='combined'):
    if depth == 0 or position.winner() != None:
        return position.evaluate(heuristic), position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth-1, False, game, heuristic)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth-1, True, game, heuristic)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move            

def abNegamax(position, depth, game, alpha, beta, heuristic='average'):
    if depth == 0 or position.winner() != None:
        return position.evaluate(heuristic), position
    
    best_move = None
    best_score = float('-inf')
    
    for move in get_all_moves(position, WHITE, game):
        evaluation = abNegamax(move, depth-1, game, -beta, -max(alpha, best_score), heuristic)[0]
        currentScore = -evaluation
        
        if currentScore > best_score:
            best_score = currentScore
            best_move = move
            
            if best_score >= beta:
                break
    
    return best_score, best_move

def avgmax(position, depth, max_player, game, heuristic='average'):
    if depth == 0 or position.winner() is not None:
        return position.evaluate(heuristic), position, []
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation, _, _ = avgmax(move, depth - 1, False, game, heuristic)
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        
        return maxEval, best_move, []
    
    else:
        minEval = float('inf')
        best_move = None
        minEvalList = []
        for move in get_all_moves(position, RED, game):
            evaluation, _, _ = avgmax(move, depth - 1, True, game, heuristic)
            minEval = min(minEval, evaluation)
            minEvalList.append(evaluation)
        
        averageEval = sum(minEvalList) / len(minEvalList)
        best_move = None
        minDiff = float('inf')
        for move, evaluation in zip(get_all_moves(position, RED, game), minEvalList):
            diff = abs(evaluation - averageEval)
            if diff < minDiff:
                minDiff = diff
                best_move = move
            elif diff == minDiff:
                best_move = random.choice([move, best_move])
                
        return averageEval, best_move, minEvalList



def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            #draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    
    return moves


def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    #pygame.time.delay(100)

