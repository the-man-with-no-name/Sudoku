import pygame
import pygame.locals as pl
import numpy
pygame.init()

sq_dim = 480
screen = pygame.display.set_mode((sq_dim,sq_dim))
COLOR_INACTIVE = pygame.Color(156,156,156)
COLOR_ACTIVE = pygame.Color(255,255,255)
FONT = pygame.font.Font("Roboto-Medium.ttf", 32)
board = numpy.zeros((9,9),dtype=int)


def borders(screen):
    shift = 33
    total = 296
    pygame.draw.line(screen, pygame.Color(255,255,255), (left,top), (left+total,top),4)
    pygame.draw.line(screen, pygame.Color(255,255,255), (left,top), (left,top+total),4)
    pygame.draw.line(screen, pygame.Color(255,255,255), (left+total,top), (left+total,top+total),4)
    pygame.draw.line(screen, pygame.Color(255,255,255), (left,top+total), (left+total,top+total),4)

    pygame.draw.line(screen, pygame.Color(255,255,255), (left,top+3*shift), (left+total,top+3*shift),4)
    pygame.draw.line(screen, pygame.Color(255,255,255), (left,top+6*shift), (left+total,top+6*shift),4)

    pygame.draw.line(screen, pygame.Color(255,255,255), (left+3*shift,top), (left+3*shift,top+total),4)
    pygame.draw.line(screen, pygame.Color(255,255,255), (left+6*shift,top), (left+6*shift,top+total),4)

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


def isTaken(coord,num):
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

    def __init__(self, x, y, w, h, text='',cursor_visible=True,max_string_length=1,board_coordinates=(0,0)):
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
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    #self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < self.max_string_length or self.max_string_length == -1:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)
                if(self.text == ''):
                    self.value = 0
                else:
                    self.value = int(self.text)

    def update(self):
        # Resize the box if the text is too long.
        width = max(32, self.txt_surface.get_width()+10)
        self.rect.w = width
        return (self.board_coordinates,self.value)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+6, self.rect.y-2))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class TextBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = COLOR_ACTIVE
        self.hint = 0
        self.txt_surface = FONT.render(text, True, self.color)
        screen.blit(self.txt_surface, (self.rect.x+6, self.rect.y-2))

    def update(self,hint):
        if hint:
            self.text="Try again"
        else:
            self.text="GO!"
        self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+6, self.rect.y))
        # Blit the rect.
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
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+6, self.rect.y-2))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Create input boxes
top = 48
left = 86
y = 32
# input_box1 = InputBox(100, 100, 32, 32)
# input_box2 = InputBox(100, 200, 32, 32)
# input_boxes = [input_box1, input_box2]
init_board = initialboard()

number_boxes = []
taken_positions = []
for position in init_board:
    pos = position[0]
    taken_positions.append(pos)
    num = position[1]
    number_boxes.append(NumBox(left+pos[0]*(y+1),top+pos[1]*(y+1),y,y,board_coordinates=(pos[0],pos[1]),value=num,text=str(num)))
    board[pos[0],pos[1]] = num

input_boxes = []
for i in range(9):
    for j in range(9):
        if (i,j) not in taken_positions:
            input_boxes.append(InputBox(left+i*(y+1),top+j*(y+1),y,y,board_coordinates=(i,j)))
#[InputBox(left+i*y,top+j*y,y,y) for i in range(10) for j in range(10)]
resetbox1 = TextBox(left+170,top+350,130,40,text='Reset')
hintbox1 = TextBox(left,top+350,150,40,text='GO!')


# Run until user asks to quit
Taken = numpy.zeros((9,9),dtype=bool)
running = True 
while running:

    # Did user click window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for box in input_boxes:
            box.handle_event(event)

    for box in input_boxes:
        (coord,number) = box.update()
        board[coord[0],coord[1]] = number
        if isTaken(coord,number):
            Taken[coord[0],coord[1]] = True
        else:
            Taken[coord[0],coord[1]] = False

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

    resetbox1.draw(screen)

    borders(screen)

    pygame.display.flip()

pygame.quit()