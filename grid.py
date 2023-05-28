import random
import sys  # for sys.exit()
import os
import time

random.seed(0)

class PeekABooGrid:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid, self.pairs = self.createInitialGrid()
        self.num_pairs = grid_size * grid_size // 2
        self.uncovered_coordinates = set()
        self.found_pairs = 0
        self.total_guesses = 0
        self.revealed_elements = 0

    def createInitialGrid(self):
        grid = [] # empty list to hold the rows
        pairs = list(range(self.grid_size * self.grid_size // 2)) * 2
        random.shuffle(pairs)
        for _ in range(self.grid_size):
            row = ['X'] * self.grid_size
            grid.append(row)
        return grid, pairs
    
    def check_winning_condition(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 'X':
                    return False
        return True

    def option1(self):
        row1, col1 = self.selectPair()
        row2, col2 = self.selectPair()

        if self.pairs[row1 * self.grid_size + col1] == self.pairs[row2 * self.grid_size + col2]:
            self.found_pairs += 1
            self.grid[row1][col1] = str(self.pairs[row1 * self.grid_size + col1])
            self.grid[row2][col2] = str(self.pairs[row2 * self.grid_size + col2])
            # os.system('cls')
            print("Correct pair!")
            self.printGrid()
        else:
            print("Incorrect pair!")
            self.grid[row1][col1] = str(self.pairs[row1 * self.grid_size + col1])
            self.grid[row2][col2] = str(self.pairs[row2 * self.grid_size + col2])
            # os.system('cls')
            self.printGrid()
            time.sleep(2)
            self.grid[row1][col1] = 'X'
            self.grid[row2][col2] = 'X'
            os.system('cls')
            self.printGrid()
            print("Try Again!")

        self.total_guesses += 1

        return self.check_winning_condition() , self.determineScore()


        # if self.found_pairs == self.num_pairs:
        #     score = self.determineScore()
        #     os.system('cls')
        #     if score == 100:
        #         print("Oh Happy Day. You won!")
        #         print("Your Score is: {:.2f}".format(score))
        #     else:
        #         print("Oh You revealed all the numbers -- Peek - A - Boo!")
        #         print("Your Score is: {:.2f}".format(score))


    def printGrid(self):
        size = len(self.grid)
        print("  ", end="  ")
        for col in range(size):
            print(f"[{chr(ord('A') + col)}]", end=" ")
        print()
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
        return round(score , 2)

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
                self.total_guesses += 2
                os.system('cls')
                self.printGrid()

                self.uncovered_coordinates.add(cell.upper())

                isWin = self.check_winning_condition()
                isCheated = len(self.uncovered_coordinates) == self.grid_size * self.grid_size

                return isWin , isCheated , self.determineScore()

            except ValueError:
                print("Invalid cell format. Please enter cells in the format 'A1', 'B2', etc.")
                
    def display_menu(self):
        print("1. Let me select 2 elements")
        print("2. Uncover one element for me")
        print("3. I gave up - reveal all elements")
        print("4. New Game")
        print("5. Exit")

    def get_user_choice(self):
        while True:
            choice = input("Select: ")
            if choice.isdigit() and 1 <= int(choice) <= 5:
                return int(choice)
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

