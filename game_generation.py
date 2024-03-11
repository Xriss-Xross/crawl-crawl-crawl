import random


def generate():
	levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # the levels possible
	levelsToSpawn = []  # to be generated random order
	for i in range(0, 7):
		rand = random.randint(0, len(levels)-1)
		levelsToSpawn.append(levels[rand])
		levels.pop(rand)

	return(levelsToSpawn)
