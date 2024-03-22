



class Widget:
	
	_changed = True
	
	def change(self):
		self._changed = True
	
	def is_changed(self):
		return self._changed
	
	def unchange(self):
		self._changed = False
	
	def resize(self, screen):
		self.change()
	
	def update(self, target, force=False):
		""" draw the widget onto target.
		if force is false and the widget did not change since the previous update, don't do anything
		return whether anything was drawn
		"""
		if self.is_changed() or force:
			self.draw(target)
			self.unchange()
			return True
		return False
	
	@classmethod
	def from_xml(cls, children, attr, text):
		raise NotImplementedError
