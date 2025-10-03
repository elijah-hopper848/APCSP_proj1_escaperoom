BLACK = 30
RED = 31
GREEN = 32
YELLOW = 33
BLUE = 34
MAGENTA = 35
CYAN = 36
WHITE = 37

BRIGHT_BLACK = 90
BRIGHT_RED = 91
BRIGHT_GREEN = 92
BRIGHT_YELLOW = 93
BRIGHT_BLUE = 94
BRIGHT_MAGENTA = 95
BRIGHT_CYAN = 96
BRIGHT_WHITE = 97

def tint16(text: str, color: int, bg: bool = False) -> str:
	if bg:
		color += 10
	
	return f"\x1b[{color}m{text}\x1b[0m"

# great name i know
def tint_bad(text: str) -> str:
	return tint16(text, BRIGHT_RED)