import os 
from grid import PeekABooGrid
import sys


def start_game(args):
    grid_size = int(args[0])
    if grid_size not in [2, 4, 6]:
        print("Invalid grid size. Grid size must be 2, 4, or 6.")
        sys.exit(1)

    game = PeekABooGrid(grid_size)
    os.system('clear')
    print("--" * 10)
    print("|   PEEK - A BOO    |")
    print("--" * 10)
    game.printGrid()
    while True:
        game.display_menu()
        user_choice = game.get_user_choice()

        if user_choice == 1:
            isWin , score = game.option1()

            if isWin:
                os.system('clear')
                print("Oh Happy Day. You won!")
                print("Your Score is: {:.2f}".format(score))
                break

        elif user_choice == 2:
            isWin , isCheated , score = game.uncoverOneElement()

            if isWin:
                if isCheated: 
                    print("You cheated!! Your score is 0.")
                    break
                else: 
                    print("Oh Happy Day. You won!")
                    print("Your Score is: {:.2f}".format(score))

        elif user_choice == 3:
            game.revealGrid()
            game.printGrid()

        elif user_choice == 4:
            game.__init__(game.grid_size)
            os.system('clear')
            game.printGrid()
        elif user_choice == 5:
            break
        else:
            print("Invalid input. Please try again.")

        if game.revealed_elements == game.grid_size * game.grid_size:
            score = game.determineScore()
            print("Congratulations! You revealed all elements.")
            print("Score: {:.2f}".format(score))
            break

    # if game.revealed_elements == game.grid_size * game.grid_size:
    #     print("Game Over!")

if __name__ == '__main__':  
    args = sys.argv[1:]
    start_game(args)