from Board import BoardUtility
import random
import copy
import numpy as np

ROWS = 6
COLS = 6


class Player:
    def __init__(self, player_piece):
        self.piece = player_piece

    def play(self, board):
        return 0


class RandomPlayer(Player):
    def play(self, board):
        return [random.choice(BoardUtility.get_valid_locations(board)), random.choice([1, 2, 3, 4]), random.choice(["skip", "clockwise", "anticlockwise"])]


class HumanPlayer(Player):
    def play(self, board):
        move = input("row, col, region, rotation\n")
        move = move.split()
        print(move)
        return [[int(move[0]), int(move[1])], int(move[2]), move[3]]


class MiniMaxPlayer(Player):
    def __init__(self, player_piece, depth=5):
        super().__init__(player_piece)
        self.depth = depth

    def play(self, board):
        row = -1
        col = -1
        region = -1
        rotation = -1
        # Todo: implement minimax algorithm
        
        bestMove = self.max_value(board, self.depth, 1, -10000, 10000)[1]

        return [bestMove.loc, bestMove.reg, bestMove.rot]
        
    
    def min_value(self, board, depth, turn, alpha, beta):
        if BoardUtility.is_terminal_state(board):
            return self.terminal_state(board), 0
        piece = self.piece
        opponent = 0
        if piece == 1:
            opponent = 2
        else:
            opponent = 1
        if depth <= turn:
            return self.get_eval(board, opponent), 0
        
        rotation =["skip", "clockwise", "anticlockwise"]
        validLocs = BoardUtility.get_valid_locations(board)
        bestMove = Move([-1,-1], -1, -1)
        v = 10000
        
        for loc in validLocs:
            for rot in rotation:
                for reg in range(4):
                    copy_board = copy.deepcopy(board)
                    move = Move(loc, reg, rot)
                    BoardUtility.make_move(copy_board, loc[0], loc[1], reg, rot, opponent)
                    v_copy = v
                    v = min(v, self.max_value(copy_board, depth, turn + 1, alpha, beta)[0])
                    if v_copy != v:
                        bestMove = move
#                         print(copy_board, "min")
                    if v <= alpha:
                        return v, bestMove
                    beta = min(beta, v)
        return v, bestMove
    
    
    def max_value(self, board, depth, turn, alpha, beta):
        if BoardUtility.is_terminal_state(board):
            return self.terminal_state(board), 0
        
        piece = self.piece
        opponent = 0
        if piece == 1:
            opponent = 2
        else:
            opponent = 1
        if depth <= turn:
            return self.get_eval(board, opponent), 0
        
        rotation =["skip", "clockwise", "anticlockwise"]
        validLocs = BoardUtility.get_valid_locations(board)
        values = {}
        bestMove = Move([-1,-1], -1, -1)
        v = -10000
        
        for loc in validLocs:
            for rot in rotation:
                for reg in range(4):
                    copy_board = copy.deepcopy(board)
                    move = Move(loc, reg, rot)
                    BoardUtility.make_move(copy_board, loc[0], loc[1], reg, rot, piece)
                    v_copy = v
                    v = max(v, self.min_value(copy_board, depth, turn + 1, alpha, beta)[0])
                    if v_copy != v:
                        bestMove = move
