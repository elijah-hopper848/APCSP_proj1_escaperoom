from classes import Feature, Room, Player

# Rooms

class CaveDoor(Feature):
	def __init__(self) -> None:
		super().__init__()

		self.is_open = False

	def describe(self) -> str:
		return "and a door near the furnace"

	def examine(self) -> str:
		return self.is_open and "It's open" or "It's closed"

class CaveFurnace(Feature):
	def __init__(self, linked_door: CaveDoor) -> None:
		self.linked_door = linked_door
		self.is_active = False
		self.has_fuel = False

	def ignite(self):
		self.is_active = True
		self.has_fuel = False

		self.linked_door.is_open = True
	
	def extinguish(self):
		self.is_active = False

		self.linked_door.is_open = False

	def use(self, actor: Player, item: str | None) -> str:
		if self.is_active:
			if actor.prompt("Do you want to extinguish the furnace? (y/n) ") == "y":
				self.extinguish()

				return "You extinguish the furnace."

			return "I can't use the furnace while it's burning."

		if item == None:
			if self.has_fuel:
				self.ignite()

				return "You ignite the furnace with the sticks."
			
			return "I can't ignite the furnace without any fuel."
		elif item == "sticks":
			self.has_fuel = True

			actor.inventory.remove("sticks")

			return "You throw the sticks into the furnace."

		return "I can't use this here."

	def describe(self) -> str:
		return "a furnace in the corner of the room"
	
	def examine(self) -> str:
		output = "It's a furnace. It appears to be connected to the door."

		if self.is_active:
			output += " The furnace is burning."
		elif self.has_fuel:
			output += " There are some sticks inside of it."

		return output

class CaveRoom(Room):
	description = "You are in a cave."
	items = {"sticks": "some sticks"}

	def __init__(self) -> None:
		door = CaveDoor()
		furnace = CaveFurnace(door)

		self.features = {
			"furnace": furnace,
			"door": door
		}