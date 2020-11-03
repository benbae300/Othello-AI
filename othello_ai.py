
import random
import sys
import time
import heapq
from othello_shared import get_possible_moves, play_move, compute_utility


############ MINIMAX ###############################

"""
Computes the minimax value of a MAX node
"""
def minimax_max_node(board):
    moves = get_possible_moves(board,1) 
    if(moves == []): return compute_utility(board)
    util = float('-inf') 
    for col, row in moves: 
        util = max(minimax_min_node(play_move(board, 1, col ,row)), util)

    return util


"""
Computes the minimax value of a MIN node
"""
def minimax_min_node(board):
    moves = get_possible_moves(board,2) 
    if(moves == []): return compute_utility(board)
    util = float('inf') 
    for col, row in moves: 
        util = min(minimax_max_node(play_move(board, 2, col ,row)), util)

    return util


"""
Given a board and a player color, decide on a move. 
The return value is a tuple of integers (i,j), where
i is the column and j is the row on the board.  
"""
# dark = 1, light = 2 
def select_move_minimax(board, color):
    moves = get_possible_moves(board, color) 
    util = float('inf')
    if color == 1: util = float('-inf') 
    col, row = 0,0
    for x,y in moves:  
        new_board = play_move(board, color, x, y)
        if(color == 1):
            new_board_util = minimax_min_node(new_board)
            if(new_board_util > util): col, row = x,y
            util = max(util, new_board_util)  
        else: 
            new_board_util = minimax_max_node(new_board)

            if(new_board_util < util): col, row = x,y
            util = min(util, new_board_util) 
    return col, row 

    
############ ALPHA-BETA PRUNING #####################

"""
Computes the minimax value of a MAX node with alpha-beta pruning
"""
def alphabeta_max_node(board, alpha, beta, level, limit):
    moves = get_possible_moves(board,1) 
    if(moves == [] or level == limit): return compute_utility(board)
    ordered = []
    for m in moves: 
        heapq.heappush(ordered,
            (-1 * compute_utility(play_move(board, 1, m[0], m[1])), m))
    util = float('-inf')
    for u, move in ordered: 
        col, row = move
        util = max(alphabeta_min_node(play_move(board, 1, col ,row), alpha, 
            beta, level+1, limit), util)
        if(util >= beta): return util 
        alpha = max(alpha, util)
    return util


"""
Computes the minimax value of a MIN node with alpha-beta pruning
"""
def alphabeta_min_node(board, alpha, beta, level, limit):
    moves = get_possible_moves(board,2) 
    if(moves == [] or level == limit): return compute_utility(board)
    ordered = []
    for m in moves: 
        heapq.heappush(ordered,
            (compute_utility(play_move(board, 2, m[0], m[1])),m))
    util = float('inf') 
    for u, move in ordered:
        col, row= move 
        util = min(alphabeta_max_node(play_move(board, 2, col ,row), alpha,
            beta,level+1, limit), util)
        if(util <= alpha): return util 
        beta = min(beta, util)
    return util


"""
Given a board and a player color, decide on a move. 
The return value is a tuple of integers (i,j), where
i is the column and j is the row on the board.  
"""
def select_move_alphabeta(board, color, limit):
    moves = get_possible_moves(board, color) 
    util = float('inf')
    if color == 1: util = float('-inf') 
    col, row = 0,0
    ordered = [] 
    if color == 1: 
        for m in moves: 
            heapq.heappush(ordered,
                (-1 * compute_utility(play_move(board, 1, m[0], m[1])), m))
    else: 
        for m in moves: 
            heapq.heappush(ordered,
                (compute_utility(play_move(board, 2, m[0], m[1])), m))
    for u,move in ordered: 
        x,y = move
        new_board = play_move(board, color, x, y)
        if(color == 1):
            new_board_util = alphabeta_min_node(new_board, util, float('inf'), 2, limit)
            if(new_board_util > util): col, row = x,y
            util = max(util, new_board_util)  
        else: 
            new_board_util = alphabeta_max_node(new_board, float('-inf') , util,2,limit)
            if(new_board_util < util): col, row = x,y
            util = min(util, new_board_util) 
    return col, row 


####################################################
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("Minimax AI") # First line is the name of this AI  
    color = int(input()) # Then we read the color: 1 for dark (goes first), 
                         # 2 for light. 

    while True: # This is the main loop 
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input() 
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over. 
            print 
        else: 
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The 
                                  # squares in each row are represented by 
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)
                    
            # Select the move and send it to the manager 
            #movei, movej = select_move_minimax(board, color)
            movei, movej = select_move_alphabeta(board, color, 8)
            print("{} {}".format(movei, movej)) 


if __name__ == "__main__":
    run_ai()