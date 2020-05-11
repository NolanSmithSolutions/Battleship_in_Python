import random
board_yours=[]
board_guess=[]
board_ai=[]
board_aiguess=[]
ships=["Destroyer","Submarine","Cruiser","Battleship","Carrier"]
player_ship_hits={"C":0, "B":0, "R":0, "S":0,"D":0}
ai_ship_hits={"C":0, "B":0, "R":0, "S":0,"D":0}
ai_first_hit={"C":[9,9], "B":[9,9], "R":[9,9], "S":[9,9],"D":[9,9]}
ai_last_move=[9,-9]
ai_last_dir="u"
ai_last_hit="N"
curr_move=[9,9]

def game_start():
    """Creates the original 4 game boards (Player's, Player's Guess, AI's, AI's Guess) by appending blank "*" lists"""
    row=["*","*","*","*","*","*","*","*"]
    for x in range(0,8):
        board_yours.append(row[:])
        board_guess.append(row[:])
        board_ai.append(row[:])
        board_aiguess.append(row[:])

def display_board(board):
    """Prints a board to screen"""
    count=8
    for row in board:
        print("  "+"-"*33)
        print(str(count) +  " | " + " | ".join(row) + " |")
        count-=1
    print("  "+"-"*33)
    print("    A   B   C   D   E   F   G   H")

def in_hit_seq():
    """This is used for AI strategy - if they have more than one hit one a certain ship they will continue searching near that ship's initial hit until they sink it"""
    if ai_ship_hits["C"]>0 and ai_ship_hits["C"]<5:
        return "C"
    elif ai_ship_hits["B"]>0 and ai_ship_hits["B"]<4:
        return "B"
    elif ai_ship_hits["R"]>0 and ai_ship_hits["R"]<3:
        return"R"
    elif ai_ship_hits["S"]>0 and ai_ship_hits["S"]<3:
        return "S"
    elif ai_ship_hits["D"]>0 and ai_ship_hits["D"]<2:
        return "D"
    else:
        return "N"

def announce(x):
    """Prints out how many ships the player/ai has sunk"""
    lst=""
    if x["C"]==5:
        lst+=(" Carrier")
    if x["B"]==4:
        lst+=(" Battleship")
    if x["R"]==3:
        lst+=(" Cruiser")
    if x["S"]==3:
        lst+=(" Submarine")
    if x["D"]==2:
        lst+=(" Destroyer")
    print("List of ships sunk:", lst)   
    
def ship_length(ship):
    """Contains ship lengths of different ships as well as how many spaces a guess takes, used in board placement and checking functions"""
    if ship=="Carrier":
        return 5
    if ship=="Battleship":
        return 4
    if ship=="Cruiser":
        return 3
    if ship=="Submarine":
        return 3
    if ship=="Destroyer":
        return 2
    if ship=="Guess":
        return 1

def shipping(ship):
    """Contains board placement identifier of ships, used in board placement and checking functions"""
    if ship=="Carrier":
        return "C"
    if ship=="Battleship":
        return "B"
    if ship=="Cruiser":
        return "R"
    if ship=="Submarine":
        return "S"
    if ship=="Destroyer":
        return "D"

def opens(board, xpos, ypos, ship, direct):
    """Can I guess in the direction of my current position with a ship of this length?"""
    count=ship_length(ship)
    while count>0:
        if xpos<0 or ypos<0 or xpos>=8 or ypos>=8:
            return False
        elif board[ypos][xpos]=="*":
            count-=1
            if direct=="right_open":
                xpos+=1
            elif direct=="left_open":
                xpos-=1
            elif direct=="down_open":
                ypos+=1
            elif direct=="up_open":
                ypos-=1
            else:
                print("Something wrong with open function")
        else:
            return False
    return True

options=["left_open", "right_open", "up_open", "down_open"]

def ai_start():
    """Creates a starting position for the AI"""
    s=4
    while s>-1:
        x=random.randint(0,7)
        y=random.randint(0,7)
        ship=ships[s]
        choice=random.choice(options)
        if opens(board_ai, x, y, ship, choice) is True:
            place(board_ai,choice, ship, x, y)
            s-=1
    #announce(ai_ship_hits)
    #display_board(board_ai)

def place(board, direction, how, xpos, ypos):
    """Updates a chosen board on a particular place for a guess or ship placement"""
    length=ship_length(how)
    while length>0:
        board[ypos][xpos]=shipping(how)
        length-=1
        if direction=="left_open":
            xpos-=1
        elif direction=="right_open":
            xpos+=1
        elif direction=="up_open":
            ypos-=1
        elif direction=="down_open":
            ypos+=1
        else:
            print("ERROR with board placement")

