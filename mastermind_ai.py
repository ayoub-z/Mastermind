import os
import random
import statistics
from itertools import product

#############
# VARIABLES #
#############

raw_combinations = list(product('abcdef', repeat=4)) # all possible combinations
combis = sorted([''.join(i) for i in raw_combinations[:]]) # cleaned up and sorted list of combinations
all_combis = combis[:] # keeps a list of all combinations at all times
code = random.choice(combis) # secret code for testing


# compares feedback of a guess, with a different possible guess to see if it has matching feedback
def feedback_pins(guess, possible_guess):
	'''
	Bron: https://repl.it/@ThomasS1/Mastermind
	      (regel 71 in code)
	'''
	blackPin = 0
	whitePin = 0
	guess = list(guess)
	possible_guess = list(possible_guess)
	remainingGuess = guess[:] # keeps track of remaining guesses that have yet to receive a black pin
	remainingPosGuess = possible_guess[:] # remaining letters that were not guessed correctly
	for n in range(0, len(guess)-1):
		if guess[n] == possible_guess[n]: # checks if each letter in possible_guess matches letters in guess
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
	BlackPin = feedback_pins(guess, code)[0] # For AUTOMATIC feedback when testing
	WhitePin = feedback_pins(guess,code)[1]
	rightCombis = [] # holds the leftover possibilities

	for possibilities in combis: # Goes through all possible combinations
		if feedback_pins(guess, possibilities) == [BlackPin, WhitePin]: # compares feedback of all combinations with given feedback
			rightCombis.append(possibilities) # adds combinations that have matching feedback with given feedback in one list
	return rightCombis


##############
# Strategies #
##############

# Sorts possibilities based on worst possible outcome and chooses the best one out of those
def worst_case_strategy():
	'''
	Bron: https://en.wikipedia.org/wiki/Mastermind_(board_game)
	Bron: https://repl.it/@ThomasS1/Mastermind 
		  (regel 458 in code)
	'''
	all_possibilities = {}
	if len(combis) == 1296:
		guess = ('aabb') # 'aabb' according to Knuth's algorithm
		combis.remove(guess)
	else:
		for guess1 in all_combis: # checks ALL combinaions for guess with best feedback, even if guess is incorrect
			possibilities = {}
			for guess2 in combis: # compares it with list that has all POSSIBLE correct guesses
				possible_feedback = tuple(feedback_pins(guess1, guess2))  
				if possible_feedback in possibilities:
					possibilities[possible_feedback] += 1 # adds value +1 to existing guess in dict
				else:
					possibilities[possible_feedback] = 1 # creates new guess in dict if it doesn't exist and gives value 1
				all_possibilities[guess1] = max(possibilities.values()) # Chooses worst possible outcome from each guess
		best_choice = min(all_possibilities.values()) # guess that has lowest amount of possible leftover guesses
		guess = ''
		for possible_guess in all_possibilities.keys(): 
			if all_possibilities[possible_guess] == best_choice: # finds guess with matching value
				guess = possible_guess
	return guess


# Can't get any simpler
def simple_strategy():
	return combis[0]


# Similar to worst case strategy
# however, instead of sorting them on worst outcome and choosing the best one
# it sorts them on the median outcome and chooses the best out of that, also starts with 'aabc'
def avg_case_strategy():
	all_possibilities = {}
	if len(combis) == 1296:
		return ('aabc')
	else:
		for guess_1 in all_combis:
			possibilities = {}
			for guess_2 in combis:
				possible_feedback = tuple(feedback_pins(guess_1, guess_2))
				if possible_feedback in possibilities:
					possibilities[possible_feedback] += 1
				else:
					possibilities[possible_feedback] = 1
				all_possibilities[guess_1] = statistics.median(possibilities.values()) # chooses median outcome for each guess.
		best_choice = min(all_possibilities.values()) # guess that has lowest median of leftover guesses
		guess = ''
		for possible_guess in all_possibilities.keys():
			if all_possibilities[possible_guess] == best_choice:
				guess = possible_guess
		return guess


def play_WorstCaseStrat():
	c = 0 # Keeps track of turn number
	global combis
	while True:
		c += 1 
		guess = worst_case_strategy()
		if len(combis) == 0: # Checks if 0 possibilites left and gives error message if so
			print('Oops, something went wrong. Most likely wrong feedback given.')
			quit()
		print(f'Guess {c}: {guess}')
		combis = reduce_function(guess)
		print('\nAantal mogelijkheden2:',len(combis))
		if len(combis) == 1: # Success message if only 1 possibility left
			print(f'Your code is: {combis[0]}')
			print(f'Got it in {c} turns')
			break
		else:
			continue


def play_SimpleStrat():
	c = 0 
	global combis
	while True:
		c += 1
		guess = simple_strategy()
		if len(combis) == 0: 
			print('Oops, something went wrong. Most likely wrong feedback given.')
			quit()
		print(f'Guess {c}: {guess}')
		if len(combis) != 1:
			combis = reduce_function(guess)
		print('\nAantal mogelijkheden2:',len(combis))
		if len(combis) == 1: 
			print(f'Your code is: {combis[0]}')
			print(f'Got it in {c} turns')
			break
		elif guess in combis: # guess is removed when used, otherwise errors may occur
			combis.remove(guess)
			continue
		else:
			continue


def play_AvgCaseStrat():
	c = 0 
	global combis
	while True:
		c += 1
		guess = avg_case_strategy()
		if len(combis) == 0: 
			print('Oops, something went wrong. Most likely wrong feedback given.')
			quit()
		print(f'Guess {c}: {guess}')
		combis = reduce_function(guess)
		print('\nAantal mogelijkheden2:',len(combis))
		if len(combis) == 1: 
			print(f'Your code is: {combis[0]}')
			print(f'Got it in {c} turns')
			break
		else:
			continue


