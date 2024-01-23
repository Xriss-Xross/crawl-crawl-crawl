import random


def generate_next_rooms(rooms_remaining, prefabs):

	next_rooms = []

	if rooms_remaining >= 3:
		rooms = random.randint(1,3)
		rooms_remaining -= rooms
	else:
		rooms = random.randint(1, rooms_remaining)
		rooms_remaining -= rooms

	for i in range(rooms):
		n = random.randint(0, len(prefabs)-1)
		next_rooms.append(prefabs[n])
		prefabs.pop(n)

	return next_rooms, prefabs, rooms_remaining


def generate():
	
	rooms_remaining = 7
	prefabs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	map = []
	
	while rooms_remaining != 0:
		next_rooms, prefabs, rooms_remaining = generate_next_rooms(rooms_remaining, prefabs)
		map.append(next_rooms)
	map.append([prefabs[random.randint(0, len(prefabs)-1)]])
	return map