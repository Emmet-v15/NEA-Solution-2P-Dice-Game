# Import the login system that i have created for the NEA
import login

# Import the tools to save and load profiles and to get the highscores
import filetools

# Import the text file which i use to color my text (also made for the NEA)
import text

# Import the Dice class form dice that has a roll function which returns a random number
# between 1 and 6
from dice import Dice

def pause():
    input("Press Enter to continue")

def getWinner(users):
    """
    get the winner and looser from comparing scores
    """

    winner = None
    loser = None
    if users[0].points > users[1].points:
        winner = users[0]
        loser = users[1]

    elif users[0].points < users[1].points:
        winner = users[1]
        loser = users[0]

    return winner, loser

def calculateScore(roll):
    """
    Divide the number by 2 and check for remainder to see if number is even or odd
    then calculate the points
    """

    if (roll % 2) == 0:
        even = text.green("True")
        points = 10
    else:
        even = text.red("False")
        points = -5

    return points, even

def main():
    users = login.getUsers() # get 2 user objects and save them in an array
    dice = Dice() # initialise a dice

    for roundNum in range(1, 6):
        for user in range(0, 2):
            
            # calculate the rolls and score
            dice1 = dice.roll()
            dice2 = dice.roll()
            dice3 = None
            total = dice1 + dice2
            
            # if they both are the same, calculate another roll and add it to the total
            if dice1 ==  dice2:
                dice3 = dice.roll()
                total += dice3

            # get the calculated points and if the total is even from our function
            points, even = calculateScore(total)
            
            # make sure the points don't go below 0
            if users[user].points + points < 0:
                points = 0
            
            users[user].addPoints(points)
            
            print("\n\n\n")
            print(text.blue("===[Round #" + str(roundNum) + "]==="))
            print("User:", text.orange(users[user].username))
            print("Dice 1 Roll:", dice1)
            print("Dice 2 Roll:", dice2)
            if dice3 != None:
                print(text.green("Dice 3 Roll (EXTRA): " + str(dice3)))
            print("Total Roll:", total)
            print("Even:", even)
            print("Points:", points)
            print("Total Score for " + str(users[user].username) + ":", users[user].points)
            print(text.blue("================"))
            pause()
    
    # check if there is a winner
    winner, loser = getWinner(users)
    
    # do a tiebreaker until a winner is found
    while winner == None:
        print(text.orange("======TIEBREAKER======"))
        for user in users:
            # roll a dice
            total = dice.roll()
            
            # get the calculated points and if the total is even from our function
            points, even = calculateScore(total)

            print(user.username + "'s Roll:", total)
            print("Even:", even)
            print("Points:", points)

            # add points to the user
            user.addPoints(points)

            # wait for user input
            pause()

        # check if it's a tie
        winner, loser = getWinner(users)


    # output a winner
    print(text.orange("Game Over"))
    print(text.green("Winner: " + winner.username + "  [SCORE " + str(winner.points) + "]"))
    print(text.red("Loser: " + loser.username + "  [SCORE " + str(loser.points) + "]"))
    
    # save their score in an external file if it is a highscore
    winner.save()

    pause()

    # display the leaderboard

    print(text.green("===Leaderboard==="))
    highscores = filetools.getHighscores()
    

    for i in range(5):
        # make sure we aren't exceeding the length of the array
        if i < len(highscores):
            # loop through all the five highscores and print them
            print(str(i+1) + ".", highscores[i]['username'], "  [SCORE " + str(highscores[i]['score']) + "]")
        else:
            # if there aren't 5 accounts, print the rest as NONE
            print(str(i+1) + ". None")

    print(text.green("Thanks for playing!"))
    # wait for user to end the game.
    pause()

main()