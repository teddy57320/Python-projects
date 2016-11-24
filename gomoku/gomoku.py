# "b" indicates black pieces, which is the computer. The user plays as white, denoted by "w".
# The computer operates by calculating which move grants a 
# maximum "score", which increases with increasing importance.

def is_empty(board):                                            
# checks if board is empty
    for y in range (len(board)):
        for x in range (len(board)):
           if board[y][x] != " ":
               return False
    return True
    
def is_bounded(board, y_end, x_end, length, d_y, d_x):     
# checks if a sequence of pieces of a single color are bounded, semibounded, or open.
# d_y and d_x are the directions in which we check for bounding.
    end_bounded = False                                         
    start_bounded = False
    
    if (((y_end + d_y) not in range(0, len(board))) or ((x_end + d_x) not in range (0, len(board)))):   
    # checks if next piece in sequence is bounded by the wall
        end_bounded = True
        
    elif board[y_end + d_y][x_end + d_x] == board[y_end][x_end]:        
    # if not, then check if it is bounded by a piece of the same color                                       
        return None
        
    elif board[y_end + d_y][x_end + d_x] != " ":                        
    # if the next piece in the d_y, d_x direction is not unoccupied, then it is bounded by a piece of the opponent
        end_bounded = True
        
    if ((y_end - d_y*length) not in range(-1, len(board)+1)) or ((x_end - d_x*length) not in range (-1, len(board)+1)): 
    # these cases below handle errors that may arise from going out of bound
        return None
        
    if ((y_end - d_y*length) not in range(0, len(board))) or ((x_end - d_x*length) not in range (0, len(board))):
        start_bounded = True
    elif board[y_end - d_y*length][x_end - d_x*length] == board[y_end][x_end]:
        return None
    elif board[y_end - d_y*length][x_end - d_x*length] != " ":
        start_bounded = True
    if ((y_end - d_y*(length-1)) in range(0, len(board))) and ((x_end - d_x*(length-1)) in range (0, len(board))):
        for i in range (1, length):
            if board[y_end-i*d_y][x_end-i*d_x] != board[y_end][x_end]:
                return None

    if start_bounded and end_bounded:
        return "CLOSED"
    if start_bounded ^ end_bounded:
        return "SEMIOPEN"
    return "OPEN"
    
    
def detect_row(board, col, y_start, x_start, length, d_y, d_x):    
# used to determine how many open and semi open sequences are available
    open_seq_count, semi_open_seq_count = 0, 0
    while y_start < len(board) and x_start < len(board) and x_start > -1 and y_start > -1:
        if ((y_start + d_y*(length - 1)) in range (0, len(board))) and ((x_start + d_x*(length - 1)) in range (0, len(board))):
            if board[y_start][x_start] == col:
                for i in range (length - 1):
                    x_start += d_x
                    y_start += d_y
                    if board[y_start][x_start] != col:
                        y_start -= d_y
                        x_start -= d_x
                        break
                    
                if is_bounded(board, y_start, x_start, length, d_y, d_x) == "OPEN":
                    open_seq_count += 1
                if is_bounded(board, y_start, x_start, length, d_y, d_x) == "SEMIOPEN":
                    semi_open_seq_count += 1
                    
        x_start += d_x
        y_start += d_y
        
    return open_seq_count, semi_open_seq_count
    
def detect_rows(board, col, length):       
# counts number of open and semi open sequences with a specified color and length
    open_seq_count, semi_open_seq_count = 0, 0
    for verticals in range (len(board)):
        open_seq_count += detect_row(board, col, 0, verticals, length, 1, 0)[0]
        semi_open_seq_count += detect_row(board, col, 0, verticals, length, 1, 0)[1]
    for diagonals1 in range (1, len(board)):
        open_seq_count += detect_row(board, col, diagonals1, 0, length, 1, 1)[0]
        semi_open_seq_count += detect_row(board, col, diagonals1, 0, length, 1, 1)[1]
        open_seq_count += detect_row(board, col, 0, diagonals1, length, 1, 1)[0]
        semi_open_seq_count += detect_row(board, col, 0, diagonals1, length, 1, 1)[1]
    open_seq_count += detect_row(board, col, 0, 0, length, 1, 1)[0]
    semi_open_seq_count += detect_row(board, col, 0, 0, length, 1, 1)[1]
    
    for diagonals2 in range (1, len(board)):
        open_seq_count += detect_row(board, col, diagonals2, len(board)-1, length, 1, -1)[0]
        semi_open_seq_count += detect_row(board, col, diagonals2, len(board)-1, length, 1, -1)[1]
        open_seq_count += detect_row(board, col, 0, diagonals2, length, 1, -1)[0]
        semi_open_seq_count += detect_row(board, col, 0, diagonals2, length, 1, -1)[1]
    open_seq_count -= detect_row(board, col, 0, len(board)-1, length, 1, -1)[0]
    semi_open_seq_count -= detect_row(board, col, 0, 0, len(board)-1, 1, -1)[1]
    
    for horizontals in range (0, len(board)):
        open_seq_count += detect_row(board, col, horizontals, 0, length, 0, 1)[0]
        semi_open_seq_count += detect_row(board, col, horizontals, 0, length, 0, 1)[1]
    
    return open_seq_count, semi_open_seq_count
    
