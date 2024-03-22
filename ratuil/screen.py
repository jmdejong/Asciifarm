
import sys
import shutil

from .constants import INT_INFINITY
from .drawtarget import DrawTarget
from .textstyle import TextStyle
from .strwidth import charwidth


class Attr:
	
	RESET = "0"
	BOLD = "1"
	UNDERSCORE = "4"
	BLINK = "5"
	REVERSE = "7"
	CONCEALED = "8"
	
	
	FG_DEFAULT = "39"
	BG_DEFAULT = "49"
	
	FG_COLORS = [str(i) for i in list(range(30, 38)) + list(range(90, 98))]
	BG_COLORS = [str(i) for i in list(range(40, 48)) + list(range(100, 108))]
	
	ATTRS = {
		TextStyle.BOLD: BOLD,
		TextStyle.REVERSE: REVERSE,
		TextStyle.UNDERSCORE: UNDERSCORE,
		TextStyle.BLINK: BLINK
	}

class Screen(DrawTarget):
	
	
	def __init__(self, out=sys.stdout, always_reset=False, blink_bright_background=False):
		self.out = out
		self.width = 0
		self.height = 0
		self.blink_bright_background = blink_bright_background # use the blink attribute for bright backgrounds
		self.always_reset = always_reset or blink_bright_background # always reset if the style is different than the previous one
		self.update_size()
	
	def update_size(self):
		size = shutil.get_terminal_size()
		self.width = size.columns
		self.height = size.lines
	
	def move(self, x, y):
		self.out.write("\033[{};{}f".format(y+1, x+1))
	
	def addstr(self, text):
		self.out.write(text)
	
	def style(self, style, previous=None):
		if style is None:
			style = TextStyle.default
		if style == previous:
			return
		parts = []
		reset = False
		if style.fg is None or style.bg is None or previous is None or previous != style and self.always_reset:
			parts.append(Attr.RESET)
			reset = True
		else :
			for attr, enabled in style.attr.items():
				if not enabled and previous.attr[attr]:
					parts.append(Attr.RESET)
					reset = True
		if style.fg is not None and (reset or style.fg != previous.fg):
			parts.append(Attr.FG_COLORS[style.fg])
		if style.bg is not None and (reset or style.bg != previous.bg):
			parts.append(Attr.BG_COLORS[style.bg])
			if style.bg > 7 and self.blink_bright_background:
				parts.append(Attr.BLINK)
		for attr, enabled in style.attr.items():
			if enabled and (reset or not previous.attr[attr]):
				parts.append(Attr.ATTRS[attr])
		ansistyle = "\033[" + ";".join(parts) + "m"
		self.out.write(ansistyle)
	
	def write(self, x, y, text, style=None):
		self.move(x, y)
		self.style(style)
		self.addstr(text)
	
	def clear(self):
		self.out.write("\033[0m\033[2J")
	
	def clear_line(self):
		self.out.write("\033[K")
	
	def skip(self, amount=1):
		if amount == 0:
			return
		if amount == 1:
			stramount = ""
		else:
			stramount = str(abs(amount))
		self.out.write("\033[{}{}".format(stramount, ("C" if amount >= 0 else "D")))
	
	def draw_pad(self, pad, scr_x=0, scr_y=0, width=INT_INFINITY, height=INT_INFINITY, pad_x=0, pad_y=0):
		screen = self
		width = min(width, screen.width - scr_x, pad.width - pad_x)
		height = min(height, screen.height - scr_y, pad.height - pad_y)
		last_style = None
		for y in range(height):
			screen.move(scr_x, scr_y+y)
			skip = 0
			line_y = pad_y + y
			for cell in pad.get_line(pad_x, line_y, width):
				if cell is None:
					skip += 1
					continue
				if skip != 0:
					screen.skip(skip)
					skip = 0
				style, char = cell
				screen.style(style, last_style)
				last_style = style
				screen.addstr(char)
				skip += 1 - charwidth(char)
	
	def hide_cursor(self):
		self.out.write("\033[?25l")
		
	def show_cursor(self):
		self.out.write("\033[?25h")
	
	def finalize(self):
		self.style(None)
		self.move(0, self.height - 1)
		self.show_cursor()
		self.out.flush()
	
	def update(self):
		self.out.flush()
	

Screen.default = Screen()
