def suffix(num: int) -> str:
	t = str(num)

	if t.endswith("1") and num != 11:
		return "st"
	elif t.endswith("2") and num != 12:
		return "nd"
	elif t.endswith("3") and num != 13:
		return "rd"
	else:
		return "th"

def positional(num: int) -> str:
	return str(num) + suffix(num)