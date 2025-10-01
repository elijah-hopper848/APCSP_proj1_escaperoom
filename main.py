from random import randint

from classes import Player
from storyclasses import CaveRoom

INVALID_COMMAND_QUOTES = ["What?", "Speak english.", "I don't know what you mean.", "What do you mean?"]
ROOMS = {
	"cave": CaveRoom()
}

MAIN_PLAYER = Player(init_room=ROOMS["cave"])

print("Commands:\nexamine [thing]\ntake [thing]\nuse [thing]\nuse [thing] with [item]\n")
print(MAIN_PLAYER.current_room.describe())

while True:
	text = input("> ").lower()
	parts = text.split(" ")

	command = parts[0]

	if command == "examine":
		if len(parts) == 1:
			print("Examine what?")
			continue

		print(MAIN_PLAYER.examine(parts[1]))
	elif command == "take":
		if len(parts) == 1:
			print("Take what?")
			continue

		print(MAIN_PLAYER.take(parts[1]))
	elif command == "use":
		if len(parts) == 1:
			print("Use what?")
			continue
		
		# valid, technically
		# not using an item on something
		if len(parts) == 2:
			print(MAIN_PLAYER.use(parts[1], None))
			continue

		if len(parts) <= 3:
			print("With what?")
			continue
		
		print(MAIN_PLAYER.use(parts[1], parts[3]))
	else:
		quote = INVALID_COMMAND_QUOTES[randint(0, len(INVALID_COMMAND_QUOTES) - 1)]

		print(quote)
