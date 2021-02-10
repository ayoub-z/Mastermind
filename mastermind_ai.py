from random import choice
import secrets
from itertools import product

#############
# VARIABLES #
#############

combinations = list(product('abcdcd', repeat=4)) # ALl possible combinations
combis = [''.join(i) for i in combinations[:]] # Copy + cleaned up list of combinations
code = secrets.choice(combis) 
print('secret code is: ',code) # For testing


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


##############
# Strategies #
##############

def worst_case_strategy():
	scores = {}
	for guess1 in combis:
		possibilities = {}
		for guess2 in combis:
			possible_feedback = tuple(pins(guess1, guess2))  
			if possible_feedback in possibilities:
				possibilities[possible_feedback] += 1
			else:
				possibilities[possible_feedback] = 1
		scores[guess1] = max(possibilities.values())
	best  = min(scores.values())
	guess = ''
	for possible_guess in scores.keys():
		if scores[possible_guess] == best:
			guess = possible_guess
	return guess

# Can't get any simpler
def simple_strategy():
	return combis[0]


def heuristic_strategy():
	return secrets.choice(combis)
	pass


########
# GAME #
########
		
def ai_play():
	c = 0 # Keeps count on amount of guesses
	global combis # Making it global, so we can edit it
	while True:
		c += 1 
		guess = heuristic_strategy() 
		if len(combis) == 0: # Checks if 0 possibilites left
			print('You probably gave wrong feedback pins. Try again')
			quit()
		print(f'Guess {c}: {guess}')
		BlackPin = int(input('Black pins: ')) # Feedback black pin
		if BlackPin == int(len(guess)): # Success message if 4 black pins
			print(f'Got it in {c} turns!')
			break
		WhitePin = int(input('White pins: ')) # Feedback white pin
		rightCombis = [] # for keeping the leftover possibilities
		for possibilities in combis: # Goes through all possible combinations
			if pins(guess, possibilities) == [BlackPin, WhitePin]: # compares feedback of all combinations with given feedback
				rightCombis.append(possibilities) # adds combinations that have matching feedback with given feedback in one list
		combis = rightCombis[:] # Updates combination list
		print('Aantal mogelijkheden:',len(combis))
		if len(combis) == 1: # Success message if only 1 possibility left
			print(f'Your code is: {combis[0]}')
			print(f'Got it in {c} turns')
			break
		else:
			continue

ai_play()
		