def search_max(board):  
#computes a move for the computer that will grant maximum "score" based on the board state

    max_score = -2000000
    move_y = 4
    move_x = 4
    for y in range (len(board)):
        for x in range(len(board)):
            if board[y][x] == " ":
                board[y][x] = "b"
                
                if score(board) > max_score:
                    max_score = score(board)
                    move_y, move_x = y, x
                board[y][x] = " "
    return move_y, move_x
    
def score(board):       
#counts the score of a particular move

    MAX_SCORE = 100000
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 7):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+  #relative weights of occurring sequences 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

def detect_5(board, col):       
# detects if there is 5 in a row for a given color.

    
    for a in range(len(board)-4):
        for b in range(len(board)):
            count = 0
            if board[a][b] == col:
                for vertical in range (1, 5):
                    if board[a + vertical][b] == col:
                        count += 1
                if count == 4:
                    if a != 0 and a != len(board)-5:
                       if board[a-1][b] != col and board[a+5][b] != col:
                           return True
                    if a == 0:
                        if board[a+5][b] != col:
                            return True
                    if a == len(board)-5:
                        if board[a-1][b] != col:
                            return True
    
    for c in range(len(board)):
        for d in range(len(board)-4):
            count = 0
            if board[c][d] == col:
                for horizontal in range (1,5):
                    if board[c][d + horizontal] == col:
                        count += 1
                if count == 4:
                    if d != 0 and d != len(board)-5:
                       if board[c][d-1] != col and board[c][d+5] != col:
                           return True
                    if d == 0:
                        if board[c][d+5] != col:
                            return True
                    if d == len(board)-5:
                        if board[c][d-1] != col:
                            return True
    for e in range(len(board)-4):
        for f in range(4, len(board)):
            count = 0
            if board[e][f] == col:
                for diagonal2 in range (1, 5):
                    if board [e + diagonal2][f - diagonal2] == col:
                        count+= 1
                if count == 4:
                    if e in range (1, len(board)-5) and f in range (5,len(board)-1):
                        if board[e-1][f+1] != col and board[e+5][f-5] != col:
                           return True
                    if e == 0 or f == len(board)-1:
                        if (e+5 >= len(board)) or (f-5 >= len(board)):
                            return True
                        if board[e+5][f-5] != col:
                            return True
                    if e == len(board)-5 or f == 4:
                        if board[e-1][f+1] != col:
                            return True
    for y in range(len(board)-4):
        for x in range(len(board)-4):
            count = 0
            if board[y][x] == col:
                for diagonal1 in range (1, 5):
                    if board [y + diagonal1][x + diagonal1] == col:
                        count += 1
                if count == 4:
                    if y in range (1, len(board)-5) and x in range (1,len(board)-5):
                        if board[y-1][x-1] != col and board[e+5][f+5] != col:
                           return True
                    if y == 0 or x == 0:
                        if (y+5 >= len(board)) or (x+5 >= len(board)):
                            return True
                        if board[y+5][x+5] != col:
                            return True
                    if y == len(board)-5 or x == len(board)-5:
                        if board[y-1][x-1] != col:
                            return True
    return False
                
            
        
def is_win(board):      
# checks if either side won, or if there is a draw

    if detect_5(board, "b") == True:
        return "Black won"
    if detect_5(board, "w") == True:
        return "White won"
    for a in range (len(board)):
        for b in range(len(board)):
            if board[a][b] == " ":
                return "Continue playing"
    return "Draw"
    
def print_board(board):     
# shows the board state to the user

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)
    
def make_empty_board(sz):      
# initializes board

    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board
                

def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)     
            # computes best move for the computer
       
        print("Computer move: (%d, %d)" % (move_y, move_x))    
        # computer makes the move
         
        board[move_y][move_x] = "b"
        print_board(board)          
        
        game_res = is_win(board)                                
        # check for victory
        
        if game_res in ["White won", "Black won", "Draw"]:
            print (game_res)
            return None
            
        print("Your move:")               
        # allows users to input x and y indices to make a move on the board
        
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            print (game_res)
            return None

if __name__ == '__main__':    
    play_gomoku(10)                  
    # the size of the board is variable, although computation time goes up with board size
    