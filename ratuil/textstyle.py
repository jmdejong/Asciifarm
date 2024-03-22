class Attr:
	
	RESET = "0"
	BOLD = "1"
	UNDERSCORE = "4"
	BLINK = "5"
	REVERSE = "7"
	CONCEALED = "8"
	
	#FG_BLACK = "30"
	#FG_RED = "31"
	#FG_GREEN = "32"
	#FG_YELLOW = "33"
	#FG_BLUE = "34"
	#FG_MAGENTA = "35"
	#FG_CYAN = "36"
	#FG_WHITE = "37"
	
	#BG_BLACK = "40"
	#BG_RED = "41"
	#BG_GREEN = "42"
	#BG_YELLOW = "43"
	#BG_BLUE = "44"
	#BG_MAGENTA = "45"
	#BG_CYAN = "46"
	#BG_WHITE = "47"
	
	#FG_BRIGHT_BLACK = "90"
	#FG_BRIGHT_RED = "91"
	#FG_BRIGHT_GREEN = "92"
	#FG_BRIGHT_YELLOW = "93"
	#FG_BRIGHT_BLUE = "94"
	#FG_BRIGHT_MAGENTA = "95"
	#FG_BRIGHT_CYAN = "96"
	#FG_BRIGHT_WHITE = "97"
	
	#BG_BRIGHT_BLACK = "100"
	#BG_BRIGHT_RED = "101"
	#BG_BRIGHT_GREEN = "102"
	#BG_BRIGHT_YELLOW = "103"
	#BG_BRIGHT_BLUE = "104"
	#BG_BRIGHT_MAGENTA = "105"
	#BG_BRIGHT_CYAN = "106"
	#BG_BRIGHT_WHITE = "107"
	
	FG_DEFAULT = "39"
	BG_DEFAULT = "49"
	
	FG_COLORS = [str(i) for i in list(range(30, 38)) + list(range(90, 98))]
	BG_COLORS = [str(i) for i in list(range(40, 48)) + list(range(100, 108))]

class TextStyle:
	
	BLACK = 0
	RED = 1
	GREEN = 2
	YELLOW = 3
	BLUE = 4
	MAGENTA = 5
	CYAN = 6
	WHITE = 7
	
	BRIGHT_BLACK = 8
	BRIGHT_RED = 9
	BRIGHT_GREEN = 10
	BRIGHT_YELLOW = 11
	BRIGHT_BLUE = 12
	BRIGHT_MAGENTA = 13
	BRIGHT_CYAN = 14
	BRIGHT_WHITE = 15
	
	COLORS = list(range(16))
	
	BOLD = "bold"
	REVERSE = "reverse"
	UNDERSCORE = "underscore"
	BLINK = "blink"
	
	ATTRIBUTES = [BOLD, REVERSE, UNDERSCORE]
	
	def __init__(self, fg=None, bg=None, bold=False, reverse=False, underscore=False):
		self.fg = fg
		self.bg = bg
		self.attr = {
			self.BOLD: bold,
			self.REVERSE: reverse,
			self.UNDERSCORE: underscore
		}
		self.attr_set = frozenset(key for key, value in self.attr.items() if value)
	
	def __eq__(self, other):
		return isinstance(other, TextStyle) and other.fg == self.fg and other.bg == self.bg and self.attr_set == other.attr_set
	
	def __repr__(self):
		if self == self.default:
			return "TextStyle()"
		return "TextStyle({}, {}, {})".format(self.fg, self.bg, ", ".join(self.attr.values()))
	
	def add(self, other):
		if other is None:
			other = TextStyle()
		fg = self.fg
		if other.fg is not None:
			fg = other.fg
		bg = self.bg
		if other.bg is not None:
			bg = other.bg
		attrs = dict(self.attr)
		for key, val in other.attr.items():
			if val:
				attrs[key] = val
		return TextStyle(fg, bg, **attrs)
	
	@property
	def bold(self):
		return self.attr[self.BOLD]
	
	@property
	def underscore(self):
		return self.attr[self.UNDERSCORE]
	
	@property
	def reverse(self):
		return self.attr[self.REVERSE]
	
	@classmethod
	def from_str(cls, text):
		if text is None:
			return TextStyle.default
		fg = None
		bg = None
		attrs = {}
		parts = text.split(";")
		for part in parts:
			attr, _sep, value = part.partition(":")
			attr = attr.strip().casefold()
			value = value.strip()
			if attr == "fg" and int(value) in TextStyle.COLORS:
				fg = int(value)
			if attr == "bg" and int(value) in TextStyle.COLORS:
				bg = int(value)
			if attr in TextStyle.ATTRIBUTES:
				attrs[attr] = True
		return cls(fg, bg, **attrs)
	

TextStyle.default = TextStyle()
