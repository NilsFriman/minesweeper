
# Minesweeper
# Functions: difficulty level. colors. safe start. recursive reveals.
# 21-10-23  ~  4 hours

import random
from library import intinput
import time


class Color:
    PINK = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    LIME = '\033[92m'
    YELLOW = '\033[93m'
    BLACK = '\33[30m'
    SALMON = '\33[31m'
    GREEN = '\33[32m'
    GOLD = '\33[33m'
    PURPLE = '\33[35m'
    GREY = '\33[37m'
    RED = '\033[91m'
    BOX = '\33[51m'
    BOLD = '\033[1m'
    ITALIC = '\33[3m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# Generate board with mines
def generateboard(difficulty):
    if difficulty == 1:
        size = 5
        mines = 5
    elif difficulty == 2:
        size = 10
        mines = 20
    elif difficulty == 3:
        size = 15
        mines = 45
    elif difficulty == 4:
        size = 25
        mines = 125
    else:  # Makes sure that a difficulty is chosen
        return False
    genboard = []  # Empty variable
    for i in range(size):
        sublist = []
        for u in range(size):
            sublist.append(-1)  # -1 = unknown grass spots
        genboard.append(sublist)
    while mines > 0:  # While is better than for
        r1 = random.randint(0, size - 1)
        r2 = random.randint(0, size - 1)
        if genboard[r1][r2] != -2:
            genboard[r1][r2] = -2
            mines -= 1
    return genboard


def printboard(proard, secret):
    remcell = 0  # Remaining cells
    count1 = len(proard)  # How many rows there is
    for sublist in proard:
        yaxis = Color.UNDERLINE + Color.GREY + str(count1) + Color.END + "\t|  "  # Prints 1, 2, 3 and so on
        count1 -= 1
        for value in sublist:
            if secret:
                if value > -1:  # Known grass
                    if value == 0:
                        yaxis += "   "
                    else:
                        yaxis += Color.BLUE + str(value) + Color.END + "  "
                elif value != -3:  # ?
                    yaxis += Color.ITALIC + "?  " + Color.END
                    remcell += 1
                else:  # Known mine
                    yaxis += Color.RED + Color.BOLD + "X  " + Color.END
            else:
                if value == -1:  # Unknown grass
                    yaxis += Color.GREEN + "_  " + Color.END
                elif value == -2:  # Unknown mine
                    yaxis += Color.YELLOW + "*  " + Color.END
                elif value == -3:  # Known mine
                    yaxis += Color.RED + Color.BOLD + "X  " + Color.END
                else:  # Known grass
                    if value == 0:
                        yaxis += "   "
                    else:
                        yaxis += Color.BLUE + str(value) + Color.END + "  "
        print(yaxis)
    xaxis = Color.UNDERLINE + Color.GREY + "0" + Color.END + "\t|  " + Color.UNDERLINE + Color.GREY + "1" \
        + Color.END + "  "
    for s in range(len(proard)-1):
        space = ""
        for j in range(3-(len(str(abs(s+2))))):
            space += " "
        xaxis += Color.UNDERLINE + Color.GREY + str(s+2) + Color.END + space
    print(xaxis)
    global total
    if total == remcell:
        total = 0


def neighbors(noard, yc, xc):
    size = len(noard)
    if noard[yc][xc] < 0:
        neival = 0
        for t in range(yc-1, yc+2):
            for g in range(xc-1, xc+2):
                if -1 < t < size and -1 < g < size:
                    if noard[t][g] < -1:
                        neival += 1
        noard[yc][xc] = neival
        if neival == 0:
            for m in range(yc-1, yc+2):
                for n in range(xc-1, xc+2):
                    if -1 < m < size and -1 < n < size:
                        neighbors(noard, m, n)


done = False

print("What difficulty level do you want to play at?")
if board := generateboard(diff := intinput("Easy: 1\nMedium: 2\nHard: 3\nImpossible: 4\n")):
    first = True
    total = len(board) ** 2 / 5
    while not done:
        printboard(board, True)
        if first:
            x = intinput("What x coordinate would you like to pick?\n") - 1
            y = len(board) - intinput("What y coordinate would you like to pick?\n")
            try:
                safe = False
                while board[y][x] != 0:
                    board = generateboard(diff)
                    if board[y][x] == -1:  # Unknown grass
                        neighbors(board, y, x)
                first = False
            except IndexError:
                print("That coordinate doesn't exist!")
                time.sleep(0.8)
        else:
            if total != 0:
                x = intinput("What x coordinate would you like to pick?\n") - 1
                y = len(board) - intinput("What y coordinate would you like to pick?\n")
                try:
                    if board[y][x] == -1:  # Unknown grass
                        neighbors(board, y, x)
                    elif board[y][x] == -2:
                        board[y][x] = -3
                        print(Color.RED + Color.BOLD + "YOU LOSE! Unlucky.")
                        done = True
                    else:
                        print("You have already tried that coordinate!")
                        time.sleep(0.8)
                except IndexError:
                    print("That coordinate doesn't exist!")
                    time.sleep(0.8)
            else:
                print(Color.GREEN + Color.BOLD + "YOU WIN! Well done.")
                done = True
    print("Thank you for playing! Here was the layout of the minefield:")
    printboard(board, False)
else:
    print("You can only input 1, 2, 3 or 4 as your difficulty level!")


# Improvements to be done: Made in pygame. Implement flag system. Make the required start area larger
