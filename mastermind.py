import time
import sys
import random

# bron: https://repl.it/@FGratt/Mastermind


# support variables:
colors = ["yellow", "blue", "orange", "green", "red", "white"]  # list of possible colors of "secret_code"
possible_inputs = ["yellow", "y", "blue", "b", "orange", "o", "green", "g", "red", "r", "white", "w"]
# used to check the input of the player. These are all the possible inputs.
guesses = []  # store the history of the input
pegs = []  # store the output (black pegs - white pegs)
user_input = []  # temporary user input. Used to check if inputs are in "possible_inputs" and then stored in "guesses"
secret_code = []
turn = 0


def welcome():
	print("Starting Game.........")
	time.sleep(1)
	print("\n======================================================================================")
	print('''The colors used in the game will be: Yellow, Blue, Orange, Green, Red and White.\
    \nIf you guess the right color at the right spot, the black pin goes up by 1.\
    \nAnd if you guess the right color but at the wrong spot, the white pin goes up by 1.
    '''   
    )





# function that generates the code to guess
def generate_secret_code():
	global secret_code
	a = colors[random.randrange(0, len(colors))]
	b = colors[random.randrange(0, len(colors))]
	c = colors[random.randrange(0, len(colors))]
	d = colors[random.randrange(0, len(colors))]
	secret_code = [a, b, c, d]
	#print("The secret code is: ",secret_code)


# function that prints the whole history of player guesses in the game.
def print_history():
	global guesses
	global pegs
	global turn
	header = ["Guess", "", "", "", "", "Black", "White"]
	guess_number = []
	first = []
	second = []
	third = []
	fourth = []
	black_pegs = []
	white_pegs = []
	# here i create the support list to create the table
	# we need the lists containing the elements of the single column in order to compose another list that contains ...
	# ... the elements of the table in order of appareance.
	for x in range(1, turn):
		g = 4 * x - 4  # indexes of guesses
		p = 2 * x - 2  # indexes of pegs
		guess_number.append(x)
		first.append(guesses[g])  # first element of every group of four guesses
		second.append(guesses[g + 1])  # second element of every group of four guesses
		third.append(guesses[g + 2])  # third element of every group of four guesses
		fourth.append(guesses[g + 3])  # fourth element of every group of four guesses
		black_pegs.append(pegs[p])  # first element of every group of two pegs
		white_pegs.append(pegs[p + 1])  # second element of every group of two pegs
	# list containing every element of the table in order of appearance
	data = [header] + list(zip(guess_number, first, second, third, fourth, black_pegs, white_pegs))
	# composition of the table
	for i, d in enumerate(data):
		line = "| ".join(str(x).ljust(7) for x in d)
		print(line)
		if i == 0:
			# separation from header to the data
			print("- " * (int(len(line) / 2) + 1))
	# separation at the end of the table
	print("-" * len(line))


# furthermore the function gives an error if the player puts more than 4 colors or fewer than 4.
# if an error occurs the player can type the input again without any loss in the turns played.
def user_guess():
	while True:  
		try:  # checks if number of inputs is 4. If not, "except" occurs.
			# first we need to create and in case of repetition reset support variables
			global user_input  # we need the global one because we need it in another function ("input_in_guesses()")
			user_input = [0, 0, 0, 0]  # resets the user input
			var = 0  # support variable that increases only if one of the values inserted is not in "possible_inputs"
			user_input[0], user_input[1], user_input[2], user_input[3], = map(str, input(
				"Insert the colors separated by a space: ").lower().split())
			for i in user_input:  # checks if every input is in "possible_inputs"
				if i not in possible_inputs:  # if not increases the support function
					var += 1
			if var == 0:  # if no errors occurred
				return user_input  # we return "user_input" for further use
				break  # we break the while function. The input has been correctly inserted
			else:
				print("One or more of the values inserted is wrong. Please try again.")
		except ValueError:
			print("Error. Something wrong happened. Please insert the values again.")


# USER INPUT INTO GUESSES [LIST]
# This function will store the user input into the guesses list that will store the entire history of user guesses
# furthermore this function will transform the user input in readable input by the program for future reference
# (in "function compare_guess_solution()")
def input_in_guesses():
	global guesses
	global user_input
	for index, word in enumerate(user_input):
		if word == "yellow" or word == "y":
			guesses.append("yellow")
			user_input[index] = "yellow"
		elif word == "blue" or word == "b":
			guesses.append("blue")
			user_input[index] = "blue"
		elif word == "orange" or word == "o":
			guesses.append("orange")
			user_input[index] = "orange"
		elif word == "green" or word == "g":
			guesses.append("green")
			user_input[index] = "green"
		elif word == "red" or word == "r":
			guesses.append("red")
			user_input[index] = "red"
		else:
			guesses.append("white")
			user_input[index] = "white"


# function to check the solution and input
# we compare the "user_input" producing the output result of white and black pegs
def compare_guess_solution(user_input, secret_code):
	global pegs
	global black
	black = 0
	white = 0
	secret_copy = secret_code[:]  # we want a copy of the secret code in order to not change it for future turns
	user_copy = user_input[:]
	# we check for black pegs
	# first and separately we check for black pegs in order to not give false white ones.
	# if a color is in the right position we change it both in "user_copy" and "secret_copy" ...
	# ... in this way it will not be checked again when we will check for white pegs.
	for index, input in enumerate(user_copy):
		if input == secret_copy[index]:
			black += 1
			secret_copy[index] = "checked solution"
			user_copy[index] = "checked user"
	# now we check for white pegs
	# here, as we did for the black pegs, if a color is right but in the wrong position we change that ...
	# ... color in the "secret_copy" in this way we will not control it again giving fake white pegs
	for index, input in enumerate(user_copy):
		for i, p in enumerate(secret_copy):
			if p == input:
				white += 1
				secret_copy[i] = "checked solution"
				break
	# implementation of result in pegs list
	pegs.append(black)
	pegs.append(white)


# resets global variables in order to restart with another game.
# function embedded in "replay()"
def reset():
	global turn
	global guesses
	global pegs
	turn = 0
	guesses = []
	pegs = []


# asks the player if they want to play again, after a game.
def replay():
	again = input("Would you like to play again? Y/N: ").lower().replace(" ", "")
	if again == "y":
		print('\n' * 31)  # clean the window
		reset()
		mastermind()  # starts with another game
	else:
		print("See you soon!")


# checks if the player guessed the secret code.
def check_victory():
	global black
	global turn
	if black == 4:
		print("Compliments, you won with ", turn, " turn(s)!")
		turn = 100  # this makes the game to finish!
		replay()


# function that activates the game itself. This function contain all of the other inside of it.
def mastermind():
	global turn
	while turn < 9:
		turn += 1
		if turn == 1:  # first turn. We print instructions
			welcome()
			generate_secret_code() 
			print("Turn: 1")
		elif turn > 1:
			print("-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - \n")
			print("Turn: ", turn)
			print_history()
		user_guess()
		input_in_guesses()
		compare_guess_solution(user_input, secret_code)
		check_victory()
	else:
		if turn != 100:
			print("You lose. You used all your available guesses.")
			print("The secret code was:", secret_code[0], "-", secret_code[1], "-", secret_code[2], "-", secret_code[3], ".")
			replay()


mastermind()
