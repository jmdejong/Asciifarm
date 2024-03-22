

from enum import Enum

def clamp(x, lower, upper):
	return min(max(x, lower), upper)

class Relativity(Enum):
	ABSOLUTE = 0
	RELATIVE = 1
	VERY_RELATIVE = 2

class Value:
	
	
	def __init__(self, val=0, relative=Relativity.ABSOLUTE):
		self.val = val
		self.relative = relative
	
	def to_actual_value(self, available_size, remaining_size=None):
		if remaining_size is None:
			remaining_size = available_size
		value = self.val
		if self.relative == Relativity.VERY_RELATIVE:
			value *= remaining_size
		elif self.relative == Relativity.RELATIVE:
			value *= available_size
		return int(value)
	
	@classmethod
	def parse(self, text):
		if text is None:
			return None
		text = str(text) # in case someone would enter a number
		text = "".join(text.split()) # remove whitespace
		if not text:
			return None
		relative = Relativity.ABSOLUTE
		modifier = 1
		if text[-1] == "/":
			relative = Relativity.RELATIVE
			text = text[:-1]
			if text[-1] == "/":
				relative = Relativity.VERY_RELATIVE
				text = text[:-1]
		elif text[-1] == "%":
			relative = Relativity.RELATIVE
			text = text[:-1]
			modifier = 0.01
			if text[-1] == "%":
				relative = Relativity.VERY_RELATIVE
				text = text[:-1]
		if not text:
			return None
		if '.' in text:
			val = float(text)
		else:
			val = int(text)
		return Value(val * modifier, relative)


class BoxStyle():
	
	LEFT = "left"
	RIGHT = "right"
	TOP = "top"
	BOTTOM = "bottom"
	
	def __init__(self, width=None, height=None, offset_x=None, offset_y=None, align_right=False, align_bottom=False, granularity=1, min_width=None, min_height=None, max_width=None, max_height=None):
		self.width = width or Value(1, Relativity.RELATIVE)
		self.height = height or Value(1, Relativity.RELATIVE)
		self.min_width = min_width or Value(0)
		self.min_height = min_height or Value(0)
		self.max_width = max_width or Value(1, Relativity.RELATIVE)
		self.max_height = max_height or Value(1, Relativity.RELATIVE)
		self.offset_x = offset_x or Value(0)
		self.offset_y = offset_y or Value(0)
		self.granularity = granularity
		self.align_right = align_right
		self.align_bottom = align_bottom
	
	def get_width(self, available, remaining=None):
		return clamp(
			self.width.to_actual_value(available, remaining),
			self.min_width.to_actual_value(available, remaining),
			self.max_width.to_actual_value(available, remaining)
		)
	
	def get_height(self, available, remaining=None):
		return clamp(
			self.height.to_actual_value(available, remaining),
			self.min_height.to_actual_value(available, remaining),
			self.max_height.to_actual_value(available, remaining)
		)
	
	def get_offset_x(self, available, remaining=None):
		return self.offset_x.to_actual_value(available, remaining)
	
	def get_offset_y(self, available, remaining=None):
		return self.offset_y.to_actual_value(available, remaining)
	
	
	@classmethod
	def from_attrs(cls, attrs):
		width = Value.parse(attrs.get("width"))
		height = Value.parse(attrs.get("height"))
		min_width = Value.parse(attrs.get("min-width"))
		min_height = Value.parse(attrs.get("min-height"))
		max_width = Value.parse(attrs.get("max-width"))
		max_height = Value.parse(attrs.get("max-height"))
		offset_x = Value.parse(attrs.get("offset-x"))
		offset_y = Value.parse(attrs.get("offset-y"))
		granularity = int(attrs.get("granularity", "1"))
		align_right = ("right" in attrs.get("align", "").casefold() or "right" in attrs.get("hor-align", "").casefold())
		align_bottom = ("bottom" in attrs.get("align", "").casefold() or "bottom" in attrs.get("vert-align", "").casefold())
		return cls(
			width = width, 
			height = height, 
			offset_x = offset_x, 
			offset_y = offset_y,
			align_right = align_right,
			align_bottom = align_bottom,
			granularity = granularity,
			min_width = min_width,
			min_height = min_height,
			max_width = max_width,
			max_height = max_height
		)
