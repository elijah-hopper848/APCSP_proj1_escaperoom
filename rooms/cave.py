from classes import Feature, Room, Player
from utility.ANSI import tint_bad

TARGET_FUEL_LEVEL = 3

class CaveDoor(Feature):
	def __init__(self, next_room: Room) -> None:
		super().__init__()

		self.next_room = next_room
		self.is_locked = True

	def use(self, actor: Player, item: str | None):
		if item != None:
			return tint_bad("I can't use this here.")
		
		if self.is_locked:
			return tint_bad("The door doesn't budge.")
		
		actor.change_room(self.next_room)

		return actor.examine("room")

	def describe(self) -> str:
		return "and a door near the furnace"
	def examine(self, actor: Player) -> str:
		output = "It's a heavy wooden door."

		if self.is_locked:
			output += " It doesn't budge."

		return output
class CaveFurnace(Feature):
	def __init__(self, linked_door: CaveDoor) -> None:
		self.is_burning = False
		self.fuel_level = 0
		
		self.linked_door = linked_door

	def ignite(self):
		# it'd be funny if there was an condition for putting like way too many planks in the furnace
		
		self.is_burning = True
		
		self.linked_door.is_locked = self.fuel_level < TARGET_FUEL_LEVEL
	def extinguish(self):
		self.is_burning = False
		self.fuel_level = 0
		
		self.linked_door.is_locked = True

	def use(self, actor: Player, item: str | None) -> str:
		if self.is_burning:
			if actor.prompt("Do you want to extinguish the furnace? (y/n) ") == "y":
				self.extinguish()

				return "You extinguish the furnace."

			return tint_bad("I can't use the furnace while it's lit, I'll get burnt!")

		if item == None:
			if actor.prompt("Do you want to ignite the furnace? (y/n) ") != "y":
				return "You decided to not ignite the furnace."
			
			if self.fuel_level > 0:
				self.ignite()

				output = "You ignite the furnace with the planks of wood."

				if self.fuel_level >= TARGET_FUEL_LEVEL:
					output += " You hear the door click..."
				else:
					output += " Nothing happened..."

				return output
			
			return tint_bad("I can't ignite the furnace without any fuel inside it.")
		elif item == "wood":
			self.fuel_level += 1

			actor.remove_item("wood")

			return "You place the planks inside the furnace."

		return tint_bad("I can't use this here.")

	def describe(self) -> str:
		return "a furnace in the corner of the room"
	def examine(self, actor: Player) -> str:
		output = "It's a furnace. It appears to be connected to a door."
	
		fuel_level = self.fuel_level
	
		if self.is_burning:
			output += " The furnace is burning."
			
			if fuel_level == 1:
				output += " It's warm. The gauge is at 30%"
			elif fuel_level == 2:
				output += " It's hot. The gauge is at 67%"
			elif fuel_level >= 3:
				output += " It's searing hot. The gauge is at 100%"
		else:
			output += " The gauge is at 0%."
			
			if fuel_level == 1:
				output += " There are a few planks inside of it."
			elif fuel_level == 2:
				output += " There are some planks inside of it."
			elif fuel_level >= 3:
				output += " There are a lot of planks inside of it."
			elif actor.has_item("wood"): # very subtle hint, i know
				output += " These planks could be used as fuel..."

		return output

class CaveRoom(Room):
	description = "You are in a cave."
	items = {"wood": "a couple planks of \x1b[1mwood\x1b[22m"}

	def __init__(self, next_room: Room) -> None:
		door = CaveDoor(next_room)
		furnace = CaveFurnace(door)

		self.features = {
			"furnace": furnace,
			"door": door
		}