
import sys

BACKSPACE = "backspace"
ENTER = "enter"


DELETE = "delete"
ESCAPE = "escape"
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
PAGEUP = "pageup"
PAGEDOWN = "pagedown"
HOME = "home"
END = "end"

BEFORE_LETTERS = ord('A') - 1

def name_char(char):
	n = ord(char)
	if n > 31 and n != 127:
		return char
	if n == 8 or n == 127:
		return BACKSPACE
	if n == 10 or n == 13:
		return ENTER
	if n > 0 and n <= 26:
		return "^" + chr(n + BEFORE_LETTERS)
	return "chr({})".format(n)

def get_key(stream=sys.stdin, combine_escape=True, do_interrupt=False):
	char = stream.read(1)
	if do_interrupt and ord(char) == 3:
		raise KeyboardInterrupt
	if ord(char) == 27:
		if not combine_escape:
			return ESCAPE
		nextchar = stream.read(1)
		while ord(nextchar) == 27: # avoid deep recursion
			nextchar = stream.read(1)
		if nextchar != "[":
			return "\\e" + name_char(nextchar)
		last = stream.read(1)
		rest = last
		while last in "1234567890;=?":
			last = stream.read(1)
			rest += last
		if rest == "A":
			return UP
		elif rest == "B":
			return DOWN
		elif rest == "C":
			return RIGHT
		elif rest == "D":
			return LEFT
		elif rest == "H":
			return HOME
		elif rest == "F":
			return END
		elif rest == "3~":
			return DELETE
		elif rest == "5~":
			return PAGEUP
		elif rest == "6~":
			return PAGEDOWN
		else:
			return "\\e[" + rest
	else:
		return name_char(char)
		
	