#                         print(copy_board, "max")
                    if beta <= v:
                        return v, bestMove
                    alpha = max(alpha, v)
        return v, bestMove
                
                
                
    def terminal_state(self, board):
        if BoardUtility.has_player_won(board, self.piece): 
            return 15
        if BoardUtility.is_draw(board): 
            return 0
        return -15
    
    
    def get_eval(self, board, opponent):
        val = self.check4(board, self.piece) * 0.9 - self.check4(board, opponent) * 0.6 + self.check3(board, self.piece) * 0.5 - self.check3(board, opponent) * 0.3
        return val
    
    def check4(self, game_board, player_piece):
        num = 0
        for c in range(3):
            for r in range(ROWS):
                if game_board[r][c] == player_piece and game_board[r][c + 1] == player_piece and game_board[r][
                        c + 2] == player_piece and game_board[r][c + 3] == player_piece:
                    num+=1

        # checking vertically
        for r in range(3):
            for c in range(COLS):
                if game_board[r][c] == player_piece and game_board[r + 1][c] == player_piece and game_board[r + 2][
                        c] == player_piece and game_board[r + 3][c] == player_piece:
                    num+=1

        # checking diagonally
        for c in range(COLS - 3):
            for r in range(3, ROWS):
                if game_board[r][c] == player_piece and game_board[r - 1][c + 1] == player_piece and game_board[r - 2][
                    c + 2] == player_piece and \
                        game_board[r - 3][c + 3] == player_piece:
                    num+=1

        # checking diagonally
        for c in range(3, COLS):
            for r in range(3, ROWS):
                if game_board[r][c] == player_piece and game_board[r - 1][c - 1] == player_piece and game_board[r - 2][
                    c - 2] == player_piece and \
                        game_board[r - 3][c - 3] == player_piece:
                    num+=1

        return num
    
    
    def check3(self, game_board, player_piece):
        num = 0
        for c in range(4):
            for r in range(ROWS):
                if game_board[r][c] == player_piece and game_board[r][c + 1] == player_piece and game_board[r][
                        c + 2] == player_piece:
                    num+=1

        # checking vertically
        for r in range(4):
            for c in range(COLS):
                if game_board[r][c] == player_piece and game_board[r + 1][c] == player_piece and game_board[r + 2][
                        c] == player_piece:
                    num+=1

        # checking diagonally
        for c in range(COLS - 2):
            for r in range(2, ROWS):
                if game_board[r][c] == player_piece and game_board[r - 1][c + 1] == player_piece and game_board[r - 2][
                    c + 2] == player_piece:
                    num+=1

        # checking diagonally
        for c in range(2, COLS):
            for r in range(2, ROWS):
                if game_board[r][c] == player_piece and game_board[r - 1][c - 1] == player_piece and game_board[r - 2][
                    c - 2] == player_piece:
                    num+=1

        return num
    


class MiniMaxProbPlayer(Player):
    def __init__(self, player_piece, depth=5, prob_stochastic=0.9):
        super().__init__(player_piece)
        self.depth = depth
        self.prob_stochastic = 1 - prob_stochastic

    def play(self, board):
        row = -1
        col = -1
        region = -1
        rotation = -1
        # Todo: implement minimax algorithm
        bestMove = None
        p = np.random.binomial(1, self.prob_stochastic, 1)
        if p == 0:
            bestMove = self.random_state(board)
        else:
            bestMove = self.max_value(board, self.depth, 1, -10000, 10000)[1]
        return [bestMove.loc, bestMove.reg, bestMove.rot]
    
    
    def random_state(self, board):
        rotation =["skip", "clockwise", "anticlockwise"]
        validLocs = BoardUtility.get_valid_locations(board)
        move = Move(random.choice(validLocs), random.choice([1, 2, 3, 4]), random.choice(rotation))
#         print(self.prob_stochastic)
        return move
                    
    def max_value(self, board, depth, turn, alpha, beta):
        if BoardUtility.is_terminal_state(board):
            return self.terminal_state(board), 0
        
        piece = self.piece
        opponent = 0
        if piece == 1:
            opponent = 2
        else:
            opponent = 1
        if depth <= turn:
            return self.get_eval(board, opponent), 0
        
        rotation =["skip", "clockwise", "anticlockwise"]
        validLocs = BoardUtility.get_valid_locations(board)
        values = {}
        bestMove = Move([-1,-1], -1, -1)
        v = -10000
        summ = 0
        n = 0           
                    
        for loc in validLocs:
            for rot in rotation:
                for reg in range(4):
                    copy_board = copy.deepcopy(board)
                    move = Move(loc, reg, rot)
                    BoardUtility.make_move(copy_board, loc[0], loc[1], reg, rot, piece)
                    v_copy = v
                    value = self.min_value(copy_board, depth, turn + 1, alpha, beta)[0]
                    v = max(v, value)
                    summ+=value
                    n+=1
                    if v_copy != v:
                        bestMove = move
