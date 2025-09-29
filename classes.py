class Examinable:
	"""
	Abstract class for an object that can be "examined", not to be confused with Describable.
	"""
	examine_description = "MISSING EXAMINE DESCRIPTION"

	def examine(self) -> str:
		return self.examine_description
class Describable:
	"""
	Abstract class for an object that has a description that will be displayed when examining a room.
	"""
	description = "MISSING DESCRIPTION"

	def describe(self) -> str:
		return self.description

class Feature(Describable, Examinable):
	"""
	Features are interactive, you can "use" them, optionally with an item.
	"""

	def use(self, item: str) -> str:
		...
class Room(Describable):
	"""
	Rooms contain features and items
	"""
	items: dict[str, str] = {}
	features: dict[str, Feature] = {}

	def describe(self) -> str:
		output = self.description

		list = [self.items[key] for key in self.items]
		output += f" There are {', '.join(list)}."
	
		list = [self.features[key].description for key in self.features]
		output += f" You see {', '.join(list)}."

		return output