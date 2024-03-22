
from . import Widget
from ..pad import Pad

class Field(Widget):
	
	
	def __init__(self, width=0, height=0, char_size=1):
		self.width = width
		self.height = height
		self.char_size = char_size
		self.pad = Pad(self.width * self.char_size, self.height)
		self.center = (0, 0)
		self.redraw = False
	
	def set_char_size(self, char_size):
		self.char_size = char_size
		self.pad = Pad(self.width * self.char_size, self.height)
	
	def set_size(self, width, height):
		self.width = width
		self.height = height
		self.pad.resize(width * self.char_size, height)
		self.redraw = True
		self.change()
	
	def change_cell(self, x, y, char, style=None):
		if x < 0 or y < 0 or x >= self.width or y >= self.height:
			return
		self.pad.write(x * self.char_size, y, char, style)
		self.change()
	
	def set_center(self, x, y):
		self.center = (x, y)
		self.change()
	
	
	def _round_width(self, x):
		return x // self.char_size * self.char_size
	
	def draw(self, target):
		center_x, center_y = self.center
		target.draw_pad(
			self.pad,
			src_x = max(0, min(
				self._round_width(self.pad.width - target.width),
				self._round_width(center_x * self.char_size - target.width // 2)
			)),
			src_y = max(0, min(self.pad.height - target.height, center_y - target.height // 2)),
			width = self._round_width(target.width),
			dest_x = max(0, (target.width - self.pad.width) // 2),
			dest_y = max(0, (target.height - self.pad.height) // 2)
		)
	
	@classmethod
	def from_xml(cls, children, attr, text):
		return cls(char_size=int(attr.get("char-size", 1)))
