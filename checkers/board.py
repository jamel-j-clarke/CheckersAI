import pygame

from .piece import Piece
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()
    
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self, heuristic='standard'):
        if heuristic == 'standard':
            # high piece differential (for white) is better
            h = self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)
        elif heuristic == 'bad':
            # high piece differential (for red) is better
            h = self.red_left - self.white_left + (self.red_kings * 0.5 - self.white_kings * 0.5)
        elif heuristic == 'equalize':
            # piece differential close to 0 is better
            h = 10 - abs(self.red_left - self.white_left)
        elif heuristic == 'average':
            # generate the values
            standard_value = self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)
            equalize_value = 10 - abs(self.red_left - self.white_left)
            bad_value = self.red_left - self.white_left + (self.red_kings * 0.5 - self.white_kings * 0.5)
            
            # the way heuristic values will be prioritized are as follows:
            # normal prioritization:    1) 55%  2) 35%  3) 10%
            # increased prioritization: 1) 65%  2) 30%  3) 5%
            # decreased prioritization: 1) 45%  2) 40%  3) 15%
            
            # if there are more red pieces than white pieces, prioritize standard.
            if (self.white_left < self.red_left):
                
                # if there are more red kings than white kings, increase priority
                if (self.white_kings < self.red_kings):
                    h = 0.65 * standard_value + 0.30 * equalize_value + 0.05 * bad_value
                
                # if there are more white kings than red kings, decrease priority
                elif (self.white_kings > self.red_kings):
                    h = 0.45 * standard_value + 0.35 * equalize_value + 0.15 * bad_value 
                
                # if there are an equal number of red kings and white kings, normally prioritize
                else:
                    h = 0.55 * standard_value + 0.35 * equalize_value + 0.1 * bad_value 
                
            # if there are more white pieces than red pieces, prioritize bad.
            elif (self.white_left > self.red_left):
                
                # if there are more red kings than white kings, decrease priority
                if (self.white_kings < self.red_kings):
                    h = 0.15 * standard_value + 0.4 * equalize_value + 0.45 * bad_value 
                    
                # if there are more white kings than red kings, increase priority
                elif (self.white_kings > self.red_kings):
                    h = 0.05 * standard_value + 0.3 * equalize_value + 0.65 * bad_value 
                
                # if there are an equal number of red kinds and white kings, normally prioritize bad
                else:
                    h = 0.1 * standard_value + 0.35 * equalize_value + 0.55 * bad_value 
                
            # otherwise, prioritize equalize 
            # to make the ai be a bit more naturally 'aggressive', as it is presumed that this is
            # the state the ai will more often than not be in:
            # bad priority <= standard priority <= equalize priority
            else:
                
                # if there are more red kings than white kings, increase standard's priority
                if (self.white_kings < self.red_kings):
                    h = 0.40 * standard_value + 0.55 * equalize_value + 0.05 * bad_value
                
                # if there are more white kings than red kings, increase bad's priority
                elif (self.white_kings > self.red_kings):
                    h = 0.225 * standard_value + 0.55 * equalize_value + 0.225 * bad_value
                
                # if there are an equal number of red kings and white kings, normally prioritize
                # equalize with standard and bad being evenly weighted
                else:
                    h = 0.32 * standard_value + 0.50 * equalize_value + 0.18 * bad_value
                
        return h

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1 

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1
    
    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        
        return None 
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves