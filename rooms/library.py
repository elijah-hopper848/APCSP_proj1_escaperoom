from math import log2, floor

from utility import ANSI
from utility.positional import positional
from classes import Player, Room, Feature

class LibraryCandles(Feature):
	def __init__(self, code: int) -> None:
		self.count = floor(log2(code)) + 1

		self.current_code = code
		self.code = code

	def is_lit(self, position: int) -> bool:
		return (self.current_code & (1 << position)) != 0
	def light_candle(self, position: int):
		self.current_code |= 1 << position
	def extinguish_candle(self, position: int):
		self.current_code &= ~(1 << position) # don't worry about all of these symbols, i hardly know what they mean either

	def prompt_candle(self, actor: Player, prompt: str) -> tuple[bool, int]:
		choice = actor.prompt(prompt)

		if choice == "stop":
			return (True, 0)
		
		position = 1

		try:
			position = int(choice)
		except:
			actor.display(ANSI.tint_bad("Invalid position."))
			return self.prompt_candle(actor, prompt)

		if position < 1 or position > self.count:
			actor.display(ANSI.tint_bad(f"There is no {position} candle."))
			return self.prompt_candle(actor, prompt)

		return (False, position - 1)

	def use(self, actor: Player, item: str | None) -> str:
		if item == None:
			while True:
				stop, position = self.prompt_candle(actor, "Which candle do you want to extinguish? ('stop' to exit) ")

				if stop:
					return "..."

				print(positional(position + 1))
				self.extinguish_candle(position)
		elif item == "lighter":
			while True:
				stop, position = self.prompt_candle(actor, "Which candle do you want to light? ('stop' to exit) ")

				if stop:
					return "..."
				
				self.light_candle(position)
		
		return "I can't use this here."
	def describe(self) -> str:
		return f"{self.count} candles in a row"
	def examine(self, actor: Player) -> str:
		return "A"

class LibraryBookcase(Feature):
	def __init__(self, code: int) -> None:
		self.code = code

	def describe(self) -> str:
		return "and a bookcase with a singular book on it"
	def examine(self, actor: Player) -> str:
		return str(self.code)

class LibraryRoom(Room):
	description = "You are in a library."
	items = {"lighter": "a \x1b[1mlighter\x1b[22m on a table"}

	def __init__(self) -> None:
		code = 0b1011

		candles = LibraryCandles(code)
		bookcase = LibraryBookcase(code)

		self.features = {
			"candles": candles,
			"bookcase": bookcase,
		}