'''
Game class
In charge of:
    (1) drawing gameplay areas
    (2) making and dealing the cards
    (3) storing guesses and matches
    (4) closing out game
'''
import turtle, os, time, random
from QuitButton import QuitButton
from Card import Card
from gameplay import (flipped, game_loop, save_score,
                      leaders_sort, write_score, end_game, config_error)

# define some constants for game area
PLAY_AREA_COORD = [(-440, 360), (200, 360), (200, -200), (-440, -200)]
SCOREBOARD_COORD = [(-440, -250), (200, -250), (200, -350), (-440, -350)]
LEADERBOARD_COORD = [(250, 360), (440, 360), (440, -200), (250, -200)]

# initialize a turtle to write the score
score_t = turtle.Turtle()

class Game:
    '''
    class Game
    attributes: screen, config file, username
    methods: initiate cards, make_card_objects, deal_cards,
            run, game_check, closeout,
            prep_turtle, build_play_area, build_scoreboard,
            fill_scoreboard, build_leaderboard, fill_leaderboard,
            draw
    '''
    # define some variables for play area
    play_area_width = abs(PLAY_AREA_COORD[1][0] - PLAY_AREA_COORD[0][0])
    play_area_height = abs(PLAY_AREA_COORD[2][1] - PLAY_AREA_COORD[1][1])

    # initialize variables to keep track of gameplay
    matches = 0
    guesses = 0

    def __init__(self, screen, config_file, user_name):
        self.screen = screen
        self.config_file = config_file
        self.user_name = user_name
        self.t = turtle.Turtle()
        self.prep_turtle()
        self.quit_button = QuitButton("quitbutton.gif",
                                      280, -280, self.screen, self.closeout)
        self.card_list = self.initiate_cards()
        self.card_count = len(self.card_list)
        self.card_list = self.validate_cards()
        self.draw()
        self.card_objects = self.make_card_objects()
        self.deal_cards()
        self.flipped = []

    # Methods for making, shuffling, and placing the cards
    def initiate_cards(self):
        '''
        function initiate_cards()
        I: str: configuration file
        P:  (1) iterate lines of config file (each line is a card image)
            (2) create a list of "cards"
            (each element is a face image for a card)
            (3) duplicate each "card" so that there is a match in the game
        O: list of card face images
        '''

        try:
            file_path = os.path.join("config", self.config_file)
            with open(file_path, mode="r", encoding="utf-8") as infile:
                card_list = infile.read().splitlines()
            card_list = card_list * 2
            random.shuffle(card_list)
            return card_list
        except FileNotFoundError:
            config_error()
            self.closeout()

    def validate_cards(self):
        '''check that an image file exists for each card'''
        for each in self.card_list:
            if not os.path.exists(os.path.join("images", each)):
                self.config_file = f"card_config_{self.card_count}.txt"
                self.card_list = self.initiate_cards()
                config_error()

        return self.card_list

    def make_card_objects(self):
        '''
        function make_card_objects
        I: card list (shuffled, with 2 of each card. 8, 10, or 12 total)
        0: a list of lists of card objects
        '''
        # set up our grid structure
        rows = -(len(self.card_list) // -4)
        columns = 4

        card_objects = []
        card_num = 0
        for i in range(rows):
            row = []
            for j in range(columns):
                if ((columns * i) + (j + 1)) <= len(self.card_list):
                    card_1 = Card(self.card_list[((columns * i) + j)],
                                  card_num, self.game_check)
                    row.append(card_1)
                    card_num += 1
            card_objects.append(row)
        return card_objects

    def deal_cards(self):
        ''' function deal_cards
        I: list of cards to be dealt
        P: place each card on the board
        O: none
        '''
        # set starting position to deal first card
        x = -370
        y = 270

        # loop through list of lists to assign coords and place cards
        for row in range(len(self.card_objects)):
            for column in range(len(self.card_objects[row])):
                self.card_objects[row][column].draw(x, y)
                x = x + (Game.play_area_width / 4)
            x = -370
            y = y - (Game.play_area_height / 3)

    # Methods for running the game and closing it out
    def run(self):
        turtle.mainloop()

    def game_check(self):
        '''
        function game_check
        I: None
        P:  (1) run game loop function from gameplay
            (2) update scoreboard
            (3) decide whether to end game
        '''
        # run game loop to determine what happens next
        inc_matches, inc_guesses = game_loop(flipped)
        Game.matches += inc_matches
        Game.guesses += inc_guesses

        # update scoreboard
        if inc_guesses != 0:
            self.fill_scoreboard()

        # end game if all cards have been matched
        if Game.matches * 2 == self.card_count:
            leaders = save_score(self.user_name,
                                 Game.guesses, self.config_file)
            leaders = leaders_sort(leaders)
            write_score(leaders, self.config_file)
            end_game()
            self.closeout()

    def closeout(self):
        '''final closeout if quit or win'''

        # NOTE! bye() seems to be causing Python to crash
        # I have been unable to find a solution to this error :(
        time.sleep(1)
        self.screen.ontimer(self.screen.bye, 10)

    # Methods for drawing and filling the designated areas of the gameboard
    def prep_turtle(self):
        self.t.hideturtle()
        self.t.penup()

    def build_play_area(self):
        '''draw play area'''

        self.t.goto(PLAY_AREA_COORD[0])
        self.t.pendown()
        for i in range(len(PLAY_AREA_COORD)):
            self.t.goto(PLAY_AREA_COORD[i])
        self.t.goto(PLAY_AREA_COORD[0])
        self.t.penup()

    def build_scoreboard(self):
        '''draw scoreboard'''

        self.t.goto(SCOREBOARD_COORD[0])
        self.t.pendown()
        for i in range(len(SCOREBOARD_COORD)):
            self.t.goto(SCOREBOARD_COORD[i])
        self.t.goto(SCOREBOARD_COORD[0])
        self.t.penup()

    def fill_scoreboard(self):
        '''update the scoreboard with guesses and matches'''

        score_t.clear()
        score_t.hideturtle()
        score_t.teleport(-440, -300)
        score_t.write(f"  Status: {Game.guesses} guesses, "
                      f"{Game.matches} / {int(self.card_count / 2)} matches",
                           align="left", font=("Arial", 24, "normal"))

    def build_leaderboard(self):
        '''draw box for leaderboard'''

        self.t.goto(LEADERBOARD_COORD[0])
        self.t.pensize(5)
        self.t.color("blue")
        self.t.pendown()
        for i in range(len(LEADERBOARD_COORD)):
            self.t.goto(LEADERBOARD_COORD[i])
        self.t.goto(LEADERBOARD_COORD[0])

        # write 'LEADERS' at the top of the box
        self.t.penup()
        self.t.forward(10)
        self.t.setheading(270)
        self.t.forward(70)
        self.t.write("Leaders:", align="left", font=("Arial", 24, "bold"))

    def fill_leaderboard(self):
        '''write leaders from file if file exists'''

        # leaderboard files are named based on the config file
        leaderboard_file = self.config_file.strip(".txt") + "_leaderboard.txt"
        self.t.color("black")
        self.t.goto(LEADERBOARD_COORD[0])
        self.t.setheading(0)
        self.t.forward(10)
        self.t.setheading(270)
        self.t.forward(140)

        # if leader file already exists for config, write leaders
        try:
            with open(os.path.join("leaderboards", leaderboard_file),
                      mode="r", encoding="utf-8") as infile:
                max_items = 8
                items = 1
                for line in infile:
                    if items <= max_items:
                        self.t.write(line, align="left",
                                     font=("Arial", 18, "normal"))
                        self.t.forward(40)
                        items += 1

        except FileNotFoundError:
            self.t.write("No leaders yet...", font=("Arial", 18, "italic"))

    def draw(self):
        '''combine drawing functions to call easily at once'''
        self.t.speed("normal")
        self.t.pensize(7)
        self.t.color("black")
        self.build_play_area()
        self.build_scoreboard()
        self.build_leaderboard()
        self.fill_leaderboard()
        self.fill_scoreboard()
        self.quit_button.draw()