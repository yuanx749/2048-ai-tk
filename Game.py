from Grid import Grid
from PlayerAI import PlayerAI
import tkinter

ACTION = dict(zip(range(4), ('UP', 'DOWN', 'LEFT', 'RIGHT')))

TILE_SIZE = 100
BORDER_SIZE = 45
TILE_COLOR = {0:'#CDC5BF', 2:'#EEE4DA', 4:'#EDE0C8', 8:'#F2B179', 
              16:'#F59563', 32:'#F67C60', 64:'#F65E3B', 128:'#EDCF72', 
              256:'#EDCC62', 512:'#EDC851', 1024:'#EDC746', 2048:'#EDC22E', 
              4096:'#000000', 8192:'#FFFFFF'}
TEXT_COLOR = {0:'#CDC5BF', 2:'#776E65', 4:'#776E65', 8:'#F9F6F2', 
              16:'#F9F6F2', 32:'#F9F6F2', 64:'#F9F6F2', 128:'#F9F6F2', 
              256:'#F9F6F2', 512:'#F9F6F2', 1024:'#F9F6F2', 2048:'#F9F6F2', 
              4096:'#FFFFFF', 8192:'#000000'}

class Game:
    def __init__(self):
        self.height = 4
        self.width = 4
        self.time_limit = 0.1
        self.grid = Grid(height=self.height, width=self.width)
        self.over = True

        self.root = tkinter.Tk()
        self.root.title('2048')
        self.canvas = tkinter.Canvas(self.root, 
                                     width=self.width*TILE_SIZE + 2*BORDER_SIZE, 
                                     height=self.height*TILE_SIZE + 2*BORDER_SIZE, 
                                     bg='#A39480')
        self.frame = tkinter.Frame(self.root)
        self.button = tkinter.Button(self.frame, text='New Game', command=self.reset)
        self.label1 = tkinter.Label(self.frame, text='Rows:')
        self.label2 = tkinter.Label(self.frame, text='Columns:')
        self.label3 = tkinter.Label(self.frame, text='Time limit:')
        self.entry1 = tkinter.Entry(self.frame)
        self.entry1.insert(0, str(self.height))
        self.entry2 = tkinter.Entry(self.frame)
        self.entry2.insert(0, str(self.width))
        self.entry3 = tkinter.Entry(self.frame)
        self.entry3.insert(0, str(self.time_limit))

        self.frame.grid(row=0, column=0)
        self.button.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.label1.grid(row=1, column=0, padx=5)
        self.label2.grid(row=2, column=0)
        self.label3.grid(row=3, column=0)
        self.entry1.grid(row=1, column=1, padx=5)
        self.entry2.grid(row=2, column=1)
        self.entry3.grid(row=3, column=1)
        self.canvas.grid(row=0, column=1)

        self.draw()
        self.start()
        self.root.mainloop()

    def reset(self):
        self.height = int(self.entry1.get())
        self.width = int(self.entry2.get())
        self.time_limit = float(self.entry3.get())
        self.grid = Grid(height=self.height, width=self.width)
        self.play_ai = PlayerAI(time_limit=self.time_limit)
        self.over = False

        self.canvas.config(width=self.width*TILE_SIZE + 2*BORDER_SIZE, 
                           height=self.height*TILE_SIZE + 2*BORDER_SIZE)

        for i in range(2):
            self.grid.insert_random_tile()
        print("New game:")
        print(self.grid)
        self.draw()

    def draw(self):
        self.canvas.delete(tkinter.ALL)
        for row in range(self.height):
            for col in range(self.width):               
                tile_value = self.grid.get_tile(row, col)
                self.canvas.create_rectangle(col*TILE_SIZE + BORDER_SIZE, 
                                             row*TILE_SIZE + BORDER_SIZE, 
                                             (col+1)*TILE_SIZE + BORDER_SIZE, 
                                             (row+1)*TILE_SIZE + BORDER_SIZE, 
                                             width=TILE_SIZE // 10, 
                                             outline='#A39480', 
                                             fill=TILE_COLOR[tile_value])
                self.canvas.create_text((col+0.5)*TILE_SIZE + BORDER_SIZE,
                                        (row+0.5)*TILE_SIZE + BORDER_SIZE,
                                        text=str(tile_value),
                                        fill=TEXT_COLOR[tile_value],
                                        font=('Microsoft Sans Serif', -TILE_SIZE // 3, 'bold'))

    def start(self):
        if not self.over:
            grid_copy = self.grid.clone()
            print("Player's turn:")
            move = self.play_ai.get_move(grid_copy)
            if move != None and move >= 0 and move < 4:
                if self.grid.can_move([move]):
                    print(ACTION[move])
                    self.grid.move(move)
                else:
                    print("Invalid player AI move!")
                    self.over = True
            else:
                print("Invalid player AI move!!")
                self.over = True
            if not self.over:
                print(self.grid)
                self.draw()
                print("Computer's turn:")
                self.grid.insert_random_tile()
                print(self.grid)
                self.draw()
            if not self.grid.can_move():
                self.over = True
                print("Game over:", self.grid.get_max_tile(), '\n')
        self.root.after(10, self.start)

if __name__ == '__main__':
    game = Game()
