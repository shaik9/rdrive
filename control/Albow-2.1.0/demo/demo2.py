###############################################################################
#
#   Albow - Demonstration
#
###############################################################################

screen_size = (640, 480)
flags = 0
frame_time = 50 # ms

import os, sys
from os.path import dirname as d
sys.path.insert(1, d(d(os.path.abspath(sys.argv[0]))))

import pygame
pygame.init()
from pygame.color import Color
from pygame.locals import *
from pygame.event import *
from pygame.key import *

from math import pi
from albow.widget import Widget
from albow.controls import Label, Button, Image, AttrRef, \
	RadioButton, ValueDisplay, ProgressBar
from albow.layout import Row, Column, Grid
from albow.fields import TextField, FloatField
from albow.shell import Shell
from albow.screen import Screen
from albow.text_screen import TextScreen
from albow.resource import get_font, get_image
from albow.grid_view import GridView
from albow.palette_view import PaletteView
from albow.image_array import get_image_array
from albow.dialogs import alert, ask
from albow.file_dialogs import \
	request_old_filename, request_new_filename, look_for_file_or_directory
from albow.tab_panel import TabPanel
from albow.table_view import TableView, TableColumn

#--------------------------------------------------------------------------------
#
#    Buttons
#
#--------------------------------------------------------------------------------

class MenuScreen(Screen):

	def __init__(self, shell):
		Screen.__init__(self, shell)
		self.shell = shell
		f1 = get_font(24, "VeraBd.ttf")
		title = Label("Rdrive", font = f1)
		def screen_button(text, screen):
			return Button(text, action = lambda: shell.show_screen(screen))
		menu = Column([
			screen_button("Text Screen", shell.text_screen),
			screen_button("Text Fields", shell.fields_screen),
			screen_button("Controls", shell.controls_screen),
			screen_button("Timing", shell.anim_screen),
			screen_button("Grid View", shell.grid_screen),
			screen_button("Palette View", shell.palette_screen),
			screen_button("Image Array", shell.image_array_screen),
			screen_button("Modal Dialogs", shell.dialog_screen),
			screen_button("Tab Panel", shell.tab_panel_screen),
			screen_button("Table View", shell.table_screen),
			Button("Quit", shell.quit),
		], align = 'l')
		contents = Column([
			title,
			menu,
		], align = 'l', spacing = 20)
		self.add_centered(contents)
	
	def show_text_screen(self):
		self.shell.show_screen(self.text_screen)
	
	def show_fields_screen(self):
		self.shell.show_screen(self.fields_screen)
		self.fields_screen.fld1.focus()
	
	def show_anim_screen(self):
		self.shell.show_screen(self.anim_screen)
	
	def quit(self):
		sys.exit(0)

#--------------------------------------------------------------------------------
#
#    Text Field
#
#--------------------------------------------------------------------------------

class DemoTextFieldsScreen(Screen):

	def __init__(self, shell):
		Screen.__init__(self, shell)
		self.fld1 = self.add_field("Name", 200)
		self.fld2 = self.add_field("Race", 250)
		btn = Button("OK", action = self.ok)
		btn.rect.midtop = (320, 300)
		self.add(btn)
		out = Label("")
		out.rect.width = 400
		out.rect.topleft = (200, 350)
		self.out = out
		self.add(out)
		btn = Button("Menu", action = self.go_back)
		btn.rect.midtop = (320, 400)
		self.add(btn)
		self.fld1.focus()
	
	def add_field(self, label, pos):
		lbl = Label(label)
		lbl.rect.topleft = (200, pos)
		self.add(lbl)
		fld = TextField(150)
		fld.rect.topleft = (250, pos)
		fld.enter_action = self.ok
		self.add(fld)
		return fld
	
	def ok(self):
		self.out.text = "You are a %s called %s." % (self.fld2.text, self.fld1.text)
	
	def go_back(self):
		self.parent.show_menu()

#--------------------------------------------------------------------------------
#
#   Controls
#
#--------------------------------------------------------------------------------

class DemoControlsScreen(Screen):

	def __init__(self, shell):
		Screen.__init__(self, shell)
		model = DemoControlsModel()
		width_field = FloatField(ref = AttrRef(model, 'width'))
		height_field = FloatField(ref = AttrRef(model, 'height'))
		area_display = ValueDisplay(ref = AttrRef(model, 'area'), format = "%.2f")
		shape = AttrRef(model, 'shape')
		shape_choices = Row([
			RadioButton(setting = 'rectangle', ref = shape), Label("Rectangle"),
			RadioButton(setting = 'triangle', ref = shape), Label("Triangle"),
			RadioButton(setting = 'ellipse', ref = shape), Label("Ellipse"),
			ProgressBar(100),
		])
		grid = Grid([
			[Label("Width"), width_field],
			[Label("Height"), height_field],
			[Label("Shape"), shape_choices],
			[Label("Area"), area_display],
		])
		back = Button("Menu", action = shell.show_menu)
		contents = Column([grid, back])
		self.add_centered(contents)
		width_field.focus()
	
