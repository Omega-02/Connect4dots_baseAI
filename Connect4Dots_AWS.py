import copy
import math
import random
import os

def create_board():
    global turn
    b = [[0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0]]
    turn = 0
    return b


def display_board(x):
    os.system('cls'if os.name == 'nt' else 'clear')
    print(f"Current Turn: {turn}")
    for i in x:
        print(f"{i}  ")


def guess_row_gravity(b,c):
    rev_row = [5,4,3,2,1,0]
    for i in rev_row:
        if b[i][c] == 0:
            return i


def gravity_drop(b,p,r,c):
    b[r][c] = p


def win_cond(b,p):
    #Horizontal
    for i in range(6):
        for j in range(5):
            try:
                if p == 1:
                    if (b[i][j] == 1 and b[i][j+1] == 1 and b[i][j+2] == 1 and b[i][j+3] == 1) == True:
                        return True
                elif p == 2:
                    if (b[i][j] == 2 and b[i][j+1] == 2 and b[i][j+2] == 2 and b[i][j+3] == 2) == True:
                        return True
            except:
                pass

    #Vertical
        for i in range(4):
            for j in range(7):
                try:
                    if p == 1:
                        if (b[i][j] == 1 and b[i+1][j] == 1 and b[i+2][j] == 1 and b[i+3][j] == 1) == True:
                            return True
                    elif p == 2:
                        if (b[i][j] == 2 and b[i+1][j] == 2 and b[i+2][j] == 2 and b[i+3][j] == 2) == True:
                            return True
                except:
                    pass

    #Diagonals
        for i in range(6):
            for j in range(7):
                try:
                    if p == 1:
                        if (b[i][j] == 1 and b[i+1][j+1] == 1 and b[i+2][j+2] == 1 and b[i+3][j+3] == 1):
                            return True
                    elif p == 2:
                        if (b[i][j] == 2 and b[i+1][j+1] == 2 and b[i+2][j+2] == 2 and b[i+3][j+3] == 2):
                            return True
                except:
                    pass
        for i in range(6):
            for j in range(7):
                if i - 3 < 0:
                    continue
                try:
                    if p == 1:
                        if (b[i][j] == 1 and b[i-1][j+1] == 1 and b[i-2][j+2] == 1 and b[i-3][j+3] == 1):
                            return True
                    elif p == 2:
                        if (b[i][j] == 2 and b[i-1][j+1] == 2 and b[i-2][j+2] == 2 and b[i-3][j+3] == 2):
                            return True
                except:
                    pass
    return False


def simulated_gravity(b,p,c):
    fake_board = copy.deepcopy(b)
    r = guess_row_gravity(b,c)
    gravity_drop(fake_board,p,r,c)
    return fake_board


def score_frame(frame,piece):
    score = 0
    opp = 1 if piece == 2 else 2
    piece_no = frame.count(piece)
    empty_no = frame.count(0)
    opp_no = frame.count(opp)

    if piece_no == 4:
        score += 100
    elif piece_no == 3 and empty_no == 1:
        score += 5
    elif piece_no == 2 and empty_no == 2:
        score += 2
    elif opp_no == 3 and empty_no == 1:
        score -= 80

    return score


def score_pos(b,piece):
    score = 0
    centre_frames = []
    #Centre Bonus
    for r in range(6):
        centre_frames.append(b[r][3])
    centre_no = centre_frames.count(piece)
    score += centre_no*3

    #Horizontal Check
    for r in range(6):
        row_frames = b[r]
        for c in range(4):
            frame = row_frames[c:c+4]
            score += score_frame(frame,piece)

    #Vertical Check
    for c in range(7):
        col_frames = []
        for r in range(6):
            col_frames.append(b[r][c])
        for r in range(3):
            frame = col_frames[r:r+4]
            score += score_frame(frame,piece)

    #D1 Check \
    for r in range(3):
        for c in range(4):
            frame = [b[r][c],b[r+1][c+1],b[r+2][c+2],b[r+3][c+3]]
            score += score_frame(frame,piece)

    #D2 Check /
    for r in range(3,6):
        for c in range(4):
                    frame = [b[r][c],b[r-1][c+1],b[r-2][c+2],b[r-3][c+3]]
                    score += score_frame(frame,piece)

    return score


def validity(x):
    global run_next_line,p_column,p_row
    while True:
        if x == 1:
            print("------PLAYER'S TURN------")
        try: 
                p_column = int(input())-1
                p_row = guess_row_gravity(board,p_column)
                if p_row != None:
                    return p_column,p_row
                else:
                    print("Choose a valid position")
                    run_next_line=False
        except:
            print("Choose a valid position")
            run_next_line=False


#Added cuz AI was considering moves even after column full
def if_valid(b):
    valid = []
    for c in range(7):
        if b[0][c] == 0:
            valid.append(c)
    return valid


def end_point(b):
    return win_cond(b,p1) or win_cond(b,p2) or len(if_valid(b)) == 0


def minimax(b,depth,alpha,beta,playerswitch):
    valid_loc = if_valid(b)
    if_endpoint = end_point(b)

    #If The Game Ends
    if depth == 0 or if_endpoint:
        if if_endpoint:
            if win_cond(b, p2): #AI W
                return (None, 10000000)
            elif win_cond(b, p1): #AI L
                return (None, -10000000)
            else: #Tie
                return (None, 0)
        else:
            return (None, score_pos(b, p2))
    #AI's Turn
    if playerswitch:
        value = -math.inf
        best_col = random.choice(valid_loc)
        for c in valid_loc:
            b_copy = simulated_gravity(b,p2,c)
            new_score = minimax(b_copy,depth-1,alpha,beta,False)[1] #1 is the score 2nd return

            if new_score > value:
                value = new_score
                best_col = c

            #alpha update
            alpha = max(alpha,value)
            #prune
            if alpha >= beta:
                break

        return best_col, value
    #Player's Turn (minize AI score)
    else:
        value = math.inf
        best_col = random.choice(valid_loc)
        for c in valid_loc:
            b_copy = simulated_gravity(b,p1,c)
            new_score = minimax(b_copy,depth-1,alpha,beta,True)[1]

            if new_score < value:
                value = new_score
                best_col = c

                #beta update 
                beta = min(beta,value)
                #prune
                if beta <= alpha:
                    break

        return best_col, value


board = create_board()
p1 = 1
p2 = 2
display_board(board)


while True:
    run_next_line = True
    turn += 1
    #PLAYER
    validity(p1)
    if run_next_line:
        gravity_drop(board,p1,p_row,p_column)
        display_board(board)
    if win_cond(board,p1):
        print("-----------------------\n----PLAYER WINS!!!!----\n-----------------------")
        break
    #BOT
    print("---AI IS THINKING....!---")
    ai_c,minimax_score = minimax(board,6,-math.inf,math.inf,True)
    ai_r = guess_row_gravity(board,ai_c)
    if ai_r is not None:
        gravity_drop(board,p2,ai_r,ai_c)
        print("------AI BOT'S TURN------")
        display_board(board)

    if win_cond(board,p2):
        display_board(board)
        print("-----------------------\n----AI BOT WINS!!!!----\n-----------------------")
        break