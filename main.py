from random import randint

from utility.ANSI import tint16, tint_bad, BRIGHT_BLACK

from classes import Player
from rooms.cave import CaveRoom
from rooms.library import LibraryRoom

INVALID_COMMAND_QUOTES = ["What?", "Speak english.", "I don't know what you mean.", "What do you mean?"]

INITIAL_ROOM = CaveRoom(LibraryRoom())
MAIN_PLAYER = Player(init_room=INITIAL_ROOM)

print("Only 2 puzzles because im lazy and also out of time lol")
print("you will also need a lot of patience to complete this, unless you're like a god at escape rooms\n")

def display_help():
	print(tint16("Commands:\n examine [thing]\n take [thing]\n use [thing]\n use [thing] with [item]\n help\n\nRun 'examine room' to get your bearings\n", BRIGHT_BLACK))

display_help()
print(MAIN_PLAYER.current_room.describe())

def parse(args: list[str]) -> str:
	command = args[0]
	
	if command == "examine":
		if len(args) == 1:
			return tint_bad("Examine what?")

		return MAIN_PLAYER.examine(args[1])
	elif command == "take":
		if len(args) == 1:
			return tint_bad("Take what?")

		return MAIN_PLAYER.take(args[1])
	elif command == "use":
		if len(args) == 1:
			return tint_bad("Use what?")
		
		# valid, technically
		# not using an item on something
		if len(args) == 2:
			return MAIN_PLAYER.use(args[1], None)

		if len(args) <= 3:
			return tint_bad("With what?")
		
		return MAIN_PLAYER.use(args[1], args[3])
	elif command == "help":
		display_help()
		return ""
	else:
		quote = INVALID_COMMAND_QUOTES[randint(0, len(INVALID_COMMAND_QUOTES) - 1)]

		return tint_bad(quote)

while True:
	text = MAIN_PLAYER.prompt("> ").lower()
	args = text.split(" ")

	output = parse(args)
	
	MAIN_PLAYER.display(output)
