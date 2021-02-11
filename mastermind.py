import random
import collections

'''bron: https://www.youtube.com/watch?v=Hv47MO1vQAo'''

length  = 4
guesses = 9
pattern = ''.join(random.choice('abcdef')for i in range(length))

counted = collections.Counter(pattern)

def running():
	while True:
		try:
			guess = input('Enter guess: ').lower() # Loops until valid answer is given
			if len(guess) == 4:
				break
			else:
				raise ValueError()  # goes to except
		except:
			print('I think you mistyped something. Try again')
	guess_count = collections.Counter(guess)
	close = sum(min(counted[k], guess_count[k]) for k in counted)
	exact = sum(a==b for a,b in zip(pattern, guess))
	close -= exact
	print('Black pins: {} | White pins: {}.'.format(exact, close))
	return exact != length

def start():
	print('Secret code is: ',pattern, '\n') # For testing
	print('Make sure to enter your guess WITHOUT any spaces')
	for attempt in range(guesses):
		if not running():
			print('You guessed it!')
			break
		else:
			pass
	else:
		print('Game over. The secret code was {}.'.format(''.join(pattern)))
