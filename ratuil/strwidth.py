

import unicodedata

# taken from textwrap
_whitespace = '\t\n\x0b\x0c\r '



def charwidth(char):
	""" The width of a single character. Ambiguous width is considered 1"""
	cat = unicodedata.category(char)
	if cat == "Mn":
		return 0
	eaw = unicodedata.east_asian_width(char)
	if eaw == "Na" or eaw == "H":
		return 1
	if eaw == "F" or eaw == "W":
		return 2
	if eaw == "A":
		return 1
	if eaw == "N":
		return 1
	raise Exception("unknown east easian width for character {}: {}".format(ord(char), char))

def strwidth(text):
	""" The total width of a string """
	return sum(charwidth(ch) for ch in text)


def width(text):
	return stringwidth(text)
	
def width_index(text, width):
	""" The largest index i for which the strwidth(text[:i]) <= width """
	l = 0
	for i, char in enumerate(text):
		w = charwidth(char)
		if l + w > width:
			return i
		l += w
	return len(text)
	
def crop(text, width):
	return text[:width_index(text, width)]

def wrap(text, width, separators=None):
	lines = []
	for line in text.splitlines():
		while True:
			cutoff = width_index(line, width)
			if cutoff >= len(line):
				lines.append(line)
				break
			if separators is not None:
				last_sep = max(line.rfind(c, 0, cutoff+1) for c in separators)
				if last_sep > 0:
					cutoff = last_sep
			lines.append(line[:cutoff])
			if separators is not None:
				while line[cutoff] in separators:
					cutoff += 1
			line = line[cutoff:]
	return lines

def wrap_words(text, width):
	return wrap(text, width, separators=_whitespace)

