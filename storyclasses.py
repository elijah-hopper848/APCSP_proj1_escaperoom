from classes import Feature, Room

# Rooms

class CaveFurnace(Feature):
	description = "a furnace in the corner of the room"
	examine_description = "It's a furnace. It appears to be connected to the door somehow."

class CaveDoor(Feature):
	description = "and a door near the furnace"

	def __init__(self) -> None:
		super().__init__()

		self.is_open = False

	def examine(self) -> str:
		return self.is_open and "It's open" or "It's closed"

class CaveRoom(Room):
	description = "You are in a cave."
	items = {"sticks": "some sticks"}
	features = {"furnace": CaveFurnace(), "door": CaveDoor()}