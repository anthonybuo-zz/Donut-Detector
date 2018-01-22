from graphics import *
from random import randint

class Cell(object):
	
	def __init__(self, x, y, s, shade):
		self.x = x
		self.y = y
		self.s = s
		self.shade = shade
		
	def print_info(self):
		print self.x, self.y, self.s
		
	def draw_rect(self, window):
		p1 = Point(self.x * self.s, self.y * self.s)
		p2 = Point(self.x * self.s + self.s, self.y * self.s + self.s)
		rect = Rectangle(p1, p2)
		rect.setFill(color_rgb(self.shade, self.shade, self.shade))
		rect.draw(window)
		
class Filter(object):
	
	multipliers = [[0, -0.2, -0.1, -0.2, 0],
			      [-0.2, 0.7, 1, 0.7, -0.2],
				  [-0.1, 1, -2.5, 1, -0.1],
				  [-0.2, 0.7, 1, 0.7, -0.2],
				  [0, -0.2, -0.1, -0.2, 0]]
				  
	def print_res(self, cells, current_x, current_y, window, total):
		side = cells[current_x][current_y].s
		label_location = Point(current_x * side + side / 2, current_y * side + side / 2)
		label = Text(label_location, str(total))
		label.setFill(color_rgb(255,0,0))
		label.draw(window)
				  
	def compute(self, cells, cols, rows, window):
	
		print "Computing..."
		current_x = 0
		current_y = 0
		
		while current_x < cols and current_y < rows:
			total = 0
			for i in range(-2,3):
				for j in range(-2,3):
					if current_x + i >= 0 and current_y + j >= 0 and current_x + i < cols and current_y + j < rows:
						total -= (255-cells[current_x + i][current_y + j].shade) * Filter.multipliers[2+i][2+j]
	
			cells[current_x][current_y].res = total
			self.print_res(cells, current_x, current_y, window, total)
			if current_x != cols - 1:
				current_x += 1
			else:
				current_x = 0
				current_y += 1
				
		
		
def init_cells(cells, side_length, rows, cols):
	for i in range(0,rows):
		row = []
		for j in range(0,cols):
			shade = randint(0,255)
			new_cell = Cell(i, j, side_length, shade)
			# Uncomment the following section and comment the line above to see
			# a single ring example
			"""
			darks = [[1,0], [2,0], [3,0], 
					 [0,1], [4,1], 
					 [0,2], [2,2], [4,2],
					 [0,3], [4,3],
					 [1,4], [2,4], [3,4]]
			lights = [[1,1], [2,1], [3,1],
					  [1,2], [3,2],
					  [1,3], [2,3], [3,3]]
			if (i == 1 or i == 2 or i == 3) and j == 0:
				new_cell = Cell(i,j,side_length, 0)
			elif (i == 0 or i == 4) and j == 1:
				new_cell = Cell(i,j,side_length, 0)
			elif j == 2 and (i == 0 or i == 2 or i == 4):
				new_cell = Cell(i,j,side_length, 0)
			elif j == 3 and (i == 0 or i == 4):
				new_cell = Cell(i,j,side_length, 0)
			elif j == 4 and (i == 1 or i == 2 or i == 3):
				new_cell = Cell(i,j,side_length, 0)
			else:
				new_cell = Cell(i,j,side_length, 255)
			"""
			
			row.append(new_cell)
		cells.append(row)
		
	return cells
	
def identify_best_match(cells, cols, rows, window):
	best = 0
	for i in range(0, rows):
		for j in range(0, cols):
			if cells[i][j].res > best:
				print "Current best:", cells[i][j].res
				best_value = cells[i][j].res
				best_cell = [i, j]
				best = cells[i][j].res
				
	
	p1 = Point(best_cell[0] * cells[i][j].s - 2*cells[i][j].s, best_cell[1] * cells[i][j].s - 2*cells[i][j].s)
	p2 = Point(best_cell[0] * cells[i][j].s+50 + 2*cells[i][j].s, best_cell[1] * cells[i][j].s+50 + 2*cells[i][j].s)
	best_rectangle = Rectangle(p1, p2)
	best_rectangle.setOutline(color_rgb(0,255,0))
	best_rectangle.draw(window)

def main():
	
	# setup canvas size variables
	canvas_width = 500
	canvas_height = 500
	rows = 10
	cols = 10
	side_length = canvas_width/cols
	
	# setup graphics window
	window = GraphWin("My Grid", canvas_height+1, canvas_width+1)
	
	# initialize cells
	cells = []
	cells = init_cells(cells, side_length, rows, cols)
		
	# print each cell's rectangle
	for i in range(0, rows):
		for j in range(0, cols):
			cells[i][j].draw_rect(window)
			
	donut_filter = Filter()
	donut_filter.compute(cells, cols, rows, window)
	
	identify_best_match(cells, cols, rows, window)
	
	window.getMouse()
	window.close()

main()