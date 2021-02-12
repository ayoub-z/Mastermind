import os
import random
from itertools import product


#############
# VARIABLES #
#############

raw_combinations = list(product('abcdef', repeat=4)) # ALl possible combinations
combis = sorted([''.join(i) for i in raw_combinations[:]]) # cleaned up and sorted list of combinations
code = random.choice(combis) 


# Compares feedback of guess, with possible guesses to find matching combinations
def pins(guess, answer):
	black = 0
	white = 0
	guess = list(guess)
	answer = list(answer)
	remainingGuess = guess[:]  # the guessed colours that were not given a black peg
	remainingAnswer = answer[:]  # the answer colours that were not correctly guessed

	for n in range(len(guess)):
		if answer[n] == guess[n]:
			black += 1
			remainingGuess.remove(guess[n])
			remainingAnswer.remove(answer[n])

	for colour in remainingGuess:
		if colour in remainingAnswer:
			white += 1
			remainingAnswer.remove(colour)
	return [black, white]




def reduce_function(guess1):
	# Making it global, so we can edit it
	# BlackPin = int(input('Black pins: '))
	# WhitePin = int(input('White pins: '))
	BlackPin = pins(guess1, code)[0] # For automatic feedback when testing
	WhitePin = pins(guess1,code)[1]
	rightCombis = [] # for keeping the leftover possibilities

	for possibilities in combis: # Goes through all possible combinations
		if pins(guess1, possibilities) == [BlackPin, WhitePin]: # compares feedback of all combinations with given feedback
			rightCombis.append(possibilities) # adds combinations that have matching feedback with given feedback in one list
	return rightCombis



def worst_case_strategy():
	all_possibilities = {}
	if len(combis) == 1296:
		return ('aabb')
	else:
		for guess1 in combis:
			possibilities = {}
			for guess2 in combis:
				possible_feedback = tuple(pins(guess1, guess2))  
				if possible_feedback in possibilities:
					possibilities[possible_feedback] += 1
				else:
					possibilities[possible_feedback] = 1
				all_possibilities[guess1] = max(possibilities.values())
		best = min(all_possibilities.values())
		guess = ''
		for possible_guess in all_possibilities.keys():
			if all_possibilities[possible_guess] == best:
				guess = possible_guess
		return guess

# Can't get any simpler
def simple_strategy():
	return combis[0]

		
def play_WorstCaseStrat():
	c = 0 # Keeps count on amount of guesses
	global combis
	while True:
		guess = worst_case_strategy()
		c += 1 
		if len(combis) == 0: # Checks if 0 possibilites left
			print('You probably gave wrong feedback pins. Try again')
			quit()
		print(f'Guess {c}: {guess}')
		combis = reduce_function(guess)
		print('\nAantal mogelijkheden2:',len(combis))
		if len(combis) == 1 or c >= 6: # Success message if only 1 possibility left
			print(f'Your code is: {combis[0]}')
			print(f'Got it in {c} turns')
			break
		else:
			continue

def play_SimpleStrat():
	c = 0 # Keeps count on amount of guesses
	global combis
	while True:
		# if len(combis) == 0: # Checks if 0 possibilites left
		# 	print('You probably gave wrong feedback pins. Try again')
		# 	quit()
		guess = simple_strategy()
		c += 1 
		print(f'Guess {c}: {guess}')
		combis = reduce_function(guess)
		print('\nAantal mogelijkheden2:',len(combis))
		if len(combis) == 1 or c >= 6: # Success message if only 1 possibility left
			print(f'Your code is: {combis[0]}')
			print(f'Got it in {c} turns')
			break
		else:
			continue








