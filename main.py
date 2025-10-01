from random import randint

from utility.ANSI import tint16, t_not_ok, BRIGHT_BLACK

from classes import Player
from rooms.cave import CaveRoom

INVALID_COMMAND_QUOTES = ["What?", "Speak english.", "I don't know what you mean.", "What do you mean?"]
ROOMS = {
	"cave": CaveRoom()
}

MAIN_PLAYER = Player(init_room=ROOMS["cave"])

print(tint16("Commands:\n examine [thing]\n take [thing]\n use [thing]\n use [thing] with [item]\n", BRIGHT_BLACK))
print(MAIN_PLAYER.current_room.describe())

def parse(args: list[str]) -> str:
	command = args[0]
	
	if command == "examine":
		if len(args) == 1:
			return t_not_ok("Examine what?")

		return MAIN_PLAYER.examine(args[1])
	elif command == "take":
		if len(args) == 1:
			return t_not_ok("Take what?")

		return MAIN_PLAYER.take(args[1])
	elif command == "use":
		if len(args) == 1:
			return t_not_ok("Use what?")
		
		# valid, technically
		# not using an item on something
		if len(args) == 2:
			return MAIN_PLAYER.use(args[1], None)

		if len(args) <= 3:
			return t_not_ok("With what?")
		
		return MAIN_PLAYER.use(args[1], args[3])
	else:
		quote = INVALID_COMMAND_QUOTES[randint(0, len(INVALID_COMMAND_QUOTES) - 1)]

		return t_not_ok(quote)

while True:
	text = MAIN_PLAYER.prompt("> ").lower()
	args = text.split(" ")

	output = parse(args)
	
	MAIN_PLAYER.display(output)
