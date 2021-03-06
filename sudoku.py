__author__ = "Ryan DeMuse"
__license__ = "MIT"
__email__ = "ryan.demuse@du.edu"


"""

Todo:

    [Organized HIGH to LOW priority...]

    Organize in Functions better - 
    Remove Redundant Code & Optimize - 

"""

# Modules required
import pygame
import time
import numpy
from typing import List

# Initialize global variables
pygame.init()
SQ_DIM = 480
top = 48
left = 86
y = 32
screen = pygame.display.set_mode((SQ_DIM,SQ_DIM))
clock = pygame.time.Clock()
COLOR_INACTIVE = pygame.Color(156,156,156)
COLOR_ACTIVE = pygame.Color(255,255,255)
COLOR_TAKEN = pygame.Color(255,89,89)
ALLOWED = ['1','2','3','4','5','6','7','8','9']
FONT = pygame.font.Font("font/Roboto-Medium.ttf", 32)
FONT_SMALL = pygame.font.Font("font/Roboto-Medium.ttf", 16)


# Predefined Sudoku game boars
def initialboard(difficulty: int = 3) -> List:
    if difficulty == 1:
        easy_1 = [[(0,1),1],[(0,3),9],[(0,4),4],[(0,7),6],
                    [(1,1),2],[(1,3),7],[(1,5),6],[(1,6),1],[(1,8),3],
                    [(2,0),6],[(2,2),9],[(2,3),1],[(2,6),7],[(2,8),4],
                    [(3,2),7],[(3,3),4],
                    [(4,0),4],[(4,2),3],[(4,6),8],[(4,8),9],
                    [(5,5),8],[(5,6),4],
                    [(6,0),9],[(6,2),6],[(6,5),4],[(6,6),2],[(6,8),7],
                    [(7,0),2],[(7,2),1],[(7,3),6],[(7,5),5],[(7,7),3],
                    [(8,1),7],[(8,4),2],[(8,5),9],[(8,7),4]]
        return isomorphic_board(easy_1)
    elif difficulty == 2:
        med_1 = [[(0,0),6],[(0,1),4],[(0,3),9],
                    [(1,5),1],[(1,6),3],
                    [(2,8),2],
                    [(3,1),3],[(3,6),9],[(3,8),6],
                    [(4,0),1],[(4,6),7],[(4,7),5],
                    [(5,1),2],[(5,4),8],[(5,5),5],[(5,8),1],
                    [(6,5),8],
                    [(7,7),9],[(7,8),7],
                    [(8,0),2],[(8,1),7],[(8,2),9],[(8,7),6],[(8,8),4]]
        return isomorphic_board(med_1)
    elif difficulty == 3:
        hard_1 = [[(0,3),4],
                    [(1,5),8],[(1,7),9],[(1,8),6],
                    [(2,4),5],[(2,5),3],[(2,7),8],
                    [(3,1),4],[(3,2),8],
                    [(4,0),2],[(4,4),4],[(4,5),9],[(4,8),1],
                    [(5,0),6],[(5,6),5],[(5,8),9],
                    [(6,0),4],[(6,3),1],[(6,6),7],
                    [(7,1),8],[(7,3),9],[(7,6),4],
                    [(8,1),1],[(8,4),7],[(8,7),2]]
        return isomorphic_board(hard_1)
    else:
        return easy_1
    return hard_1