def player_start():
    """Player inputs their starting position and will continually be asked to give such if they give impossible starting conditions"""
    s=4
    while s>-1:
        ship=ships[s]
        i = 1
        #https://stackoverflow.com/questions/38707513/ignoring-an-error-message-to-continue-with-the-loop-in-python
        #https://stackoverflow.com/questions/2083987/how-to-retry-after-exception
        while i > 0:
            try:
                x,y,direct="Z","Z","Z"
                x,y,direct=input("Please enter the x,y coordinates and direction [A-H,1-8,U/D/L/R] (ie: A 3 R) \n for where to put your "
                                 + str(ship) + " which is "
                          + str(ship_length(ship)) + " spaces long: ").split(' ')
                #https://stackoverflow.com/questions/4528982/convert-alphabet-letters-to-number-in-python
                x=ord(x)-65
                y=8-int(y)
            except ValueError:
                print("Error 1: You have chosen an invalid position (only A-H for x-coordinate and 1-8 for y-coordinate work).")
                continue
            except TypeError:
                print("Error 2: You have chosen an invalid position (only A-H for x-coordinate and 1-8 for y-coordinate work).")
                continue
            except x<0 or y<0 or x>=8 or y>=8:
                print("Error 3: You have chosen an invalid position (only A-H for x-coordinate and 1-8 for y-coordinate work).")
                continue
            except UnboundLocalError:
                print("Error 4: You have not entered in enough information")
                continue
            finally:
                if direct != "R" and direct != "L" and direct != "U" and direct != "D":
                        print("You have chosen a wrong direction, you can only choose from U, D, L or R.")
                else:
                    break         
        if direct=="U":
            choice="up_open"
        elif direct=="D":
            choice="down_open"
        elif direct=="L":
            choice="left_open"
        else:
            choice="right_open"
        if opens(board_yours, x, y, ship, choice) is True:
            place(board_yours,choice, ship, x, y)
            display_board(board_yours)
            s-=1
        else:
            print("You have chosen a position where a ship cannot be placed.")

def hit_or_miss(yours, theirs, how, xpos, ypos):
    """Updates boards with a hit or misses for guesses as well as updating information relevant to AI strategy such as if they are in a hit sequences, their last guess, last guess direction, etc."""
    #https://stackoverflow.com/questions/10588317/python-function-global-variables
    global ai_last_dir, ai_last_move, curr_move, ai_last_hit
    length=1
    while length>0:
        if theirs[ypos][xpos]!="*":
            print("That was a hit at",chr(xpos+65),8-ypos,"!")
            yours[ypos][xpos]="H"
            if how=="ai":
                ai_ship_hits[theirs[ypos][xpos]]+=1
                if ai_ship_hits[theirs[ypos][xpos]]==1:
                    ai_first_hit[theirs[ypos][xpos]][0],ai_first_hit[theirs[ypos][xpos]][1]=xpos,ypos
                ai_last_hit="Y"
                curr_move[0],curr_move[1]=xpos,ypos
                if in_hit_seq()!="N":
                    if curr_move[1]>ai_first_hit[in_hit_seq()][1]:
                        ai_last_dir='d'
                    elif curr_move[1]<ai_first_hit[in_hit_seq()][1]:
                        ai_last_dir='u'
                    elif curr_move[0]>ai_first_hit[in_hit_seq()][0]:
                        ai_last_dir='r'
                    else:
                        ai_last_dir='l'
                else:
                    ai_last_dir='u'
                ai_last_move[0]=xpos
                ai_last_move[1]=ypos
                theirs[ypos][xpos]="H"
            elif how=="player":
                player_ship_hits[theirs[ypos][xpos]]+=1
        else:
            print("That was a miss at",chr(xpos+65),8-ypos,"!")
            yours[ypos][xpos]="M"
            if how=="ai":
                ai_last_hit="N"
                curr_move[0],curr_move[1]=xpos,ypos
                if curr_move[1]>ai_last_move[1]:
                    ai_last_dir='d'
                elif curr_move[1]<ai_last_move[1]:
                    ai_last_dir='u'
                elif curr_move[0]>ai_last_move[0]:
                    ai_last_dir='r'
                else:
                    ai_last_dir='l'
                ai_last_move[0]=xpos
                ai_last_move[1]=ypos
                theirs[ypos][xpos]="M"
        length-=1

def ai_try_same(xpos, ypos, ship, yours, theirs):
    """If the last move was a hit, can the AI keep to move the way have been going?"""
    global ai_last_dir, ai_last_move, curr_move, ai_last_hit
    if ai_last_dir=="d" and opens(theirs, xpos, ypos+1, ship, "down_open"):
        hit_or_miss(board_aiguess, board_yours,"ai",ai_last_move[0],ai_last_move[1]+1)
    elif ai_last_dir=="u" and opens(theirs, xpos, ypos-1, ship, "up_open"):
        hit_or_miss(board_aiguess, board_yours,"ai",ai_last_move[0],ai_last_move[1]-1)
    elif ai_last_dir=="r" and opens(theirs, xpos+1, ypos, ship, "right_open"):
        hit_or_miss(board_aiguess, board_yours,"ai",ai_last_move[0]+1,ai_last_move[1])
    elif ai_last_dir=="l" and opens(theirs, xpos-1, ypos, ship, "left_open"):
        hit_or_miss(board_aiguess, board_yours,"ai",ai_last_move[0]-1,ai_last_move[1])
    else:
        ai_try_start(ai_first_hit[in_hit_seq()][0], ai_first_hit[in_hit_seq()][1], "Guess", board_yours, board_aiguess)

