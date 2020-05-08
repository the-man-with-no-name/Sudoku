# Add Reset Button
# Add Win Function - DONE
# Organize in Functions better
# Add checker to see if input is a number / if not, display a message and set text = '' - DONE
# Add Score Option

import pygame
import pygame.locals as pl
import numpy
pygame.init()

sq_dim = 480
screen = pygame.display.set_mode((sq_dim,sq_dim))
COLOR_INACTIVE = pygame.Color(156,156,156)
COLOR_ACTIVE = pygame.Color(255,255,255)
COLOR_TAKEN = pygame.Color(255,89,89)
ALLOWED = ['1','2','3','4','5','6','7','8','9']
FONT = pygame.font.Font("Roboto-Medium.ttf", 32)
board = numpy.zeros((9,9),dtype=int) # Current Board / 0 indicates empty box
Taken = numpy.zeros((9,9),dtype=bool) # Indicates whether the number in this box has already been taken
number_boxes = []
taken_positions = []
input_boxes = []


def create_board():
    top = 48
    left = 86
    y = 32
    init_board = initialboard()

    for position in init_board:
        pos = position[0]
        taken_positions.append(pos)
        num = position[1]
        number_boxes.append(NumBox(left+pos[0]*(y+1),top+pos[1]*(y+1),y,y,board_coordinates=(pos[0],pos[1]),value=num,text=str(num)))
        board[pos[0],pos[1]] = num

    for i in range(9):
        for j in range(9):
            if (i,j) not in taken_positions:
                input_boxes.append(InputBox(left+i*(y+1),top+j*(y+1),y,y,board_coordinates=(i,j)))

def borders(screen):
    shift = 32
    total = 296
    for i in range(9):
        pygame.draw.line(screen, COLOR_INACTIVE, (left,top+i*(shift+1)-1), (left+total,top+i*(shift+1)-1),4)

    pygame.draw.line(screen, COLOR_ACTIVE, (left,top), (left+total+2,top),4)
    pygame.draw.line(screen, COLOR_ACTIVE, (left,top), (left,top+total+2),4)
    pygame.draw.line(screen, COLOR_ACTIVE, (left+total,top), (left+total,top+total+2),4)
    pygame.draw.line(screen, COLOR_ACTIVE, (left,top+total), (left+total,top+total),4)

    pygame.draw.line(screen, COLOR_ACTIVE, (left,top+3*(shift+1)-1), (left+total,top+3*(shift+1)-1),4)
    pygame.draw.line(screen, COLOR_ACTIVE, (left,top+6*(shift+1)-1), (left+total,top+6*(shift+1)-1),4)

    pygame.draw.line(screen, COLOR_ACTIVE, (left+3*(shift+1)-1,top), (left+3*(shift+1)-1,top+total),4)
    pygame.draw.line(screen, COLOR_ACTIVE, (left+6*(shift+1)-1,top), (left+6*(shift+1)-1,top+total),4)

# Check whether the board is a Latin Square
def win():
    comp = numpy.array(list(range(1,10)))
    for i in range(9):
        if not (numpy.array_equal(board[i],comp) and numpy.array_equal(board[:,i],comp)):
            return False
    for offset_x in range(0,7,3):
        for offset_y in range(0,7,3):
            box_xy = []
            for smallbox_x in range(3):
                for smallbox_y in range(3):
                    box_xy.append(board.item(offset_x+smallbox_x,offset_y+smallbox_y))
            if not numpy.array_equal(numpy.array(box_xy),comp):
                return False
    return True
    

def initialboard(difficulty=1):
    if difficulty == 1:
        easy_1 = [[(0,0),9],[(0,1),1],
                    [(1,1),3],[(1,4),9],[(1,5),1],[(1,7),2],
                    [(2,1),6],[(2,2),5],[(2,3),4],[(2,6),3],[(2,7),7],
                    [(3,0),1],[(3,2),8],[(3,5),6],[(3,7),9],[(3,8),7],
                    [(4,3),7],[(4,5),8],
                    [(5,0),4],[(5,1),7],[(5,3),2],[(5,6),5],[(5,8),8],
                    [(6,2),6],[(6,3),1],[(6,5),5],[(6,6),9],[(6,7),7],
                    [(7,1),8],[(7,3),9],[(7,4),7],[(7,7),3],
                    [(8,7),8],[(8,8),1]]
    return easy_1


def isTaken(coord: tuple, num: int):
    for i in range(9):
        if board.item(i,coord[1]) == num and coord[0] != i and num != 0:
            return True
    for j in range(9):
        if board.item(coord[0],j) == num and coord[1] != j and num != 0:
            return True
    startx = coord[0]//3
    starty = coord[1]//3
    for i in range(startx*3,startx*3+3,1):
        for j in range(starty*3,starty*3+3,1):
            if board.item(i,j) == num and coord[0] != i and coord[1] != j and num != 0:
                return True
    return False


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


class TextBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = COLOR_ACTIVE
        self.hint = 0
        self.txt_surface = FONT.render(text, True, self.color)
        screen.blit(self.txt_surface, (self.rect.x+6, self.rect.y-2))

    def update(self,hint: bool):
        if hint:
            self.text="Try again"
        else:
            self.text="Go!"
        self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+6, self.rect.y))
        pygame.draw.rect(screen, self.color, self.rect, 2)


class WinBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = COLOR_ACTIVE
        self.hint = 0
        self.txt_surface = FONT.render(text, True, self.color)
        screen.blit(self.txt_surface, (self.rect.x+6, self.rect.y-2))

    def update(self):
        if win():
            self.text="You Win!"
        else:
            self.text="Not done"
        self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+6, self.rect.y))
        pygame.draw.rect(screen, self.color, self.rect, 2)


class NumBox:

    def __init__(self, x, y, w, h, text='', value=0, board_coordinates=(0,0)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = COLOR_INACTIVE
        self.hint = 0
        self.board_coordinates = board_coordinates
        self.value = value
        self.txt_surface = FONT.render(text, True, self.color)
        screen.blit(self.txt_surface, (self.rect.x+6, self.rect.y-2))

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+6, self.rect.y-2))
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Create input boxes
top = 48
left = 86
# y = 32
create_board()
resetbox1 = WinBox(left,top+310,150,40,text='Not done')
hintbox1 = TextBox(left,top+360,150,40,text='GO!')


# Run until user asks to quit
running = True 
while running:

    # Did user click window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for box in input_boxes:
            box.handle_event(event)

    for box in input_boxes:
        (coord,number) = box.get_attr()
        board[coord[0],coord[1]] = number
        toggle = isTaken(coord,number)
        if toggle:
            Taken[coord[0],coord[1]] = True
        else:
            Taken[coord[0],coord[1]] = False
        #box.update(toggle)

    screen.fill((0, 0, 0))
    for numbox in number_boxes:
        numbox.draw(screen)
    for box in input_boxes:
        box.draw(screen)

    Hint = False
    for i in range(9):
        for j in range(9):
            Hint = Hint or Taken.item(i,j)

    hintbox1.update(Hint)
    hintbox1.draw(screen)

    resetbox1.update()
    resetbox1.draw(screen)

    borders(screen)

    pygame.display.flip()

pygame.quit()