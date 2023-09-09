import random


def generate_next_rooms(rooms_remaining, treasure_chance, treasures_remaining, rooms_to_spawn, prefabs):

	next_rooms = []

	if rooms_remaining >= 3:
		rooms = random.randint(1,3)
		rooms_remaining -= rooms
	else:
		rooms = random.randint(1, rooms_remaining)
		rooms_remaining -= rooms

	for i in range(rooms):
		if random.randint(1,100) <= 10 and treasures_remaining == 1:
			treasures_remaining -= 1
			next_rooms.append("a")
		else:
			n = random.randint(0, len(prefabs)-1)
			next_rooms.append(prefabs[n])
			prefabs.pop(n)

	return next_rooms, prefabs, rooms_remaining, treasures_remaining


def generate():
	
	rooms_remaining = 7
	prefabs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	treasures_remaining = 1
	map = []
	
	while rooms_remaining != 0:
		next_rooms, prefabs, rooms_remaining, treasures_remaining = generate_next_rooms(rooms_remaining, 10, treasures_remaining , [], prefabs)
		map.append(next_rooms)
	map.append([prefabs[random.randint(0, len(prefabs)-1)]])
	return map
