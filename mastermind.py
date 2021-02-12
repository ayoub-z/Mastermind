import random
import collections
from mastermind_ai import *

'''bron: https://www.youtube.com/watch?v=Hv47MO1vQAo'''

length  = 4 # length of secret code
guesses = 9 # total turns
pattern = ''.join(random.choice('abcdef')for i in range(length)) # generates secret code

counted = collections.Counter(pattern) # counts the amount of each letter in the secret code

def running():
	while True:
		try: # loops until valid answer is given
			guess = input('Enter guess: ').lower() 
			if len(guess) == 4:
				break
			else:
				raise ValueError()  # goes to except and prints error with instruction.
		except:
			print('I think you mistyped something. Try again')
	guess_count = collections.Counter(guess) # counts the amount of each letter in the secret code
	whitePin = 0
	# sum(min(counted[k], guess_count[k]) for k in counted) 
	for k in counted: # loops through each letter in secret code
		whitePin += min(counted[k], guess_count[k]) # counts letters that are in secret code, but at wrong position
	blackPin = sum(a==b for a,b in zip(pattern, guess)) # counts matching letters in guess and secret code 
	whitePin -= blackPin
	print('Black pins: {} | White pins: {}.'.format(blackPin, whitePin))
	return blackPin != length # keeps running until there are 4 black pins, the length of the guess

def start():
	print('Secret code is: ',pattern, '\n') # For testing
	print('Make sure to enter your guess WITHOUT any spaces')
	for attempt in range(guesses): # gives you 9 turns to guess the code before stopping
		if not running():
			print(f'You guessed it!')
			break
		else:
			pass
	else:
		print('Game over. The secret code was {}.'.format(''.join(pattern)))

def play():
	os.system('clear')
	choice = int(input(
					   '===============Welcome=============== \n'
					   'Let\'s start with choosing a strategy!\n\n'
					   '1: Worst Case Strategy\n'
					   '2: Simple Strategy\n'
					   '3: I\'d rather guess the code myself \n\n'
					   'Type the strategy number you want to use: '
					  ))
	print('------------------------------------------------------')
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

play()