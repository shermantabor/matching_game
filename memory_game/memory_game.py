'''
CS5001 Foundations
Fall 2025
Sherman Tabor
Final Project

main() function to execute game
'''
import turtle
from game import Game
from setup import take_init_input, open_screen

def main():
    # build gameplay area
    screen = turtle.Screen()
    open_screen(screen)

    # get user inputs and run game
    user_name, num_cards, config_file = take_init_input()
    game = Game(screen, config_file, user_name)
    game.run()

if __name__ == '__main__':
    main()