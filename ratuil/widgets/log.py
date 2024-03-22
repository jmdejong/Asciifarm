
from . import Widget
from ..strwidth import wrap

class Log(Widget):
	
	def __init__(self, messages=None):
		self.messages = list(messages or [])
		self.scrolled_back = 0
	
	def add_message(self, message, style=None):
		self.messages.append((message, style))
		if self.scrolled_back:
			self.scrolled_back += 1
		self.change()
	
	def scroll(self, amount, relative=True):
		if relative:
			self.scrolled_back += amount
		else:
			self.scrolled_back = amount
		self.scrolled_back = max(self.scrolled_back, 0)
		self.change()
	
	
	
	def draw(self, target):
		width = target.width
		height = target.height
		lines = []
		messages = self.messages
		for message, style in messages:
			for line in wrap(message, width):
				lines.append((line, style))
		self.scrolled_back = max(min(self.scrolled_back, len(lines)-height), 0)
		moreDown = False
		if self.scrolled_back > 0:
			lines = lines[:-self.scrolled_back]
			moreDown = True
		moreUp = False
		if len(lines) > height:
			moreUp = True
			lines = lines[len(lines)-height:]
		elif len(lines) < height:
			lines = (height-len(lines)) * [("",)] + lines
		target.clear()
		for i, line in enumerate(lines):
			target.write(0, i, *line)
		if moreUp:
			target.write(width-1, 0, '-')
		if moreDown:
			target.write(width-1, height-1, '+')
	
	@classmethod
	def from_xml(cls, children, attr, text):
		if text is not None:
			messages = [(line.strip(), None) for line in text.splitlines() if line.strip()]
			return cls(messages)
		else:
			return cls()