# Creates an isomorphic sudoku board
# Only symbol, row, column permutations implemented
#   TODO: Implement block and stack permutations
def isomorphic_board(board: List) -> List:
    iso_board = []
    permute_symbols = numpy.random.permutation(9)
    row_permutations = [numpy.random.permutation(range(3*i,3*(i+1))) for i in range(3)]
    col_permutations = [numpy.random.permutation(range(3*i,3*(i+1))) for i in range(3)]
    #block_permutation = numpy.random.permutation(range(3))
    #stack_permutation = numpy.random.permutation(range(3))
    for entry in board:
        pos = entry[0]
        val = entry[1]
        r_perm = row_permutations[pos[0]//3]
        c_perm = col_permutations[pos[1]//3]
        iso_board.append([(r_perm.item(pos[0]%3),c_perm.item(pos[1]%3)),permute_symbols.item(val-1)+1])
    return iso_board



# Create number boxes and user input boxes based on the initial board chosen
def create_board(taken_positions: List, number_boxes: List, input_boxes: List, board: List, difficulty: int) -> None:
    init_board = initialboard(difficulty)
    for position in init_board:
        pos = position[0]
        taken_positions.append(pos)
        num = position[1]
        number_boxes.append(NumBox(left+pos[1]*(y+1),top+pos[0]*(y+1),y,y,board_coordinates=(pos[0],pos[1]),value=num,text=str(num)))
        board[pos[0],pos[1]] = num
    for i in range(9):
        for j in range(9):
            if (i,j) not in taken_positions:
                input_boxes.append(InputBox(left+j*(y+1),top+i*(y+1),y,y,board_coordinates=(i,j)))

# Make the sudoku board look nice with borders and such
def borders(screen):
    shift = 32
    total = 296
    for i in range(9):
        pygame.draw.line(screen, COLOR_INACTIVE, (left,top+i*(shift+1)-1), (left+total,top+i*(shift+1)-1),4)

    pygame.draw.line(screen, COLOR_ACTIVE, (left-1,top-1), (left+total+2,top-1),4)
    pygame.draw.line(screen, COLOR_ACTIVE, (left,top), (left,top+total+2),4)
    pygame.draw.line(screen, COLOR_ACTIVE, (left+total,top), (left+total,top+total+2),4)
    pygame.draw.line(screen, COLOR_ACTIVE, (left,top+total), (left+total,top+total),4)

    pygame.draw.line(screen, COLOR_ACTIVE, (left,top+3*(shift+1)-1), (left+total,top+3*(shift+1)-1),4)
    pygame.draw.line(screen, COLOR_ACTIVE, (left,top+6*(shift+1)-1), (left+total,top+6*(shift+1)-1),4)

    pygame.draw.line(screen, COLOR_ACTIVE, (left+3*(shift+1)-1,top), (left+3*(shift+1)-1,top+total),4)
    pygame.draw.line(screen, COLOR_ACTIVE, (left+6*(shift+1)-1,top), (left+6*(shift+1)-1,top+total),4)


# Check whether the board has Sudoku Properties
#   1) Whole Board is Latin Square
#   2) Each subsquare has a distinct entries
def win(board: List) -> bool:
    comp = numpy.array(list(range(1,10)))
    # Latin Square Check
    for i in range(9):
        if not (numpy.array_equal(numpy.sort(board[i]),comp) and numpy.array_equal(numpy.sort(board[:,i]),comp)):
            return False
    # Subsquare Checks
    for offset_x in range(0,7,3):
        for offset_y in range(0,7,3):
            box_xy = []
            for smallbox_x in range(3):
                for smallbox_y in range(3):
                    box_xy.append(board.item(offset_x+smallbox_x,offset_y+smallbox_y))
            if not numpy.array_equal(numpy.sort(numpy.array(box_xy)),comp):
                return False
    return True

# Is this a valid number placement, i.e., does it maintain the Latin Square
#   property and the subsquare property?
def is_taken(coord: tuple, num: int, board) -> bool:
    # 0's are default values, do not check them
    if num != 0:
        # Latin Square rows
        for i in range(9):
            if board.item(i,coord[1]) == num and coord[0] != i:
                return True
        # Latin Square columns
        for j in range(9):
            if board.item(coord[0],j) == num and coord[1] != j:
                return True
        startx = coord[0]//3
        starty = coord[1]//3
        # Subsquare property?
        for i in range(startx*3,startx*3+3,1):
            for j in range(starty*3,starty*3+3,1):
                if board.item(i,j) == num and coord[0] != i and coord[1] != j:
                    return True
    return False


def find_first_empty_location(sboard) -> bool:
    for r in range(9):
        for c in range(9):
            if sboard.item(r,c) == 0:
                return (r,c)
    return (-1,-1)

# Solve Sudoku by backtracking
def sudoku_backtracking_solver(sboard) -> bool:
    loc = find_first_empty_location(sboard)
    if loc[0] == loc[1] == -1:
        return True
    (row,col) = loc
    for number in range(1,10):
        if not is_taken((row,col),number,sboard):
            sboard[row,col] = number
            if sudoku_backtracking_solver(sboard):
                return True
            sboard[row,col] = 0
    return False


# Class defining user input boxes
class InputBox:

    def __init__(self, x, y, w, h, text='', cursor_visible=True, max_string_length=1, board_coordinates=(0,0)):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.cursor_color = (0, 0, 1)
        self.cursor_visible = cursor_visible
        self.max_string_length = max_string_length # set to -1 for no limit
        self.board_coordinates = board_coordinates
        self.value = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < self.max_string_length or self.max_string_length == -1:
                    self.text += event.unicode
                if(self.text == ''):
                    self.value = 0
                elif(self.text in ALLOWED):
                    self.value = int(self.text)
                else:
                    self.text = ''
                    self.value = 0
                self.txt_surface = FONT.render(self.text, True, self.color)

    def get_attr(self):
        return (self.board_coordinates,self.value)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+6, self.rect.y-2))
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Number boxes from predefined board, not user interactive.
class NumBox:

    def __init__(self, x, y, w, h, text='', value=0, board_coordinates=(0,0)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = COLOR_INACTIVE
        self.hint = 0
        self.board_coordinates = board_coordinates
        self.value = value
        self.txt_surface = FONT.render(text, True, self.color)

    def draw(self, screen):
        surf = self.txt_surface.get_rect()
        surf.center = (self.rect.x+int(self.rect.w/2), (self.rect.y + int(self.rect.h/2)))
        screen.blit(self.txt_surface, surf)
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Messages to inform player
class MessageBox:

    def __init__(self, x, y, w, h, text, font=FONT):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = COLOR_ACTIVE
        self.hint = 0
        self.font = font
        self.txt_surface = font.render(text, True, self.color)

    def __draw__(self, screen):
        surf = self.txt_surface.get_rect()
        surf.center = (self.rect.x+int(self.rect.w/2), (self.rect.y + int(self.rect.h/2)))
        screen.blit(self.txt_surface, surf)
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Message to indicate whether the move just made was valid
class TextBox(MessageBox):

    def __init__(self, x, y, w, h, text='',font=FONT_SMALL):
        super().__init__(x,y,w,h,text,font)

    def update(self,hint: bool):
        if hint:
            self.text="Try again"
        else:
            self.text="Go!"
        self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        super().__draw__(screen)


# Message to indicate whether the board is properly completed
class WinBox(MessageBox):

    def __init__(self, x, y, w, h, text='',font=FONT_SMALL):
        super().__init__(x,y,w,h,text,font)
        self.win = False
        self.score_changed = False

    def update(self,board):
        if win(board):
            self.text="You Win!"
            self.win = True
        else:
            self.text="Not done"
        self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        super().__draw__(screen)


class ScoreBox(MessageBox):
    def __init__(self, x, y, w, h, text='',font=FONT_SMALL):
        super().__init__(x,y,w,h,text,font)
        self.value = 0

    def update(self,move):
        self.value += move
        self.text = str(self.value)
        self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        super().__draw__(screen)


def text_objects(text, font):
    textSurface = font.render(text, True, pygame.Color(0,0,0))
    return textSurface, textSurface.get_rect()


def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            difficulty = int(msg)
            action(difficulty)
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))
    textSurf, textRect = text_objects(msg, FONT_SMALL)
    textRect.center = ( (x+int(w/2)), (y+int(h/2)) )
    screen.blit(textSurf, textRect)

