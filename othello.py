from timeit import *
import math
from random import randint

w = "o"
b = "@"
EDGE = [s for s in range(10)] + [t for t in range(90,100)] + [10*u for u in range(10)] + [10*v+9 for v in range(10)]
UP, DOWN, LEFT, RIGHT = -10,10,-1,1
NW,NE,SW,SE = -11,-9,9,11
DIRECTIONS = [UP,DOWN,LEFT,RIGHT,NW,NE,SW,SE]
BOARD_WEIGHTS = [
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
]

#PREGAME FUNCTIONS
def make_board():
    array = []
    for bo in range(100):
        if bo in EDGE: 
            array.append("x")
        elif bo == 44 or bo == 55: 
            array.append(w)
        elif bo == 45 or bo == 54:
            array.append(b)
        else:
            array.append(".")
    return array
def display(board):
    print("  1 2 3 4 5 6 7 8 ", end = "")
    i = 1
    for s in range(len(board)):
        if board[s] == 'x':
            if s == 0:
                print(" ", end = " ")
            elif s%10 == 0:
                print()
                if i != 9:
                    print(i, end = " ")
                    i+=1
            if s == 90:
                print(" ",end = " ")
        else:
            print(board[s], end = " ")
    print()
def count(board,player):
    c = 0
    for bo in range(len(board)):
        if bo in EDGE: continue
        if board[bo] == player:
            c+=1
    return c
def empties(board):
    c = []
    for bo in range(len(board)):
        if bo in EDGE: continue
        if board[bo] == '.':
            c.append(bo)
    return c


#GAME FUNCTIONS
def opponent(player):
    if player == w: return b
    else: return w
def bracket(sq,direction,board,player):
    bracket = sq + direction
    if board[bracket] == player or bracket in EDGE: return None
    while board[bracket] == opponent(player):
        bracket += direction
    if bracket in EDGE or board[bracket] == ".": return None
    else: return bracket
def valid_move(sq,board,player):
    if board[sq] != '.': return False 
    return any(bracket(sq,D,board,player) for D in DIRECTIONS)
def flip(sq,bracket,direction,board,player): #flip all squares between sq and bracket
    current = sq + direction
    while current != bracket:
        board[current] = player
        current += direction
def moves(board,player): #all possible moves
    m = []
    for bo in range(len(board)):
        if bo in EDGE: continue
        if valid_move(bo,board,player):
            m.append(bo)
    return m
def play(sq,board,player):
    if not sq: return
    if not valid_move(sq,board,player):
        print("not a valid move")
        if player == b:
            return play(int(input("move: ")),board,player)
    board[sq] = player
    for D in DIRECTIONS:
        br = bracket(sq,D,board,player)
        if br:
            flip(sq,br,D,board,player)
    return board
def winner(board):
    if count(board,w) > count(board,b): return w
    elif count(board,b) > count(board,w): return b
    else: return 0
#STRATEGIES
def score(board,player):
    total = 0
    for bo in range(len(board)):
        if bo in EDGE: continue
        if board[bo] == player: total += BOARD_WEIGHTS[bo]
        elif board[bo] == opponent(player): total -= BOARD_WEIGHTS[bo]
    return total
def alphabeta(board,depth,alpha,beta,player,maximizing_player):
    if depth == 0 or not moves(board,player):
        return score(board,player)
    if maximizing_player:
        v = -math.inf
        #print(player, moves(board,player))
        for bo in moves(board,player):
            temp_board = play(bo,board.copy(),player)
            #display(temp_board)
            v = max(v,alphabeta(temp_board,depth-1,alpha,beta,opponent(player),False))
            alpha = max(alpha,v)
            if beta<=alpha:
                break
        return v
    else:
        v = math.inf
        #print(player, moves(board,player))
        for bo in moves(board,player):
            temp_board = play(bo,board.copy(),player)
            #display(temp_board)
            v = min(v,alphabeta(temp_board,depth-1,alpha,beta,opponent(player),True))
            beta = min(beta,v)
            if beta<=alpha:
                break
        return v
def best_move(board,player):
    if len(empties(board))==1: return empties(board)[0]
    depth = 4 #will search __ moves in advance
    mov = moves(board,player)
    if not mov: return None
    print("computer can move: ",mov)
    max_points = 0
    max_index = mov[0]
    for m in mov:
        temp_board = play(m,board.copy(),player)
        points = alphabeta(temp_board,depth,-math.inf,math.inf,player,True)
        if points > max_points:
            max_points = points
            max_index = m 
    return max_index
def random_move(board,player):
    m = moves(board,player)
    if not m: return None
    r = randint(0, len(m)-1)
    return m[r]
def game_over():
    return all(board[bo] != '.' for bo in range(len(board)))

board = make_board()
print()
print("to play, type a two digit number, the first digit is the row & second is column")
print()
print("BEGIN")
print()
display(board)
print()
while not game_over():
    print("user can move: ",moves(board,b))
    move = int(input("user's move: "))
    #print(rand)
    play(move,board,b)
    display(board)
    print()

    #print(moves(board,w))
    best = best_move(board,w)
    #print(best)
    play(best,board,w)
    print("computer's move: ", best)
    display(board)
    print()


print("END")
display(board)
print("winner: ",winner(board))