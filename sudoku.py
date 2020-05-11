
__author__ = "Ryan DeMuse"
__license__ = "MIT"
__email__ = "ryan.demuse@du.edu"

"""
Todo:

    Add Reset Button - DONE / ADDED MAIN MENU INSTEAD
    Add Win Function - DONE
    Organize in Functions better
    Add checker to see if input is a number / if not, display a message and set text = '' - DONE
    Add Score Option - DONE
    Remove Redundant Code & Optimize
    Create a Button Class 
    Center Text in Rects - DONE
    Add Leaderboard
    Add Permutor to create a unique board each time through isomorphism classes of hardcoded boards

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
FONT = pygame.font.Font("Roboto-Medium.ttf", 32)
FONT_SMALL = pygame.font.Font("Roboto-Medium.ttf", 16)

# Predefined Sudoku game boars
def initialboard(difficulty: int = 3) -> List:
    if difficulty == 1:
        easy_1 = [[(0,0),9],[(0,1),1],
                    [(1,1),3],[(1,4),9],[(1,5),1],[(1,7),2],
                    [(2,1),6],[(2,2),5],[(2,3),4],[(2,6),3],[(2,7),7],
                    [(3,0),1],[(3,2),8],[(3,5),6],[(3,7),9],[(3,8),7],
                    [(4,3),7],[(4,5),8],
                    [(5,0),4],[(5,1),7],[(5,3),2],[(5,6),5],[(5,8),8],
                    [(6,2),6],[(6,3),1],[(6,5),5],[(6,6),9],
                    [(7,1),8],[(7,3),9],[(7,4),7],[(7,7),3],
                    [(8,7),8],[(8,8),1]]
        return easy_1
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
        return med_1
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
        return hard_1
    else:
        return easy_1
    return hard_1

# Create number boxes and user input boxes based on the initial board chosen
def create_board(taken_positions,number_boxes,input_boxes,board,difficulty):
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
def win(board):
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
def isTaken(coord: tuple, num: int, board) -> bool:
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
        #screen.blit(self.txt_surface, (self.rect.x+6, self.rect.y-2))

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

    # def update(self,taken):
    #     if taken:
    #         self.color = COLOR_TAKEN
    #     else:
    #         self.color = COLOR_INACTIVE

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
        #screen.blit(self.txt_surface, (self.rect.x+6, self.rect.y-2))

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
        #screen.blit(self.txt_surface, (self.rect.x+6, self.rect.y-2))

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

    def update(self,board):
        if win(board):
            self.text="You Win!"
        else:
            self.text="Not done"
        self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        super().__draw__(screen)

class ScoreBox(MessageBox):
    def __init__(self, x, y, w, h, text='',font=FONT_SMALL):
        super().__init__(x,y,w,h,text,font)

    def update(self,move):
        self.text = str(int(self.text)+move)
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


def menu():
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
                button("1",140,200,40,50,COLOR_INACTIVE,COLOR_ACTIVE,action=main)
                button("2",220,200,40,50,COLOR_INACTIVE,COLOR_ACTIVE,action=main)
                button("3",300,200,40,50,COLOR_INACTIVE,COLOR_ACTIVE,action=main)
                pygame.display.update()
                clock.tick(40)
    return

def main(difficulty):
    # Initialize board components
    board = numpy.zeros((9,9),dtype=int)
    Taken = numpy.zeros((9,9),dtype=bool)
    number_boxes = []
    taken_positions = []
    input_boxes = []
    create_board(taken_positions,number_boxes,input_boxes,board,difficulty)

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
            toggle = isTaken(coord,number,board)
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
        Hint = False
        for i in range(9):
            for j in range(9):
                Hint = Hint or Taken.item(i,j)

        # Indicate to user whether the move was invalid
        hintbox1.update(Hint)
        hintbox1.draw(screen)

        if numpy.array_equal(lastboard,board):
            scorebox1.update(0)
        elif (not numpy.array_equal(lastboard,board)) and (not Hint) and (not change_to_zero):
            scorebox1.update(1)
        elif (not numpy.array_equal(lastboard,board)) and (Hint) and (not change_to_zero):
            scorebox1.update(-1)
        else:
            scorebox1.update(0)

        scorebox1.draw(screen)

        # Indicate to user whether game is finished
        resetbox1.update(board)
        resetbox1.draw(screen)
        

        borders(screen)

        pygame.display.flip()
        clock.tick(40)

if __name__ == '__main__':
    menu()
    #main()
    pygame.quit()