'''
Quit Button class
'''
import turtle
import os

class QuitButton:
    '''
    Class QuitButton
    attributes: image, x-coord, y-coord, screen, end_game (function!)
    methods: draw, on_click
    '''

    def __init__(self, image, x_coord, y_coord, screen,
                 end_game=None, height=40, width=60):
        self.image = os.path.join("images", image)
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.screen = screen
        self.height = height
        self.width = width
        self.t = turtle.Turtle()
        self.state = False
        self.end_game = end_game

    def draw(self):
        '''draw quit button on gameboard'''

        self.t.penup()
        self.t.teleport(self.x_coord, self.y_coord)
        self.t.shape(self.image)

        # make button dimensions a clickable area
        self.t.shapesize(stretch_wid = self.width, stretch_len = self.height)
        self.t.onclick(self.on_click)

    def on_click(self, x, y):
        quit = str(turtle.textinput("Are you sure?",
                                    "'y' to quit, else to continue"))
        quit = quit.lower()
        if len(quit) > 0 and quit[0] == "y":
            turtle.teleport(0, 0)
            turtle.showturtle()
            turtle.shape(os.path.join("images", "quitmsg.gif"))
            self.end_game()
