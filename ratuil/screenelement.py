
from .boxstyle import BoxStyle

class ScreenElement:
	
	def __init__(self, widget, attr):
		self.widget = widget
		self.style = BoxStyle.from_attrs(attr)
		self.id = attr.get("id")
		self.key = attr.get("key")
		self.hidden = bool(attr.get("hidden", False))
	
	def hide(self):
		self.hidden = True
	
	def show(self):
		self.hidden = False
	
	def resize(self, target):
		if target is not None and (target.width <= 0 or target.height <= 0):
			target = None
		self.target = target
		self.widget.resize(target)
	
	def update(self, force):
		if self.target and not self.hidden:
			return self.widget.update(self.target, force)
		return False
