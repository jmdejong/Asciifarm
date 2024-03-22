

import sys
import io

from .constants import INT_INFINITY
from .screen import Screen
from .pad import Pad
from .drawtarget import DrawTarget
from .strwidth import charwidth



class BufferedScreen(DrawTarget):
	
	def __init__(self, out=sys.stdout, *args, **kwargs):
		self.screen = RememberingScreen(out, *args, **kwargs)
		self.buff = Pad(self.screen.width, self.screen.height)
	
	@property
	def width(self):
		return self.screen.width
	
	@property
	def height(self):
		return self.screen.height
	
	def clear(self):
		self.screen.clear()
		self.buff = Pad(self.screen.width, self.screen.height)
	
	def reset(self):
		self.screen.reset()
		self.clear()
	
	def update(self):
		self.screen.draw_pad(self.buff)
		self.screen.update()
	
	def write(self, x, y, text, style=None):
		self.buff.write(x, y, text, style)
	
	def draw_pad(self, pad, dest_x=0, dest_y=0, width=INT_INFINITY, height=INT_INFINITY, src_x=0, src_y=0):
		self.buff.draw_pad(pad, dest_x, dest_y, width, height, src_x, src_y)


class RememberingScreen(DrawTarget):
	
	def __init__(self, out=sys.stdout, *args, **kwargs):
		self.out = out
		self.screen = Screen(io.StringIO(), *args, **kwargs)
		self.on_screen = Pad(self.screen.width, self.screen.height)
		self.style = None
	
	
	@property
	def width(self):
		return self.screen.width
	
	@property
	def height(self):
		return self.screen.height
	
	def clear(self):
		self.on_screen = Pad(self.screen.width, self.screen.height)
		self.screen.clear()
	
	def reset(self):
		self.screen.update_size()
		self.clear()
	
	def update(self):
		self.out.write(self.screen.out.getvalue())
		self.screen.out = io.StringIO()
		self.out.flush()
	
	def write(self, x, y, text, style=None):
		text = crop(text, self.screen.width-x)
		self.on_screen.write(x, y, text, style)
		#self.screen.write(x, y, text, style)
		self.screen.move(x, y)
		self.screen.style(style, self.style)
		self.style = style
		self.screen.addstr(text)
	
	def draw_pad_direct(self, *args, **kwargs):
		self.on_screen.draw_pad(*args, **kwargs)
		self.screen.draw_pad(*args, **kwargs)
		
	
	def draw_pad(self, pad, dest_x=0, dest_y=0, width=INT_INFINITY, height=INT_INFINITY, src_x=0, src_y=0):
		# Optimizes on the amount of characters to write to the terminal, which is more crucial in applications running over a network connection (like ssh)
		# This will only draw the changed characters
		width = min(width, self.screen.width - dest_x, pad.width - src_x)
		height = min(height, self.screen.height - dest_y, pad.height - src_y)
		
		
		BEGIN = "BEGIN" # before anything on the line has been done
		RUNNING = "RUNNING" # while changing current characters
		POSTRUN = "POSTRUN" # after changing some characters. Unsure whether to jump to next place or just continue
		POSTPOSTRUN = "POSTPOSTRUN" # same, but now the style has been changed
		BETWEEN = "BETWEEN" # run finished, but not worth to continue. Looking for the next changes
		for y in range(height):
			#runs = []
			#current_run = None
			running = False
			last_run = None
			post_run = ""
			postpost_run = ""
			post_style = None
			extra = 0
			skip = 0
			
			state = BEGIN
			#self.style = None
			#cursor_x = None
			for x, (buff_cell) in enumerate(pad.get_line(src_x, src_y + y, width)):#zip(
					#self.on_screen.get_line(dest_x, dest_y + y, width),
					#pad.get_line(src_x, src_y + y, width))):
				scr_cell = self.on_screen.get(dest_x + x, dest_y + y)
				if scr_cell is None:
					scr_cell = (None, None)
				scr_style, scr_char = scr_cell
				if buff_cell is None:
					if state == BEGIN:
						continue
					if state == RUNNING:
						cursor_x = x
					skip += 1
					state = BETWEEN
					continue
				buff_style, buff_char = buff_cell
				while True:
				
					if state == BEGIN or state == BETWEEN:
						if scr_cell == buff_cell:
							skip += 1
							break
						# start the first run
						if state == BEGIN:
							skip = 0
							self.screen.move(dest_x + x, dest_y + y)
						#else:
							#self.screen.skip(skip)#x-cursor_x)
							#skip = 0
						state = RUNNING
					
					if state == RUNNING:
						if scr_cell != buff_cell:
							self.screen.skip(skip)
							skip = 0
							# continuing the same run
							self.screen.style(buff_style, self.style)
							self.style = buff_style
							self.screen.addstr(buff_char)
							self.on_screen.set_char(x, y, buff_char, buff_style)
							w = charwidth(buff_char)
							if w == 2:
								skip -= 1
								#self.on_screen.set_char(x + 2, y, None)
								self.on_screen.set_char(x + 1, y, None)
								#self.on_screen.set_char(x, y, None)
							break
						#cursor_x = x #+ char_width(buf_char) - 1
						state = BETWEEN#POSTRUN
						extra = 0
						post_run = ""
						postpost_run = ""
					
					#if state == POSTRUN:
						#if buff_cell != scr_cell:
							#self.screen.skip(skip)
							#skip = 0
							#self.screen.addstr(post_run)
							#state = RUNNING
							#continue
						#elif extra >= 4:
							#skip += extra
							#state = BETWEEN
							#break
						#elif buff_style == self.style:
							#extra += 1
							#post_run += buff_char
							#break
						#else:
							#new_style = buff_style
							#state = POSTPOSTRUN
					
					#if state == POSTPOSTRUN:
						#if buff_style != new_style:
							#state = BETWEEN
							#break
						#if buff_cell != scr_cell:
							#self.screen.addstr(post_run)
							#self.screen.style(new_style, self.style)
							#self.screen.addstr(postpost_run)
							#self.style = new_style
							#state = RUNNING
						#elif extra >= 4:
							#skip += extra
							#state = BETWEEN
							#break
						#else:
							#extra += 1
							#postpost_run += buff_char
							#break
		#self.on_screen.draw_pad(pad, dest_x, dest_y, width, height, src_x, src_y)
