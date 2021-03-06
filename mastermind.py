from mastermind_ai import *



def running():
	'''
	Standard Mastermind Game. It is compromised out of 6 colors (letters in this case).
	Each game 4 letters are chosen out of the 6 and it is your job to guess them.
	You have 9 turns, goodluck!
	Bron: https://www.youtube.com/watch?v=Hv47MO1vQAo
	''' ### added docstring
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
	'''
	Function to check if the game is still running or whether all 9 turns have been used.
	In which case a "Game Over" message is given with the secret code
	''' ### added docstring
	print('Secret code is: ',pattern, '\n\n') # for testing
	print('Make sure to enter your guess WITHOUT any spaces')
	for attempt in range(guesses): ### gives you 9 turns to guess the code before stopping
		if not running():
			print(f'You guessed it!')
			break
		else:
			pass
	else:
		print('Game Over. The secret code was {}.'.format(''.join(pattern)))

def play():
	'''
	Functions makes use of all the strategy functions and allows you to play the game.
	You get the option to either play the game yourself (option 4), or to let the ai
	find your guess using any of the 3 strategies (option 1-3)
	''' ### added docstring
	os.system('clear') ### clears the terminal before the game starts
	choice = int(input( ### greeting and instruction message
					   '===============Welcome=============== \n'
					   'Let\'s start with choosing a strategy!\n\n'
					   '1: Worst Case Strategy\n'
					   '2: Simple Strategy\n'
					   '3: Average Case Strategy\n'
					   '4: I\'d rather guess the code myself \n\n'
					   'Type the strategy number you want to use: '
					  ))
	print('-------------------------------------------------------\n')
	if choice == 1: 
		choice = play_WorstCaseStrat() ### choice 1, Worst Case Strategy
	elif choice == 2: 
		choice = play_SimpleStrat() ### choice 2, Simple Strategy
	elif choice == 3: 
		choice = play_AvgCaseStrat() ### choice 3, Average Case Strategy
	elif choice == 4: 
		choice = start() ### choice 4 is to play against the Computer yourself
	return choice

play()