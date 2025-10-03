from __future__ import annotations # this might not work in cobi lol

import utility.ANSI as ANSI

PROMPT_COLOR = ANSI.YELLOW

class Examinable:
	"""
	Abstract class for an object that can be "examined" by an actor, not to be confused with Describable.
	"""
	def examine(self, actor: Player) -> str:
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
		return "I can't use this here."
class Room(Describable):
	"""
	Rooms contain features and items
	"""
	
	description = "None"
	items: dict[str, str] = {}
	features: dict[str, Feature] = {}

	def describe(self) -> str:
		output = self.description
		output += f" There is {', '.join(self.items.values())}."
	
		list = [feature.describe() for feature in self.features.values()]
		output += f" You see {', '.join(list)}."

		return ANSI.tint16(output, ANSI.BRIGHT_GREEN)

class Player(Describable):
	"""
	Player object that contains player relevant info like items
	
	for some reason i designed this to be able to work with multiplayer
	"""
	
	def __init__(self, init_room: Room) -> None:
		self.inventory = []
		self.current_room = init_room
	
	# methods for actions a player can do
	def examine(self, target: str) -> str:
		if target == "room":
			return f"{self.current_room.describe()}\n{ANSI.tint16(self.describe(), ANSI.CYAN)}"
		else:
			thing = self.current_room.features.get(target)

			if thing == None:
				return f"I can't find '{target}'"
			
			return f"You examine the {target}...\n{thing.examine(self)}"
	def take(self, item: str) -> str:
		if self.has_item(item):
			return ANSI.tint_bad(f"I already have {item}.")
		
		if self.current_room.items.get(item) != None:
			self.give_item(item)
			return f"You take the {item}."
		
		return ANSI.tint_bad(f"I can't take '{item}'")
	def use(self, target: str, item: str | None) -> str:
		feature = self.current_room.features.get(target)

		if feature == None:
			return ANSI.tint_bad(f"I don't see a {target}.")
		
		if item != None and not self.has_item(item):
			return ANSI.tint_bad(f"I don't have any {item}.")
		
		return feature.use(self, item=item)
	
	def change_room(self, new_room: Room):
		self.current_room = new_room
		self.display("You are in a new room...\n" + "-" * 40)

	def has_item(self, item: str) -> bool:
		return self.inventory.count(item) > 0
	def give_item(self, item: str):
		self.inventory.append(item)
	def remove_item(self, item: str):
		self.inventory.remove(item)
	
	def prompt(self, prompt: str) -> str:
		value = input(ANSI.tint16(prompt, PROMPT_COLOR))
		
		print("\x1b[0m", end="")
		
		return value
	def display(self, text: str):
		print(text)
	
	def describe(self) -> str:
		if len(self.inventory) == 0:
			return f"You aren't carrying anything."
		
		return f"You have {','.join(self.inventory)}."