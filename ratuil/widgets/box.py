
from . import Widget

class Box(Widget):
	
	# doesn't do anything
	# This is useful when you want to separate attributes
	
	def __init__(self, child):
		self.child = child
	
	def resize(self, target):
		self.child.resize(target)
	
	def update(self, target, force=False):
		return self.child.update(force)

	@classmethod
	def from_xml(cls, children, attr, text):
		assert len(children) == 1
		return cls(children[0])
	
