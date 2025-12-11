'''
CS5001 Foundations
Fall 2025
Sherman Tabor

Set-up functions to get user input, which will be used to construct our game object
'''
import os, time, turtle

# define constants for board dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# functions to prep gameplay area
def register_shapes(screen, directory_name):
    '''
    function register_shapes
    I: directory path to images for game
    P: iterate through all images; register each on our screen
    O: none
    '''

    images = []
    for each in os.listdir(directory_name):
        each_path = os.path.join(directory_name, each)
        if os.path.isfile(each_path) and each_path.endswith(".gif"):
            images.append(each_path)

    for each in images: # register each image
        screen.register_shape(str(each))

def open_screen(screen):
    turtle.penup()
    turtle.hideturtle()
    screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
    screen.bgcolor("white")
    register_shapes(screen, directory_name="images")

# functions to gather user input
def get_name() -> str:
    '''
        function get_name()
        I: none
        P: take user input; greet user
        O: user_name
    '''
    user_name = turtle.textinput("Your name (max 15 char): ",
                                 "Your name: ")
    # handle no input
    if user_name == "":
        user_name = "stealth player"

    # handle username too long
    user_name = user_name[:14].lower()
    # write a message to greet user
    turtle.color("green")
    turtle.teleport(0, 370)
    turtle.hideturtle()
    turtle.write(f"Good luck, {user_name}!",
                 align="center", font=("Arial", 20, "bold"))
    return user_name

def get_num_cards() -> int:
    '''
    function get_num_cards()
    I: none
    P: take user input to set number of cards (8, 10, or 12)
    O: int: number of cards
    '''
    valid_choices = (8, 10, 12)
    t = turtle.Turtle()
    t.hideturtle()
    t.color("black")
    num_cards = turtle.textinput("Number of cards to play (8, 10, or 12): ",
                                 "Input number (default 8): ")

    # handle blank or non-int inputs
    try:
        num_cards = int(round(float(num_cards), 0))
    except ValueError:
        if len(num_cards) >= 1:
            t.shape(os.path.join("images", "invalid_input.gif"))
            time.sleep(1)
            t.hideturtle()
        num_cards = 8

    # handle int inputs that are not 8, 10, or 12
    if num_cards not in valid_choices:
        t.shape(os.path.join("images", "invalid_input.gif"))
        time.sleep(1)
        t.hideturtle()
        num_cards = clamped(num_cards)
    return num_cards

def clamped(num_cards: int) -> int:
    '''
    I: number of cards, integer but not 8, 10, or 12
    O: closest int 8, 10, or 12
    '''

    if num_cards < 8:
        num_cards = 8
    elif num_cards == 9:
        num_cards = 8
    elif num_cards == 11:
        num_cards = 10
    elif num_cards > 12:
        num_cards = 12
    return num_cards

def get_config_file(num_cards: int) -> str:
    '''
    function get_config_file
    I: number of cards
    P: ask user for a config selection
    O: configuration file
    '''

    # get user input
    config = turtle.textinput("Enter a config file: (default: card)",
                              "Options: card, winston, hp, custom")
    config_file = f"{config}_config_{num_cards}.txt"

    # default to card config if input does not match existing config file
    if not os.path.exists(os.path.join("config", config_file)):
        if len(config) >= 1:
            t = turtle.Turtle()
            t.shape(os.path.join("images", "file_error.gif"))
            time.sleep(1)
            t.hideturtle()
        config_file = f"card_config_{num_cards}.txt"
    return config_file

def take_init_input():
    '''combine user input functions to call easily at once'''
    user_name = get_name()
    num_cards = get_num_cards()
    config_file = get_config_file(num_cards)
    return user_name, num_cards, config_file