# Get the list of Highscores from the file: highscores.txt
def get_highscores():
    scores = []
    scoreBoxes = []
    with open('data/highscores.txt') as f:
        scores = f.readlines()
        scores = sorted([int(score.rstrip()) for score in scores],reverse=True)
        f.close()
    space = 10
    height = 20
    i = 0
    for score in scores:
        scoreBoxes.append(MessageBox(200,330+space*i+height*(i-1),80,height,text="{}".format(score),font=FONT_SMALL))
        i += 1
    return scoreBoxes

# Update the highscores.txt file
def update_leaderboard(new_score: int) -> None:
    scores = []
    with open('data/highscores.txt') as f:
        scores = f.readlines()
        scores = sorted([int(score.rstrip()) for score in scores])
        f.close()
    if len(scores) != 0:
        i = 0
        if new_score <= scores[i]:
            return
        while new_score > scores[i] and i < len(scores)-1:
            i += 1
        if i > 0:
            for j in range(i):
                scores[j] = scores[j+1]
            scores[i-1] = new_score
        with open('data/highscores.txt','w') as f:
            scores = sorted(scores,reverse=True)
            f.seek(0)
            f.truncate()
            for score in scores:
                f.write("{}\n".format(score))
            f.close()

# Update user score
def update_score(lastboard,board,Hint,change_to_zero,changed_up_one,scorebox1,screen):
    if numpy.array_equal(lastboard,board):
        scorebox1.update(0)
    elif (not numpy.array_equal(lastboard,board)) and (not change_to_zero):
        (r,c) = matrix_not_equal(lastboard,board)
        if (not Hint) and (not changed_up_one.item(r,c)):
            scorebox1.update(1)
            # Only allow a box to increase the score once
            changed_up_one[r,c] = True
        elif Hint:
            scorebox1.update(-1)
        else:
            scorebox1.update(0)
    else:
        scorebox1.update(0)
    scorebox1.draw(screen)

