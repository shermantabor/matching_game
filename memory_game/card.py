'''
Card class
In charge of:
    (1) identity of each card
    (2) handling clicks on cards
'''
import time, os, turtle
from gameplay import flipped

# DEFINE SOME CONSTANTS FOR ALL CARDS
BACK_IMAGE = os.path.join("images", "card_back.gif")
CARD_WIDTH = 100
CARD_LENGTH = 150

class Card:
    '''
    class Card
    attributes: f_image_file, card_num (unique identifier), b_image_file
    methods: draw, on_click, eq, conceal
    '''
    # store total matches and guesses, which will be incremented by game_loop()
    matches = 0
    guesses = 0
    game_status = True

    def __init__(self, f_image_file, card_num,
                 game_check, b_image_file=BACK_IMAGE):
        self.f_image_file = os.path.join("images", f_image_file)
        self.b_image_file = b_image_file
        self.card_num = card_num
        self.game_check = game_check

        # make a turtle for each Card object
        self.t = turtle.Turtle()

    def draw(self, x_coord, y_coord):
        '''use Turtle to draw card on gameboard'''

        self.t.penup()
        self.t.teleport(x_coord, y_coord)
        self.t.shape(self.b_image_file)

        # make card dimensions a clickable area
        self.t.shapesize(stretch_wid=CARD_WIDTH, stretch_len=CARD_LENGTH)
        self.t.onclick(self.on_click)

    def on_click(self, x, y):
        '''make turtle reveal its front image when clicked'''

        self.t.shape(self.f_image_file)
        time.sleep(0.5)
        flipped.append(self)
        self.game_check()

    def __eq__(self, other):
        '''check to see if the front image on the card is the same
        but that its not the same card'''

        if (self.f_image_file == other.f_image_file and
                self.card_num != other.card_num):
            return True
        else:
            return False

    def conceal(self):
        '''make turtle 'flip back'
        so front image is hidden again, back image shown'''

        self.t.shape(self.b_image_file)
