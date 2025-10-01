from __future__ import annotations # this might not work in cobi lol

class Examinable:
	"""
	Abstract class for an object that can be "examined", not to be confused with Describable.
	"""
	def examine(self) -> str:
		return "MISSING EXAMINE DESCRIPTION"
class Describable:
	"""
	Abstract class for an object that has a description that will be displayed when examining a room.
	"""
	def describe(self) -> str:
		return "MISSING DESCRIPTION"

class Feature(Describable, Examinable):
	"""
	Features are interactive, you can "use" them, optionally with an item.
	"""

	def use(self, actor: Player, item: str | None) -> str:
		...
class Room(Describable):
	"""
	Rooms contain features and items
	"""
	description = "None"
	items: dict[str, str] = {}
	features: dict[str, Feature] = {}

	def describe(self) -> str:
		output = self.description

		list = [self.items[key] for key in self.items]
		output += f" There are {', '.join(list)}."
	
		list = [self.features[key].describe() for key in self.features]
		output += f" You see {', '.join(list)}."

		return output

class Player(Describable):
	def __init__(self, init_room: Room) -> None:
		self.inventory = []
		self.current_room = init_room
	
	# methods for actions a player can do
	def examine(self, target: str) -> str:
		if target == "room":
			return f"{self.current_room.describe()}\n{self.describe()}"
		else:
			thing = self.current_room.features.get(target)

			if thing == None:
				return f"I can't find '{target}'"
			
			return f"You examine the {target}...\n{thing.examine()}"
		
	def take(self, item: str) -> str:
		if self.inventory.count(item) > 0:
			return f"I already have {item}."
		
		if self.current_room.items.get(item) != None:
			self.inventory.append(item)
			return f"You take the {item}."
		
		return f"There is no '{item}'"
	
	def use(self, target: str, item: str | None) -> str:
		feature = self.current_room.features.get(target)

		if feature == None:
			return f"I don't see a {target}."
		
		if item != None and self.inventory.count(item) == 0:
			return f"I don't have any {item}."
		
		return feature.use(self, item=item)

	def prompt(self, prompt: str) -> str:
		return input(prompt)

	def describe(self) -> str:
		return f"You have {','.join(self.inventory)}."