
from .constants import INT_INFINITY
from .drawtarget import DrawTarget
from .strwidth import crop

class Window(DrawTarget):
	
	def __init__(self, target, x=0, y=0, width=None, height=None):
		self.target = target
		self.x = x
		self.y = y
		self.width = width if width is not None else target.width - x
		self.height = height if height is not None else target.height - y
	
	def write(self, x, y, text, style=None):
		if x < 0 or y < 0 or y >= self.height:
			raise IndexError("Trying to write outside window")
		text = crop(text, self.width - x)
		self.target.write(self.x + x, self.y + y, text, style)
	
	def clear(self):
		for y in range(self.height):
			self.write(0, y, " " * self.width)
	
	def draw_pad(self, pad, dest_x=0, dest_y=0, width=INT_INFINITY, height=INT_INFINITY, src_x=0, src_y=0):
		if dest_x < 0 or dest_y < 0:
			raise IndexError("Trying to draw pad outside window")
		width = min(width, self.width - dest_x)
		height = min(height, self.height - dest_y)
		self.target.draw_pad(pad, self.x + dest_x, self.y + dest_y, width, height, src_x, src_y)
		
