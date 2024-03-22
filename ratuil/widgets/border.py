
from . import Widget
from ..window import Window
from ..textstyle import TextStyle
from ..strwidth import strwidth

class Border(Widget):
	
	
	def __init__(self, child, attr):
		self.child = child
		self.vertchar = "|"
		self.horchar = "-"
		self.cornerchar = "+"
		self.style = TextStyle.from_str(attr.get("style"))
		char = attr.get("char")
		if char is not None:
			self.vertchar = char
			self.horchar = char
			self.cornerchar = char
		self.vertchar = attr.get("vertchar", self.vertchar)
		self.horchar = attr.get("horchar", self.horchar)
		self.cornerchar = attr.get("cornerchar", self.cornerchar)
		assert strwidth(self.horchar) == 1
		assert strwidth(self.vertchar) == 1
		assert strwidth(self.cornerchar) == 1
	
	def resize(self, target):
		if target is None:
			self.child.resize(None)
		else:
			win = Window(target, 1, 1, target.width - 2, target.height - 2)
			self.child.resize(win)
			self.change()
	
	def update(self, target, force=False):
		if self.is_changed() or force:
			self.draw(target)
			force = True
			self.unchange()
		return self.child.update(force) or force
		
	def draw(self, target):
		target.write(0, 0, self.cornerchar + self.horchar * (target.width - 2) + self.cornerchar, self.style)
		target.write(0, target.height - 1, self.cornerchar + self.horchar * (target.width - 2) + self.cornerchar, self.style)
		for y in range(1, target.height - 1):
			target.write(0, y, self.vertchar, self.style)
			target.write(target.width-1, y, self.vertchar, self.style)

	@classmethod
	def from_xml(cls, children, attr, text):
		assert len(children) == 1
		return cls(children[0], attr)
	
