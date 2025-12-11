'''
helper functions to execute gameplay for the Game object
In charge of:
    (1) assessing how to respond to each guess
    (2) saving and writing the user's score at the end of the game
    (3) displaying configuration error messages
'''
import turtle, os, time

# initialize a list to keep track of which cards are flipped over
flipped = []

# function to assess how to respond to each guess
# essentially outsourcing some logic from the Game class
def game_loop(flipped) -> tuple[int,int]:
    '''
    function game_loop
    I: flipped: list of card objects
    P: increment guesses and matches based on whether the cards are a match
    O: increment for guesses and matches
    '''

    guesses = 0
    matches = 0

    # check to see if two cards are flipped
    if len(flipped) == 2:
        # if they match, hide the cards and increment matches
        if flipped[0] == flipped[1]:
            flipped[0].t.hideturtle()
            flipped[1].t.hideturtle()
            matches += 1
        else:
            flipped[0].conceal()
            flipped[1].conceal()
        # empty flipped, increment guesses
        flipped.clear()
        guesses += 1

    return matches, guesses

# functions to save user's score
def save_score(user_name, guesses, config_file) -> list:
    '''add current user to list of leaders'''

    leaderboard_file = config_file.strip(".txt") + "_leaderboard.txt"
    leaders = []
    # load prior leaders if there are any
    try:
        with open(os.path.join("leaderboards", leaderboard_file),
                  mode="r", encoding="utf-8") as infile:
            for line in infile:
                if line != "\n":
                    leaders.append(line.strip("\n"))
            leaders.append(str(guesses) + ": " + user_name)
            return leaders

    # handle no prior leaders and add current user to empty list of leaders
    except FileNotFoundError:
        print("leaderboard file not found")
        leaders.append(str(guesses) + ": " + user_name)
        return leaders

def leaders_sort(lst) -> list:
    '''sort leaders list by score, in ascending order'''

    lst_of_lst = []
    for i in range(len(lst)):
        score = int(lst[i].split(":")[0])
        lst_of_lst.append([score, lst[i]])
    lst_of_lst.sort()

    leaders = []
    for each in lst_of_lst:
        leaders.append(each[1])
    return leaders

def write_score(leaders, config_file):
    '''write updated list of leaders to leaderboard file'''

    leaderboard_file = config_file.strip(".txt") + "_leaderboard.txt"

    with open(os.path.join("leaderboards", leaderboard_file), mode="w",
              encoding="utf-8") as outfile:
        for i in range(len(leaders)):
            outfile.write(leaders[i] + "\n")

#  functions to display messages to user
def config_error():
    '''display error message if config file cannot be found'''
    t = turtle.Turtle()
    t.teleport(0, 50)
    t.shape(os.path.join("images", "file_error.gif"))
    print('error')
    time.sleep(1)
    t.hideturtle()

def end_game():
    '''display winner image'''

    t = turtle.Turtle()
    t.teleport(0, 50)
    t.shape(os.path.join("images", "winner.gif"))