# Returns lexicographic first place two matrices not equal if the matrices are the same shape
def matrix_not_equal(A,B):
    row = -1
    col = -1
    if A.shape == B.shape:
        (nrows,ncols) = A.shape
        for i in range(nrows):
            if not numpy.array_equal(A[i],B[i]):
                row = i
        for j in range(ncols):
            if not numpy.array_equal(A[:,j],B[:,j]):
                col = j
        return (row,col)
    else:
        return (row,col)


def main():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            else:
                screen.fill((0, 0, 0))
                sudoku = MessageBox(140,50,200,50,text="SUDOKU!")
                sudoku.__draw__(screen)
                selectdiff = MessageBox(165,150,150,30,text="Select Difficulty",font=FONT_SMALL)
                selectdiff.__draw__(screen)
                button("1",140,200,40,50,COLOR_INACTIVE,COLOR_ACTIVE,action=game)
                button("2",220,200,40,50,COLOR_INACTIVE,COLOR_ACTIVE,action=game)
                button("3",300,200,40,50,COLOR_INACTIVE,COLOR_ACTIVE,action=game)
                highscores = MessageBox(165,270,150,30,text="Highscores",font=FONT_SMALL)
                scoreBoxes = get_highscores()
                for scoreBox in scoreBoxes:
                    scoreBox.__draw__(screen)
                highscores.__draw__(screen)
                pygame.display.update()
                clock.tick(40)
    return

def game(difficulty):
    # Initialize board components
    board = numpy.zeros((9,9),dtype=int)
    Taken = numpy.zeros((9,9),dtype=bool)
    # lastlastboard = numpy.zeros((9,9),dtype=int)
    lastboard = numpy.zeros((9,9),dtype=int)
    number_boxes = []
    taken_positions = []
    input_boxes = []
    changed_up_one = numpy.zeros((9,9),dtype=bool)
    create_board(taken_positions,number_boxes,input_boxes,board,difficulty)
    sboard = numpy.copy(board)
    sudoku_backtracking_solver(sboard)
    print(sboard)

    # Create Progress Messages
    resetbox1 = WinBox(left,top+310,150,40,text='Not done',font=FONT)
    hintbox1 = TextBox(left,top+360,150,40,text='GO!',font=FONT)
    scorebox1 = ScoreBox(left+170,top+310,100,40,text='0',font=FONT)

    # Run until user asks to quit
    running = True 
    while running:
        lastboard = numpy.copy(board)
        change_to_zero = False

        # Did user click window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for box in input_boxes:
                box.handle_event(event)

        # Check whether moves were valid
        for box in input_boxes:
            (coord,number) = box.get_attr()
            board[coord[0],coord[1]] = number
            if lastboard[coord[0],coord[1]] != 0 and number == 0:
                change_to_zero = True
            toggle = is_taken(coord,number,board)
            if toggle:
                Taken[coord[0],coord[1]] = True
            else:
                Taken[coord[0],coord[1]] = False

        # Draw the number the user inputed
        screen.fill((0, 0, 0))
        for numbox in number_boxes:
            numbox.draw(screen)
        for box in input_boxes:
            box.draw(screen)

        # Are there any invalid moves on the board?
        Hint = numpy.any(Taken)

        # Update Hint Message
        hintbox1.update(Hint)
        hintbox1.draw(screen)

        # Update user score
        update_score(lastboard,board,Hint,change_to_zero,changed_up_one,scorebox1,screen)

        # Indicate to user whether game is finished
        resetbox1.update(board)
        resetbox1.draw(screen)

        # Edit highscores if user won and score merits leaderboard
        if resetbox1.win and not resetbox1.score_changed:
            new_score = int(scorebox1.text)
            update_leaderboard(new_score)
            resetbox1.score_changed = True

        borders(screen)

        pygame.display.update()
        clock.tick(40)
    screen.fill((0, 0, 0))
    pygame.display.update()