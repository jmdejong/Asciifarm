
from . import Widget
from .. textstyle import TextStyle
from ..strwidth import strwidth

class Bar(Widget):
	""" A bar (healthbar/mana bar/nutrition bar etc) that can be filled, empty, or something in between)"""
	
	def __init__(self, attr):
		self.full_char = attr.get("full-char", "#")
		self.empty_char = attr.get("empty-char", " ")
		assert strwidth(self.full_char) == strwidth(self.empty_char) == 1
		self.full_style = TextStyle.from_str(attr.get("full-style", ""))
		self.empty_style = TextStyle.from_str(attr.get("empty-style", ""))
		self.total = int(attr.get("total", "-1"))
		self.filled = int(attr.get("filled", "0"))
		
	
	def set_total(self, total):
		self.total = total
		self.change()
	
	def set_filled(self, filled):
		self.filled = filled
		self.change()
	
	def draw(self, target):
		target.clear()
		width = target.width
		height = target.height
		
		bar_end = round(self.filled / self.total * width) if self.total > 0 else 0
		for y in range(target.height):
			target.write(0, y, self.full_char * bar_end , self.full_style)
			target.write(bar_end, y, self.empty_char[0]*(width - bar_end), self.empty_style)
	
	@classmethod
	def from_xml(cls, children, attr, text):
		return cls(attr)
	
