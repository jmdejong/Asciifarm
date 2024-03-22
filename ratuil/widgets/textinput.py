
from . import Widget
from ..textstyle import TextStyle
from ..strwidth import strwidth, width_index

class TextInput(Widget):
	
	def __init__(self):
		self.text = ""
		self.cursor = None

	def set_text(self, text, cursor=None):
		self.text = text
		if cursor is not None:
			assert cursor >= 0
		self.cursor = cursor
		self.change()
	
	def draw(self, target):
		target.clear()
		if self.cursor is None:
			target.write(0, 0, self.text)
		else:
			text = self.text
			cursor_pos = strwidth(self.text[:self.cursor])
			textwidth = strwidth(self.text)
			
			offset = max(0, cursor_pos - target.width * 0.9)
			
			chars_offset = width_index(text, offset)
			offset_text = self.text[chars_offset:]
			target.write(0, 0, offset_text)
			
			if self.cursor < len(self.text):
				c = self.text[self.cursor]
			else:
				c = ' '
			target.write(cursor_pos - strwidth(self.text[:chars_offset]), 0, c, TextStyle(reverse=True))
	
	@classmethod
	def from_xml(cls, children, attr, text):
		return cls()
