from math import log2, floor
from random import randint

from utility import ANSI
from utility.positional import positional
from classes import Player, Room, Feature

class LibraryCandles(Feature):
	def __init__(self, room: Room, code: int) -> None:
		super().__init__(room)

		self.count = floor(log2(code)) + 1

		self.current_code = 0
		self.code = code

	def on_change(self, actor: Player):
		if self.current_code == self.code:
			actor.display(ANSI.tint16("Congratulations, you solved the final puzzle!\nI didn't do 3 puzzles because im lazy and also because this is starting to get boring so this is all youre getting lol.\nfeel free to use this as an example of what not to do", ANSI.BRIGHT_MAGENTA))
			actor.exit()

	def is_lit(self, position: int) -> bool:
		return (self.current_code & (1 << position)) != 0
	def light_candle(self, actor: Player, position: int):
		self.current_code |= 1 << position

		self.on_change(actor)
	def extinguish_candle(self, actor: Player, position: int):
		self.current_code &= ~(1 << position) # don't worry about all of these symbols, i hardly know what they mean either

		self.on_change(actor)

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
			actor.display(ANSI.tint_bad(f"There is no {positional(position)} candle."))
			return self.prompt_candle(actor, prompt)

		return (False, position - 1)

	def use(self, actor: Player, item: str | None) -> str:
		if item == None:
			while True:
				stop, position = self.prompt_candle(actor, "Which candle do you want to extinguish? ('stop' to exit) ")

				if stop:
					return self.examine(actor)

				if not self.is_lit(position):
					actor.display(ANSI.tint_bad("Candle is already extinguished."))
					continue
				
				self.extinguish_candle(actor, position)
		elif item == "lighter":
			while True:
				stop, position = self.prompt_candle(actor, "Which candle do you want to light? ('stop' to exit) ")

				if stop:
					return self.examine(actor)
				
				if self.is_lit(position):
					actor.display(ANSI.tint_bad("Candle is already lit."))
					continue

				self.light_candle(actor, position)
		
		return "I can't use this here."
	def describe(self) -> str:
		return f"{self.count} candles in a row"
	def examine(self, actor: Player) -> str:
		on_candles = [str(x + 1) for x in range(self.count) if self.is_lit(x)]

		output = f"There's a row of {self.count} candles.\n"

		if len(on_candles) == 0:
			output += "No candles are lit."
		else:
			output += f"Candle(s) {', '.join(on_candles)} are lit."

		return output

class LibraryBookcase(Feature):
	def __init__(self, room: Room, code: int) -> None:
		super().__init__(room)

		self.code = code

	def describe(self) -> str:
		return "and a bookcase with a singular book on it"
	def examine(self, actor: Player) -> str:
		return f"As you flip through the pages in the book you notice that all but one page, page {ANSI.tint16(str(self.code), ANSI.BRIGHT_CYAN)}, are empty.\nThe page that isn't empty contains the phrase {ANSI.tint16('"Base 2"', ANSI.BRIGHT_CYAN)}."

class LibraryRoom(Room):
	description = "You are in a library."
	items = {"lighter": "a \x1b[1mlighter\x1b[22m on a table"}

	def __init__(self) -> None:
		room_code = randint(0b10, 0b11111)

		candles = LibraryCandles(self, room_code)
		bookcase = LibraryBookcase(self, room_code)

		self.features = {
			"candles": candles,
			"bookcase": bookcase,
		}