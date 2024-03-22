
from . import Widget

class SwitchBox(Widget):
	
	def __init__(self, children, selected=0):
		self.children = children
		self.select(selected)
	
	def select(self, selected):
		if isinstance(selected, str):
			key = selected.casefold()
			for i, child in enumerate(self.children):
				if child.key == key:
					selected = i
					break
		self.selected = selected
		self.change()
	
	def resize(self, target):
		for child in self.children:
			child.resize(target)
	
	def update(self, target, force):
		if self.is_changed():
			force = True
			self.unchange()
		return self.children[self.selected].update(force) or force
	
	
	@classmethod
	def from_xml(cls, children, attr, text):
		return cls(children, attr.get("selected", int(attr.get("selected-val", 0))))
