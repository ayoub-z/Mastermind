import os
import random
import statistics
import collections
from itertools import product

#############
# VARIABLES #
#############

raw_combinations = list(product('abcdef', repeat=4)) # all possible combinations
combis = sorted([''.join(i) for i in raw_combinations[:]]) # cleaned up and sorted list of combinations
all_combis = combis[:] # keeps a list of all combinations at all times
code = random.choice(combis) # secret code for testing

### joined the variables so that they're all in one file
length  = 4 # length of secret code
guesses = 9 # total turns
pattern = ''.join(random.choice('abcdef')for i in range(length)) # generates secret code
counted = collections.Counter(pattern) # counts the amount of each letter in the secret code



def feedback_pins(guess, possible_guess):
	'''
	Compares the feedback of a guess, with a different possible guess 
	to see if the feedback matches.
	Bron: https://repl.it/@ThomasS1/Mastermind
	      (regel 71 in code)
	''' ### added docstring
	blackPin = 0
	whitePin = 0
	guess = list(guess)
	possible_guess = list(possible_guess)
	remainingGuess = guess[:] # keeps track of remaining guesses that have yet to receive a black pin
	remainingPosGuess = possible_guess[:] # remaining letters that were not guessed correctly
	for n in range(0, len(guess)-1):
		if guess[n] == possible_guess[n]: # checks if each letter in possible_guess matches letters in guess
			blackPin += 1
			remainingGuess.remove(guess[n]) ### removes guessed letter if it matches letter in secret code
			remainingPosGuess.remove(possible_guess[n]) ### removes guessed letter if it matches letter in secret code
	for color in remainingPosGuess: 
		if color in guess: ### checks for guessed letters that are correct, but in wrong position
			whitePin += 1
			remainingPosGuess.remove(color)
	return [blackPin, whitePin]



def reduce_function(guess):
	'''
	Loops through the list of possible guesses and checks for values that match
	the current feedback. If the guess matches the feedback, it's added to a specific list.
	''' ### added docstring
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



def worst_case_strategy():
	'''
	Sorts all possible guesses based on worst possible outcome 
	and chooses the best one out of that.
	Bron: https://en.wikipedia.org/wiki/Mastermind_(board_game)
	Bron: https://repl.it/@ThomasS1/Mastermind 
		  (regel 458 in code)
	''' ### added docstring
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
				all_possibilities[guess1] = max(possibilities.values()) # chooses worst possible outcome from each guess
		best_choice = min(all_possibilities.values()) # guess that has lowest amount of possible leftover guesses
		guess = ''
		for possible_guess in all_possibilities.keys(): 
			if all_possibilities[possible_guess] == best_choice: # finds guess with matching value
				guess = possible_guess
	return guess



def simple_strategy():
	'''
	Picks the first guess in a sorted list.
	bron: https://www.rug.nl/research/portal/files/9871441/icgamaster.pdf
	''' ### added docstring
	return combis[0] # returns the first string in the list


#Heuristieke strategie
def avg_case_strategy():
	'''
	Similar to Worst Case Strategy
	however, instead of sorting guesses on worst outcome and choosing the best one
	it sorts them on the median outcome and chooses the best out of that, 
	also starts with 'aabc' instead of 'aabb'
	''' ### added docstring
	all_possibilities = {}
	if len(combis) == 1296: ### checks if it's turn 1 (no guesses have been made)
		return ('aabc') ### returns 'aabc' as the first guess if it's turn 1
	else:
		for guess_1 in all_combis: ### checks ALL combinaions for guess with best feedback, even if guess is incorrect
			possibilities = {}
			for guess_2 in combis: ### compares it with list that has all POSSIBLE correct guesses
				possible_feedback = tuple(feedback_pins(guess_1, guess_2))
				if possible_feedback in possibilities:
					possibilities[possible_feedback] += 1 ### adds value +1 to existing guess in dict
				else:
					possibilities[possible_feedback] = 1 ### creates new guess in dict if it doesn't exist and gives value 1
				all_possibilities[guess_1] = statistics.median(possibilities.values()) # chooses median outcome for each guess.
		best_choice = min(all_possibilities.values()) # guess that has lowest median of leftover guesses
		guess = ''
		for possible_guess in all_possibilities.keys():
			if all_possibilities[possible_guess] == best_choice: ### finds guess with matching value
				guess = possible_guess
		return guess


def play_WorstCaseStrat():
	'''
	Function that activates the Worst Case strategy so that it can be used
	when playing the Mastermind Game
	''' ### added docstring
	c = 0 ### counter to keep track of turns
	global combis
	print('Secret code is: ',code,'\n\n') # visualizes the code for when testing
	while True:
		c += 1 
		guess = worst_case_strategy()
		if len(combis) == 0: # checks if 0 possibilites left and gives error message if so
			print('Oops, something went wrong. Most likely wrong feedback given.')
			quit()
		print(f'Guess {c}: {guess}') 
		combis = reduce_function(guess) ### shortens list of possible guesses after feedback
		print('\nAantal mogelijkheden2:',len(combis))
		if len(combis) == 1: # success message if only 1 possibility left
			print(f'Your code is: {combis[0]}')
			print(f'Got it in {c} turns')
			break
		else:
			continue


def play_SimpleStrat():
	'''
	Function that activates the Simple Strategy so that it can be used
	when playing the Mastermind Game
	''' ### added docstring
	c = 0 # counter to keep track of turns
	global combis
	print('Secret code is: ',code,'\n\n') # for testing
	while True:
		c += 1 
		guess = simple_strategy()
		if len(combis) == 0: ### checks if 0 possibilites left and gives error message if so
			print('Oops, something went wrong. Most likely wrong feedback given.')
			quit()
		print(f'Guess {c}: {guess}')
		if len(combis) != 1: ### only use reduce function if there's at least 2 possibile guesses
			combis = reduce_function(guess)
		print('\nAantal mogelijkheden2:',len(combis))
		if len(combis) == 1: ### success message if only 1 possibility left
			print(f'Your code is: {combis[0]}')
			print(f'Got it in {c} turns')
			break
		elif guess in combis: # guess is removed when used, otherwise errors may occur
			combis.remove(guess)
			continue
		else:
			continue


def play_AvgCaseStrat():
	'''
	Function that activates the Average Case Strategy so that it can be used
	when playing the Mastermind Game
	''' ### added docstring
	c = 0 ### counter to keep track of turns
	print('Secret code is: ',code,'\n\n') # for testing
	global combis
	while True:
		c += 1 
		guess = avg_case_strategy()
		if len(combis) == 0: ### checks if 0 possibilites left and gives error message if so
			print('Oops, something went wrong. Most likely wrong feedback given.')
			quit()
		print(f'Guess {c}: {guess}')
		combis = reduce_function(guess) ### only use reduce function if there's at least 2 possibile guesses
		print('\nAantal mogelijkheden2:',len(combis))
		if len(combis) == 1: ### success message if only 1 possibility left
			print(f'Your code is: {combis[0]}')
			print(f'Got it in {c} turns')
			break
		else:
			continue