def ai_try_start(xpos, ypos, ship, yours, theirs):
    """The AI has missed their last guess but are in a hit sequences, they must go back to their original hit for that ship and try a new direction"""
    global ai_last_dir, ai_last_move, curr_move, ai_last_hit
    if opens(theirs, xpos, ypos+1, ship, "down_open"):
        hit_or_miss(board_aiguess, board_yours,"ai",xpos,ypos+1)
    elif opens(theirs, xpos, ypos-1, ship, "up_open"):
        hit_or_miss(board_aiguess, board_yours,"ai",xpos,ypos-1)
    elif opens(theirs, xpos-1, ypos, ship, "left_open"):
        hit_or_miss(board_aiguess, board_yours,"ai",xpos-1,ypos)
    elif opens(theirs, xpos+1, ypos, ship, "right_open"):
        hit_or_miss(board_aiguess, board_yours,"ai",xpos+1,ypos)
    else:
        print("Error nothing is open!")

def ai_turn(yours, theirs):
    """"AI strategy - if in hit sequences, try to finish off the ship; if not, guess randomly on an open spot"""
    s=1
    while s>0:
        if in_hit_seq()!="N":
            if ai_last_hit=="Y":
                ai_try_same(ai_last_move[0],ai_last_move[1],"Guess",board_yours, board_aiguess)
                s-=1
            else:
                ai_try_start(ai_first_hit[in_hit_seq()][0], ai_first_hit[in_hit_seq()][1], "Guess", board_yours, board_aiguess)
                s-=1
        else:
            x=random.randint(0,7)
            y=random.randint(0,7)
            if theirs[y][x]=="*":
                hit_or_miss(theirs, yours,"ai", x, y)
                s-=1
    announce(ai_ship_hits)
    print("AI's guess for your board:")
    display_board(yours)
    if win(theirs,"ai"):
        return False
    else:
        return True

def player_turn(yours, theirs):
    """Player takes a guess for a new spot via user input, error correcting code if they try invalid positions"""
    x,y,direct="Z","Z","Z"
    while True:
        try:
            count=0
            x,y=input("Please enter the x,y coordinates [A-H,1-8] of your guess (ie: A 3) \n").split(' ')
            x=ord(x)-65
            y=8-int(y)
            if opens(yours, x, y, "Guess", "up_open") is False:
                print("Error 3: You have chosen a spot you have already guessed.")
                count+=1
            if (x<0 or y<0 or x>=8 or y>=8) is True:
                print("Error 4: You have chosen an invalid position (only A-H for x-coordinate and 1-8 for y-coordinate work).")
                count+=1
        except ValueError:
            print("Error 1: You have chosen an invalid position (only A-H for x-coordinate and 1-8 for y-coordinate work).")
            count+=1
            continue
        except TypeError:
            print("Error 2: You have chosen an invalid position (only A-H for x-coordinate and 1-8 for y-coordinate work).")
            count+=1
            continue
        except UnboundLocalError:
                print("Error 5: You have not entered in enough information")
                count+=1
                continue
        finally:
            if count < 1:
                break
    hit_or_miss(yours,theirs,"player", x, y)
    announce(player_ship_hits)
    print("Your guess for their board:")
    display_board(yours)
    if win(yours,"player"):
        return False
    else:
        return True

def win(board, t):
    """Checks if the player or AI has won, counts their hits and misses, prints that result"""
    count=0
    miss=0
    for x in range(len(board_yours)):
        for y in range(len(board_yours[x])):
            if board[x][y]=="H":
                count+=1
            if board[int(x)][int(y)]=="M":
                miss+=1
    print("Count of hits :", count)
    print("Count of misses :", miss)
    if count < 17:
        return False
    elif count>=17 and t=="ai":
        print("The AI has beat you!")
        return True
    elif count>=17 and t=="player":
        print("Congratulations!  You have won!")
        return True
    else:
        print("Error with win function")

"""The game sequence is below.  Player or AI is choose their boards and one is randomly chosen to go first.  The players keep competing until there is a winner.
    A board is commented out in case someone wishes to test something and doesn't want to continually choose a starting place.  Simply comment out player start
    and remove the comment before the board_yours line"""

game_start()
display_board(board_yours)
ai_start()
player_start()
#board_yours=[['B', 'B', 'B', 'B', '*', '*', '*', 'R'], ['*', '*', '*', '*', '*', '*', '*', 'R'], ['*', '*', '*', '*', '*', '*', '*', 'R'], ['C', '*', '*', '*', '*', '*', '*', '*'], ['C', '*', '*', '*', '*', '*', '*', '*'], ['C', '*', '*', '*', '*', '*', '*', '*'], ['C', '*', 'D', '*', '*', '*', '*', '*'], ['C', '*', 'D', '*', '*', 'S', 'S', 'S']]
start=random.randint(0,1)
if start==1:
    print("You go first")
    player_turn(board_guess, board_ai)
else:
    print("The AI goes first")
while True:
    print("\nAI's Turn:")
    if not ai_turn(board_yours, board_aiguess):
        break
    print("\nPlayer's Turn:")
    if not player_turn(board_guess, board_ai):
        break
