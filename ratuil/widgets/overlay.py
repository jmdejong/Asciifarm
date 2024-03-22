
from . import Widget
from ..window import Window

class Overlay(Widget):
	
	def __init__(self, children):
		self.children = children
	
	def _get_child(self, index):
		if isinstance(index, int):
			return self.children(index)
		if isinstance(index, str):
			key = index.casefold()
			for i, child in enumerate(self.children):
				if child.key == key:
					return child
	
	def hide(self, index):
		self._get_child(index).hide()
		self.change()
	
	def show(self, index):
		self._get_child(index).show()
		self.change()
	
	def resize(self, target):
		for child in self.children:
			x = child.style.get_offset_x(target.width)
			y = child.style.get_offset_y(target.height)
			width = min(child.style.get_width(target.width), target.width - x)
			height = min(child.style.get_height(target.height), target.height - y)
			if child.style.align_right:
				x = target.width - x - width
			if child.style.align_bottom:
				y = target.height - y - height
			win = Window(target, x, y, width, height)
			child.resize(win)
	
	def update(self, target, force):
		if self.is_changed():
			force = True
			self.unchange()
		children = [child for child in self.children if not child.hidden]
		if not children:
			return False
		#child[0].update(force)
		for child in self.children:
			# if any child is changed, all next children get forced updates
			force = child.update(force) or force
		#self.children[self.selected].update(force)
		return force
	
	
	@classmethod
	def from_xml(cls, children, attr, text):
		return cls(children)