#--------------------------------------------------------------------------------

class DemoControlsModel(object):

	width = 0.0
	height = 0.0
	shape = 'rectangle'

	def get_area(self):
		a = self.width * self.height
		shape = self.shape
		if shape == 'rectangle':
			return a
		elif shape == 'triangle':
			return 0.5 * a
		elif shape == 'ellipse':
			return 0.25 * pi * a
	
	area = property(get_area)

#--------------------------------------------------------------------------------
#
#    Animation
#
#--------------------------------------------------------------------------------

class DemoAnimScreen(Screen):

	def __init__(self, shell):
		Screen.__init__(self, shell)
		self.rect = shell.rect.inflate(-100, -100)
		w, h = self.size
		self.points = [[100, 50], [w - 50, 100], [50, h - 50]]
		from random import randint
		def randv():
			return randint(-5, 5)
		self.velocities = [[randv(), randv()] for i in range(len(self.points))]
		btn = Button("Menu", action = self.go_back)
		btn.rect.center = (w/2, h - 20)
		self.add(btn)
	
	def draw(self, surface):
		from pygame.draw import polygon
		polygon(surface, (128, 200, 255), self.points)
		polygon(surface, (255, 128, 0), self.points, 5)
	
	def begin_frame(self):
		r = self.rect
		w, h = r.size
		for p, v in zip(self.points, self.velocities):
			p[0] += v[0]
			p[1] += v[1]
			if not 0 <= p[0] <= w:
				v[0] = -v[0]
			if not 0 <= p[1] <= h:
				v[1] = -v[1]
		self.invalidate()

	def go_back(self):
		self.parent.show_menu()

#--------------------------------------------------------------------------------
#
#   Grid View
#
#--------------------------------------------------------------------------------

class DemoGridView(GridView):

	info = [
		[("red", "r3d"), ("green", "gr33n"), ("blue", "blu3")],
		[("cyan", "cy4n"), ("magenta", "m4g3nt4"), ("yellow", "y3ll0w")]
	]

	def __init__(self):
		GridView.__init__(self, (30, 30), 2, 3)
	
	def num_rows(self):
		return 2
	
	def num_cols(self):
		return 3
	
	def draw_cell(self, surface, row, col, rect):
		color = Color(self.info[row][col][0])
		surface.fill(color, rect)
	
	def click_cell(self, row, col, event):
		self.output.text = self.info[row][col][1]

#--------------------------------------------------------------------------------

class DemoGridViewScreen(Screen):

	def __init__(self, shell):
		Screen.__init__(self, shell)
		grid = DemoGridView()
		lbl = Label("Cl1ck a Squ4r3")
		grid.output = lbl
		btn = Button("Menu", action = self.go_back)
		contents = Column([grid, lbl, btn], align = 'l', spacing = 30)
		self.add_centered(contents)

	def go_back(self):
		self.parent.show_menu()

#--------------------------------------------------------------------------------
#
#    Palette View
#
#--------------------------------------------------------------------------------

class DemoPaletteView(PaletteView):

	info = ["red", "green", "blue", "cyan", "magenta", "yellow"]
	
	sel_color = Color("white")
	sel_width = 5

	def __init__(self):
		PaletteView.__init__(self, (30, 30), 2, 2, scrolling = True)
		self.selection = None
	
	def num_items(self):
		return len(self.info)
	
	def draw_item(self, surface, item_no, rect):
		d = -2 * self.sel_width
		r = rect.inflate(d, d)
		color = Color(self.info[item_no])
		surface.fill(color, r)
	
	def click_item(self, item_no, event):
		self.selection = item_no
	
	def item_is_selected(self, item_no):
		return self.selection == item_no

#--------------------------------------------------------------------------------

class DemoPaletteViewScreen(Screen):

	def __init__(self, shell):
		Screen.__init__(self, shell)
		w, h = self.size
		grid = DemoPaletteView()
		grid.center = (w/2, h/2)
		self.add(grid)
		btn = Button("Menu", action = self.go_back)
		btn.center = (w/2, h - 50)
		self.add(btn)

	def go_back(self):
		self.parent.show_menu()
	
#--------------------------------------------------------------------------------
#
#    Image Array
#
#--------------------------------------------------------------------------------

class DemoImageArrayScreen(Screen):

	def __init__(self, shell):
		Screen.__init__(self, shell)
		self.images = get_image_array("fruit.png", shape = 3, border = 2)
		self.image = Image(self.images[0])
		self.index = 0
		contents = Column([
			Label("Image Array", font = get_font(18, "VeraBd.ttf")),
			self.image,
			Button("Next Fruit", action = self.next_image),
			Button("Menu", action = shell.show_menu),
		], spacing = 30)
		self.add_centered(contents)
	
	def next_image(self):
		self.index = (self.index + 1) % 3
		self.image.image = self.images[self.index]


