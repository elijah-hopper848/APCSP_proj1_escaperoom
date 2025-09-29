from random import randint

from classes import Describable
from storyclasses import CaveRoom

INVALID_COMMAND_QUOTES = ["What?", "Speak english.", "I don't know what you mean.", "What do you mean?"]

INVENTORY = []
ROOMS = {
	"cave": CaveRoom()
}

CURRENT_ROOM = ROOMS["cave"]

def take(item: str):
	pass

print("Commands:\nexamine [thing]\ntake [thing]\nuse [thing] on [other thing]\nuse [thing]")

while True:
	text = input("> ").lower()
	parts = text.split(" ")

	command = parts[0]

	if command == "examine":
		target = len(parts) == 1 and "room" or parts[1]

		if target == "room":
			print(CURRENT_ROOM.describe())
		elif CURRENT_ROOM.features != None:
			thing = CURRENT_ROOM.features.get(target)

			if thing == None:
				print(f"There is no '{target}'")
				continue

			print(f"You examine the {target}...")
			print(thing.examine())
	else:
		quote = INVALID_COMMAND_QUOTES[randint(0, len(INVALID_COMMAND_QUOTES) - 1)]

		print(quote)
