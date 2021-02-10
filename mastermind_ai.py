from random import choice
import secrets
from itertools import product

#############
# VARIABLES #
#############

combinations = list(product('abcdcd', repeat=4)) 
combis = [''.join(i) for i in combinations[:]] 
code = secrets.choice(combis) 
print('secret code is: ',code) 



def pins(guess, answer):
	black = 0
	white = 0
	guess = list(guess)
	answer = list(answer)
	remainingGuess = guess[:]  
	remainingAnswer = answer[:]  

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


def simple_strategy():
	return combis[0]


def heuristic_strategy():
	return secrets.choice(combis)
	pass


########
# GAME #
########
		
def ai_play():
	c = 0 
	global combis 
	while True:
		c += 1 
		guess = heuristic_strategy() 
		if len(combis) == 0: 
			print('You probably gave wrong feedback pins. Try again')
			quit()
		print(f'Guess {c}: {guess}')
		BlackPin = int(input('Black pins: ')) 
		if BlackPin == int(len(guess)): 
			print(f'Got it in {c} turns!')
			break
		WhitePin = int(input('White pins: ')) 
		rightCombis = [] 
		for possibilities in combis: 
			if pins(guess, possibilities) == [BlackPin, WhitePin]: 
				rightCombis.append(possibilities) 
		combis = rightCombis[:] 
		print('Aantal mogelijkheden:',len(combis))
		if len(combis) == 1: 
			print(f'Your code is: {combis[0]}')
			print(f'Got it in {c} turns')
			break
		else:
			continue

ai_play()