#                         print(copy_board, "max")
#                     if beta <= v:
#                         return v * self.prob_stochastic + summ / n * (1 - self.prob_stochastic), bestMove
                    alpha = max(alpha, v)
        return v * self.prob_stochastic + summ / n * (1 - self.prob_stochastic), bestMove
                    
                    
    def min_value(self, board, depth, turn, alpha, beta):
        if BoardUtility.is_terminal_state(board):
            return self.terminal_state(board), 0
        piece = self.piece
        opponent = 0
        if piece == 1:
            opponent = 2
        else:
            opponent = 1
        if depth <= turn:
            return self.get_eval(board, opponent), 0
        
        rotation =["skip", "clockwise", "anticlockwise"]
        validLocs = BoardUtility.get_valid_locations(board)
        bestMove = Move([-1,-1], -1, -1)
        v = 10000
        
        for loc in validLocs:
            for rot in rotation:
                for reg in range(4):
                    copy_board = copy.deepcopy(board)
                    move = Move(loc, reg, rot)
                    BoardUtility.make_move(copy_board, loc[0], loc[1], reg, rot, opponent)
                    v_copy = v
                    v = min(v, self.max_value(copy_board, depth, turn + 1, alpha, beta)[0])
                    if v_copy != v:
                        bestMove = move
#                         print(copy_board, "min")
#                     if v <= alpha:
#                         return v, bestMove
                    beta = min(beta, v)
        return v, bestMove
                
                
                
    def terminal_state(self, board):
        if BoardUtility.has_player_won(board, self.piece): 
            return 15
        if BoardUtility.is_draw(board): 
            return 0
        return -15
    
    
    def get_eval(self, board, opponent):
        val = self.check4(board, self.piece) * 0.9 - self.check4(board, opponent) * 0.6 + self.check3(board, self.piece) * 0.5 - self.check3(board, opponent) * 0.3
        return val
    
    def check4(self, game_board, player_piece):
        num = 0
        for c in range(3):
            for r in range(ROWS):
                if game_board[r][c] == player_piece and game_board[r][c + 1] == player_piece and game_board[r][
                        c + 2] == player_piece and game_board[r][c + 3] == player_piece:
                    num+=1

        # checking vertically
        for r in range(3):
            for c in range(COLS):
                if game_board[r][c] == player_piece and game_board[r + 1][c] == player_piece and game_board[r + 2][
                        c] == player_piece and game_board[r + 3][c] == player_piece:
                    num+=1

        # checking diagonally
        for c in range(COLS - 3):
            for r in range(3, ROWS):
                if game_board[r][c] == player_piece and game_board[r - 1][c + 1] == player_piece and game_board[r - 2][
                    c + 2] == player_piece and \
                        game_board[r - 3][c + 3] == player_piece:
                    num+=1

        # checking diagonally
        for c in range(3, COLS):
            for r in range(3, ROWS):
                if game_board[r][c] == player_piece and game_board[r - 1][c - 1] == player_piece and game_board[r - 2][
                    c - 2] == player_piece and \
                        game_board[r - 3][c - 3] == player_piece:
                    num+=1

        return num
    
    
    def check3(self, game_board, player_piece):
        num = 0
        for c in range(4):
            for r in range(ROWS):
                if game_board[r][c] == player_piece and game_board[r][c + 1] == player_piece and game_board[r][
                        c + 2] == player_piece:
                    num+=1

        # checking vertically
        for r in range(4):
            for c in range(COLS):
                if game_board[r][c] == player_piece and game_board[r + 1][c] == player_piece and game_board[r + 2][
                        c] == player_piece:
                    num+=1

        # checking diagonally
        for c in range(COLS - 2):
            for r in range(2, ROWS):
                if game_board[r][c] == player_piece and game_board[r - 1][c + 1] == player_piece and game_board[r - 2][
                    c + 2] == player_piece:
                    num+=1

        # checking diagonally
        for c in range(2, COLS):
            for r in range(2, ROWS):
                if game_board[r][c] == player_piece and game_board[r - 1][c - 1] == player_piece and game_board[r - 2][
                    c - 2] == player_piece:
                    num+=1

        return num
    
    
class Move:
    def __init__(self, loc, reg, rot):
        self.loc = loc
        self.reg = reg
        self.rot = rot
