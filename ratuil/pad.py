
from .constants import INT_INFINITY
from .drawtarget import DrawTarget

from .strwidth import charwidth


class Pad(DrawTarget):
	
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.clear()
	
	def resize(self, width, height):
		self.width = width
		self.height = height
		self.clear()
	
	def fill(self, value):
		self.data = [value for i in range(self.width*self.height)]
	
	def clear(self):
		self.fill(None)
	
	def write(self, x, y, text, style=None):
		if y >= self.height:
			return
		for char in text:
			w = charwidth(char)
			if x + w > self.width:
				break
			self.set_char(x, y, char, style)
			if w == 2:
				self.delete(x + 1, y)
			x += w
			
	
	def set_char(self, x, y, char, style=None):
		self.data[x + y * self.width] = (style, char)
	
	def delete(self, x, y):
		self.data[x + y * self.width] = None
	
	def get(self, x, y):
		if y >= self.height or x >= self.width:
			return None
		return self.data[x + y * self.width]
	
	def get_line(self, x, y, length=None):
		if length is None:
			length = self.width - x
		if x >= self.width:
			return []
		start = x + y * self.width
		return self.data[start:start+length]
	
	def draw_pad(self, src, dest_x=0, dest_y=0, width=INT_INFINITY, height=INT_INFINITY, src_x=0, src_y=0):
		dest = self
		width = min(width, dest.width - dest_x, src.width - src_x)
		height = min(height, dest.height - dest_y, src.height - src_y)
		for y in range(height):
			for x, cell in enumerate(src.get_line(src_x, src_y + y, width)):
				if cell is not None:
					style, char = cell
					self.write(dest_x + x, dest_y + y, char, style)
