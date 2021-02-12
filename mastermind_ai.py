import os
import random
from itertools import product

#############
# VARIABLES #
#############

raw_combinations = list(product('abcdef', repeat=4)) # all possible combinations
combis = sorted([''.join(i) for i in raw_combinations[:]]) # cleaned up and sorted list of combinations
code = random.choice(combis) # secret code for testing


# compares feedback of a guess, with a different possible guess to see if it has matching feedback
def feedback_pins(guess, possible_guess):
	'''
	bron: https://repl.it/@ThomasS1/Mastermind
	Regel 71
	'''
	blackPin = 0
	whitePin = 0
	guess = list(guess)
	possible_guess = list(possible_guess)
	remainingGuess = guess[:] # keeps track of remaining guesses that have yet to receive a black pin
	remainingPosGuess = possible_guess[:] # remaining letters that were not guessed correctly
	for n in range(0, len(guess)-1):
		if guess[n] == possible_guess[n]: # checks for each letter in possible_guess if it matches that of guess
			blackPin += 1
			remainingGuess.remove(guess[n]) 
			remainingPosGuess.remove(possible_guess[n])
	for color in remainingPosGuess:
		if color in guess:
			whitePin += 1
			remainingPosGuess.remove(color)
	return [blackPin, whitePin]




def reduce_function(guess):
	# BlackPin = int(input('Black feedback_pins: '))
	# WhitePin = int(input('White feedback_pins: '))
	BlackPin = feedback_pins(guess, code)[0] # For automatic feedback when testing
	WhitePin = feedback_pins(guess,code)[1]
	rightCombis = [] # for keeping the leftover possibilities

	for possibilities in combis: # Goes through all possible combinations
		if feedback_pins(guess, possibilities) == [BlackPin, WhitePin]: # compares feedback of all combinations with given feedback
			rightCombis.append(possibilities) # adds combinations that have matching feedback with given feedback in one list
	return rightCombis


##############
# Strategies #
##############


def worst_case_strategy():
	'''
	bron: https://repl.it/@ThomasS1/Mastermind
	regel 458
	'''
	all_possibilities = {}
	if len(combis) == 1296:
		return ('aabb')
	else:
		for guess1 in combis:
			possibilities = {}
			for guess2 in combis:
				possible_feedback = tuple(feedback_pins(guess1, guess2))  
				if possible_feedback in possibilities:
					possibilities[possible_feedback] += 1
				else:
					possibilities[possible_feedback] = 1
				all_possibilities[guess1] = max(possibilities.values())
		bestChoice = min(all_possibilities.values())
		guess = ''
		for possible_guess in all_possibilities.keys():
			if all_possibilities[possible_guess] == bestChoice:
				guess = possible_guess
		return guess


# Can't get any simpler
def simple_strategy():
	return combis[0]


# Heuristieke strategie
def mystery_strategy():
	pass
		
def play_WorstCaseStrat():
	c = 0 # Keeps count on amount of guesses
	global combis
	while True:
		c += 1 
		guess = worst_case_strategy()
		if len(combis) == 0: # Checks if 0 possibilites left
			print('You probably gave wrong feedback pins. Try again')
			quit()
		print(f'Guess {c}: {guess}')
		combis = reduce_function(guess)
		print('\nAantal mogelijkheden2:',len(combis))
		if len(combis) == 1: # Success message when secret code is found
			print(f'Your code is: {combis[0]}')
			print(f'Got it in {c} turns')
			break
		else:
			continue


def play_SimpleStrat():
	c = 0 # Keeps count on amount of guesses
	global combis
	while True:
		c += 1 
		guess = simple_strategy()
		if len(combis) == 0: # Checks if 0 possibilites left
			print('Woops, something went wrong. Most likely wrong feedback was given.')
			quit()
		print(f'Guess {c}: {guess}')
		combis = reduce_function(guess)
		print('\nAantal mogelijkheden2:',len(combis))
		if len(combis) == 1: # Success message when secret code is found
			print(f'Your code is: {combis[0]}')
			print(f'Got it in {c} turns')
			break
		else:
			continue

def play_MysteryStrat():
	pass

def play():
	os.system('clear')
	choice = int(input(
					   '====================Welcome==================== \n'
					   'Let\'s start with choosing a strategy for the AI!\n\n'
					   '1: Worst Case Strategy\n'
					   '2: Simple Strategy\n'
					   '3: I\'d rather guess the code myself \n\n'
					   'Pick a strategy or type 3 to guess yourself: '
					  ))
	if choice < 3:
		print('Secret code is: ',code) # For testing
		print('')
	if choice == 1:
		choice = play_WorstCaseStrat()
	elif choice == 2:
		choice = play_SimpleStrat()
	elif choice == 3:
		choice = start()
	return choice




