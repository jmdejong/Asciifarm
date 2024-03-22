
from . import Widget
from ..strwidth import crop, wrap, wrap_words
from ..textstyle import TextStyle
from collections import defaultdict

class TextBox(Widget):
	
	def __init__(self, text="", wrap=None, use_format=False, style=None):
		self.lines = []
		if wrap is None or wrap == "":
			wrap = "crop"
		assert wrap in {"crop", "words", "chars"}
		self.wrap = wrap
		self.use_format = use_format
		self.set_text(text, None)
	
	def set_text(self, text, style=None):
		self.text = text
		self.style = style
		if self.use_format:
			self.format(defaultdict(str))
		else:
			self.lines = text.splitlines()
		self.change()
	
	def format(self, values):
		self.lines = self.text.format_map(values).splitlines()
		self.change()
	
	def draw(self, target):
		target.clear()
		lines = []
		if self.wrap == "crop":
			lines = [crop(line, target.width) for line in self.lines][:target.height]
		elif self.wrap == "chars":
			for line in self.lines:
				lines.extend(wrap(line, target.width))
		elif self.wrap == "words":
			for line in self.lines:
				lines.extend(wrap_words(line, target.width))
		
		for y, line in enumerate(lines[:target.height]):
			target.write(0, y, line, self.style)
	
	@classmethod
	def from_xml(cls, children, attr, text):
		wrap = attr.get("wrap")
		use_format = bool(attr.get("format"))
		return cls((text or "").strip(), wrap, use_format, TextStyle.from_str(attr.get("style", "")))
