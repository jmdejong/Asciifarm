
from .constants import INT_INFINITY

class DrawTarget:
	
	# is actually more of an interface / trait than a useful class
	width = None
	height = None
	
	def clear(self):
		raise NotImplementedError()
	
	def write(self, x, y, text, style=None):
		raise NotImplementedError()
	
	def write_styled(self, x, y, styledtext, extrastyle=None):
		if isinstance(styledtext, str):
			self.write(x, y, styledtext, extrastyle)
			return
		for text, style in styledtext:
			self.write(x, y, text, style.add(extrastyle))
			x += len(text)
		
	
	def draw_pad(self, src, dest_x=0, dest_y=0, width=INT_INFINITY, height=INT_INFINITY, src_x=0, src_y=0):
		raise NotImplementedError()
