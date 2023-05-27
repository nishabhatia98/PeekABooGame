import random
import sys
import os
import time
import string
import threading

class PeekABooGrid:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid, self.pairs = self.createInitialGrid()
        self.num_pairs = grid_size * grid_size // 2
        self.found_pairs = 0
        self.total_guesses = 0
        self.revealed_elements = 0


    def createInitialGrid(self):
        grid = [] # empty list to hold the rows
        # list of pairs of integers
        pairs = list(range(self.grid_size * self.grid_size // 2)) * 2
        random.shuffle(pairs) # shuffle the pairs
        for _ in range(self.grid_size):
            row = ['X']*self.grid_size
            grid.append(row)
        return grid, pairs

    def printGrid(self):
        size = len(self.grid)
    # create the column header
        print("  ", end="  ")
        for col in range(size):
            print(f"[{chr(ord('A') + col)}]", end=" ")
        print()
    # print the row number and the row
        for row in range(size):
            print(f"[{row+1}]  ", end="")
            for col in range(size):
                print(f"{self.grid[row][col]} ", end="  ")
            print()

    def selectPair(self):
        size = len(self.grid)
        while True:
            try:
                cell = input("Enter the cell coordinates: ")
                row, col = self.parseCell(cell)
                # if not (0 <= row < size and 0 <= col < size):
                #     print("Invalid cell. Please try again.")
                #     continue
                if not (0 <= col < size):
                    print("Input Error: column entry is out of range. Please try again.")
                    continue
                if not (0 <= row < size ):
                    print("Input Error: row entry is out of range. Please try again.")
                    continue
                if self.grid[row][col] != 'X':
                    print("Cell already revealed. Please try again.")
                    continue

                return row, col
            except ValueError:
                print("Invalid cell format. Please enter cells in the format 'A1', 'B2', etc.")

    def parseCell(self, cell):
        col = ord(cell[0].upper()) - ord('A')
        row = int(cell[1:]) - 1
        return row, col

    def revealGrid(self):
        size = len(self.grid)
        for i in range(size):
            for j in range(size):
                if self.grid[i][j] == 'X':
                    self.grid[i][j] = str(self.pairs[i * self.grid_size + j]) 

    def determineScore(self):
        minimum_possible_guesses = (self.grid_size * self.grid_size) // 2
        score = (minimum_possible_guesses / self.total_guesses) * 100
        return score

    def uncoverOneElement(self):
        size = len(self.grid)
        while True:
            try:
                cell = input("Enter the cell coordinates: ")
                row, col = self.parseCell(cell)
                if not (0 <= col < size):
                    print("Input Error: column entry is out of range. Please try again.")
                    continue
                if not (0 <= row < size ):
                    print("Input Error: row entry is out of range. Please try again.")
                    continue

                if self.grid[row][col] != 'X':
                    print("Cell already revealed. Please try again.")
                    continue

                self.grid[row][col] = str(self.pairs[row * self.grid_size + col])
                self.revealed_elements += 1
                os.system('cls')
                self.printGrid()
                return
            except ValueError:
                print("Invalid cell format. Please enter cells in the format 'A1', 'B2', etc.")

    def display_menu(self):
        print("1. Let me select 2 elements")
        print("2. Uncover one element for me")
        print("3. I gave up  - reveal all elements")
        print("4. New Game")
        print("5. Exit")

    def get_user_choice(self):
        while True:
            choice = input("Select: ")
            if choice.isdigit() and 1 <= int(choice) <= 5:
                return int(choice)
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

    def start(self):
        print("------------------------")
        print("|       PEEK-A-BOO     |")
        print("------------------------")
        self.printGrid()

        # revealed_elements = 0
        while True:
            self.display_menu()
            user_choice = self.get_user_choice()

            if user_choice == 1:
                print("Option 1 selected")
                # Perform the action for option 1
                row1, col1 = self.selectPair()
                row2, col2 = self.selectPair()
                self.total_guesses += 1

                if self.pairs[row1 * self.grid_size + col1] == self.pairs[row2 * self.grid_size + col2]:
                    self.found_pairs += 1
                    self.grid[row1][col1] = str(self.pairs[row1 * self.grid_size + col1])
                    self.grid[row2][col2] = str(self.pairs[row2 * self.grid_size + col2])
                    os.system('cls')
                    print("Correct pair!")  
                    self.printGrid()  
                else:
                    print("Incorrect pair!")
                    self.grid[row1][col1] = str(self.pairs[row1 * self.grid_size + col1])
                    self.grid[row2][col2] = str(self.pairs[row2 * self.grid_size + col2])
                    os.system('cls')
                    self.printGrid()
                    time.sleep(4)
                    self.grid[row1][col1] = 'X'
                    self.grid[row2][col2] = 'X'
                    os.system('cls')
                    self.printGrid()
                    print("Try Again!")

                # check if the game is over or if all the pairs are revealed or not
                if self.found_pairs == self.num_pairs:
                    score = self.determineScore()
                    os.system('cls')
                    if score == 100:
                        print("Oh Happy Day. You won!")
                        print("Your Score is: {:.2f}".format(score))
                    else:
                        print("Oh You revelead all the numbers -- Peek - A - Boo!")
                        print("Your Score is: {:.2f}".format(score))
                    break

            elif user_choice == 2:
                self.uncoverOneElement()
                self.total_guesses += 1
                    # if self.found_pairs == self.num_pairs:
                    #     score = self.determineScore()
                    #     print("Oh Happy Day. You won!")
                    #     print("Score: {:.2f}".format(score))
                    #     break
                if self.revealed_elements == self.grid_size * self.grid_size:
                    os.system('cls')
                    print("You cheated - Loser! Your score is 0.00")
                    break

            elif user_choice == 3:
                self.revealGrid()
                self.printGrid()

            elif user_choice == 4:
                # New Game - Reset the grid
                self.__init__(self.grid_size)
                os.system('cls')
                self.printGrid()

            elif user_choice == 5:
                # Exit
                break
            else:
                print("Invalid input. Please try again.")
            
            if self.revealed_elements == self.grid_size * self.grid_size:
                score = self.determineScore()
                print("Congratulations! You revealed all elements.")
                print("Score: {:.2f}".format(score))
                break
        
        if self.revealed_elements == self.grid_size * self.grid_size:
         print("Game Over!")

grid_size = int(input('Enter the size of the grid: '))
if grid_size not in [2, 4, 6]:
    print("Invalid grid size. Grid size must be 2, 4, or 6.")
    sys.exit(1)

game = PeekABooGrid(grid_size)
game.start()