#--------------------------------------------------------------------------------
#
#    Dialogs
#
#--------------------------------------------------------------------------------

class DemoDialogScreen(Screen):

	def __init__(self, shell):
		Screen.__init__(self, shell)
		menu = Column([
			Button("Ask a Question", self.test_ask),
			Button("Request Old Filename", self.test_old),
			Button("Request New Filename", self.test_new),
			Button("Look for File or Directory", self.test_lookfor),
		], align = 'l')
		contents = Column([
			Label("File Dialogs", font = get_font(18, "VeraBd.ttf")),
			menu,
			Button("Menu", action = shell.show_menu),
		], align = 'l', spacing = 30)
		self.add_centered(contents)
	
	def test_ask(self):
		response = ask("Do you like mustard and avocado ice cream?",
			["Yes", "No", "Undecided"])
		alert("You chose %r." % response)
	
	def test_old(self):
		path = request_old_filename()
		if path:
			alert("You chose %r." % path)
		else:
			alert("Cancelled.")

	def test_new(self):
		path = request_new_filename(prompt = "Save booty as:",
			filename = "treasure", suffix = ".dat")
		if path:
			alert("You chose %r." % path)
		else:
			alert("Cancelled.")

	def test_lookfor(self):
		path = look_for_file_or_directory(prompt = "Please find 'Vera.ttf'",
			target = "Vera.ttf")
		if path:
			alert("You chose %r." % path)
		else:
			alert("Cancelled.")

#--------------------------------------------------------------------------------
#
#   Tab Panel
#
#--------------------------------------------------------------------------------

class TabPanelScreen(Screen):

	def __init__(self, shell):
		Screen.__init__(self, shell)
		pages = TabPanel()
		pages.size = 300, 200
		self.pages = pages
		for i in xrange(1, 4):
			page = self.make_test_page(i)
			pages.add_page("Page %s" % i, page)
		back = Button("Menu", action = shell.show_menu)
		contents = Column([pages, back], spacing = 30)
		self.add_centered(contents)

	def make_test_page(self, i):
		page_size = self.pages.content_size()
		page = Widget(size = page_size, bg_color = (128, 64, 32))
		lbl = Label("This is page %s" % i)
		page.add_centered(lbl)
		return page

#--------------------------------------------------------------------------------
#
#   Table View
#
#--------------------------------------------------------------------------------

demo_table_data = [
	(1979, 12.5),
	(1980, 13.2),
	(1981, 13.5),
	(1982, 13.1),
	(1983, 14.3),
	(1984, 15.4),
]

selected_table_row = None

#--------------------------------------------------------------------------------

class DemoTableScreen(Screen):

	def __init__(self, shell):
		Screen.__init__(self, shell)
		f = get_font(15, "VeraBd.ttf")
		title = Label("Norwegian Butter Exports", font = f)
		table = DemoTableView()
		back = Button("Menu", action = shell.show_menu)
		contents = Column([title, table, back], spacing = 30)
		self.add_centered(contents)
	
#--------------------------------------------------------------------------------

class DemoTableView(TableView):

	columns = [
		TableColumn("Year", 70),
		TableColumn("Amount", 50, 'r', "%.1f"),
	]

	border_width = 1
	
	def num_rows(self):
		return len(demo_table_data)
	
	def row_data(self, i):
		return demo_table_data[i]
	
	def row_is_selected(self, i):
		return selected_table_row == i
	
	def click_row(self, i, e):
		global selected_table_row
		selected_table_row = i

#--------------------------------------------------------------------------------
#
#    Shell
#
#--------------------------------------------------------------------------------

class RdriveShell(Shell):

	def __init__(self, display):
		Shell.__init__(self, display)
		self.create_demo_screens()
		self.menu_screen = MenuScreen(self) # Do this last
		self.set_timer(frame_time)
		self.show_menu()
	
	def create_demo_screens(self):
		self.text_screen = TextScreen(self, "demo_text.txt")
		self.fields_screen = DemoTextFieldsScreen(self)
		self.controls_screen = DemoControlsScreen(self)
		self.anim_screen = DemoAnimScreen(self)
		self.grid_screen = DemoGridViewScreen(self)
		self.palette_screen = DemoPaletteViewScreen(self)
		self.image_array_screen = DemoImageArrayScreen(self)
		self.dialog_screen = DemoDialogScreen(self)
		self.tab_panel_screen = TabPanelScreen(self)
		self.table_screen = DemoTableScreen(self)
	
	def show_menu(self):
		self.show_screen(self.menu_screen)
	
	def begin_frame(self):
		self.anim_screen.begin_frame()

        def send_key(self, widget, name, event):
		Shell.send_key(self, widget, name, event)
		if event.type == pygame.KEYDOWN:  
			print "Key pressed: " + str(event.key)

def main():
	display = pygame.display.set_mode(screen_size, flags)
	pygame.display.set_caption("Rdrive")
	shell = RdriveShell(display)
	shell.run()

main()
