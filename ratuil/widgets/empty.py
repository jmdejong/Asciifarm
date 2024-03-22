
from . import Widget

class Empty(Widget):
	
	# just some empty transparent space
	
	def resize(self, target):
		pass
	
	def update(self, target, force=False):
		return False

	@classmethod
	def from_xml(cls, children, attr, text):
		return Empty()
	
