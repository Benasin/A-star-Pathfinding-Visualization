import pygame ,math, time
from pygame.locals import *
pygame.init()

col = 40
row = 40

class Cell(object):
	def __init__(self, i, j):
		self.i = i
		self.j = j
		self.f = 0
		self.h = 0
		self.g = 0
		self.neighbors = []
		self.previous  = None
	def addNeighbors(self,grid, obstacle): #Check neighbor for every conditions
		if self.i < (col - 1):
			self.neighbors.append(grid[self.i + 1][self.j])
		if self.i > 0:
			self.neighbors.append(grid[self.i - 1][self.j])
		if self.j < (row - 1):
			self.neighbors.append(grid[self.i][self.j + 1])
		if self.j > 0:
			self.neighbors.append(grid[self.i][self.j - 1])

		if self.i > 0 and self.j > 0 and grid[self.i - 1][self.j] not in obstacle and grid[self.i][self.j - 1] not in obstacle:
			self.neighbors.append(grid[self.i - 1][self.j - 1])

		if self.i > 0 and self.j < (row - 1) and grid[self.i - 1][self.j] not in obstacle and grid[self.i][self.j + 1] not in obstacle:
			self.neighbors.append(grid[self.i - 1][self.j + 1])

		if self.i < (col - 1) and self.j > 0 and grid[self.i + 1][self.j] not in obstacle and grid[self.i][self.j - 1] not in obstacle:
			self.neighbors.append(grid[self.i + 1][self.j - 1])

		if self.i < (col - 1) and self.j < (row - 1) and grid[self.i + 1][self.j] not in obstacle and grid[self.i][self.j + 1] not in obstacle:
			self.neighbors.append(grid[self.i + 1][self.j + 1])

	def show(self):
		pygame.draw.rect(screen, (255,255,255), (self.i * 20, self.j * 20, 20, 20))
		pygame.draw.rect(screen, (0,0,0), (self.i * 20, self.j * 20, 20, 20), 1)
	def obstacle(self):
		pygame.draw.rect(screen, (0,0,0), (self.i * 20, self.j * 20, 20, 20))
	def start(self):
		pygame.draw.rect(screen, (0,255,0), (self.i * 20, self.j * 20, 20, 20))
		pygame.draw.rect(screen, (0,0,0), (self.i * 20, self.j * 20, 20, 20), 1)
	def end(self):
		pygame.draw.rect(screen, (255,0,0), (self.i * 20, self.j * 20, 20, 20))
		pygame.draw.rect(screen, (0,0,0), (self.i * 20, self.j * 20, 20, 20), 1)
	def color(self, color):
		pygame.draw.rect(screen, (color), (self.i * 20, self.j * 20, 20, 20))
		pygame.draw.rect(screen, (0,0,0), (self.i * 20, self.j * 20, 20, 20), 1)

screen = pygame.display.set_mode((800, 800))
screen.fill((255,255,255))

#Calculate the heuristic
def heuristic(a,b):
	distance = abs(a.i - b.i) + abs(a.j - b.j)
	return distance

def main():
	grid = []
	#Create a 2D Array
	for i in range(row):
		container = []
		for j in range(col):
			container.append(Cell(i,j))
		grid.append(container)
	#Show everything
	for i in range(row):
		for j in range(col):
			grid[i][j].show()
	openSet = []
	closedSet = []
	end = []
	start = []
	obstacle = []
	path = []
	dragging_draw = False
	dragging_erase = False
	loop = True

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
			x, y = pygame.mouse.get_pos()
			x_index = round(x / 20 + 0.5) - 1
			y_index = round(y / 20 + 0.5) - 1
			if event.type == pygame.MOUSEBUTTONDOWN: 
				if event.button == 3: #Erase obstacle on right click
					if grid[x_index][y_index] in obstacle:
						obstacle.remove(grid[x_index][y_index])
						grid[x_index][y_index].show()
						dragging_erase = True
				elif event.button == 1: #Add obstacle on left click
					if grid[x_index][y_index] not in obstacle:
						grid[x_index][y_index].obstacle()
						obstacle.append(grid[x_index][y_index])
						dragging_draw = True
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					dragging_draw = False
				if event.button == 3:
					dragging_erase = False
			elif event.type == pygame.MOUSEMOTION: #Add dragging effect
				if dragging_draw and grid[x_index][y_index] not in obstacle:
					grid[x_index][y_index].obstacle()
					obstacle.append(grid[x_index][y_index])
				elif dragging_erase and  grid[x_index][y_index] in obstacle:
					obstacle.remove(grid[x_index][y_index])
					grid[x_index][y_index].show()

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_s: #Place start when press s
					grid[x_index][y_index].start()
					start.append(grid[x_index][y_index])
					openSet.append(grid[x_index][y_index])
				elif event.key == pygame.K_e: #Place end when press e
					grid[x_index][y_index].end()
					end.append(grid[x_index][y_index])
				elif event.key == pygame.K_r: #Reset when press r
					main()

		winner = 0 
		if len(openSet) > 0 and len(end) > 0 and len(start) > 0 and loop: # if openSet, end, start is not empty then start the loop
			for i in range(len(openSet)):
				if openSet[i].f < openSet[winner].f: # Find the cell with the smallest f cost
					winner = i
			current = openSet[winner] # the current cell will now be the cell with the smallest f cost
			openSet.remove(current) # remove current cell from openSet
			closedSet.append(current)

			for i in range(row):
				for j in range(col):
					grid[i][j].addNeighbors(grid, obstacle) # add neighbors to all cells

			neighbors = current.neighbors 
			for neighbor in neighbors:
				if neighbor not in closedSet and neighbor not in obstacle: #evaluate if the tempG will be more efficient
					tempG = current.g + 1 
					newPath = False
					if neighbor in openSet:
						if tempG < neighbor.g:
							neighbor.g = tempG
							newPath = True
					else:
						neighbor.g = tempG
						openSet.append(neighbor)
						newPath = True

					if newPath:
						neighbor.h = heuristic(neighbor, end[0])# if there is a new path calculate the f cost
						neighbor.f = neighbor.g + neighbor.h
						neighbor.previous = current #set the neighbor parent into current
			path = []
			if current == end[0]:
				temp = current
				while (temp.previous != None): #make a loop to trace back the path
					path.append(temp.previous)
					temp = temp.previous
				loop = False
				print('Done')

		#color everything
		for cell in openSet:
			cell.color((0,255,0))
		for cell in closedSet:
			cell.color((231,84,128))
		for cell in path:
			cell.color((135,206,250))
		for cell in start:
			cell.color((0,0,255))
		for cell in end:
			cell.color((255,0,0))

		pygame.display.update()
if __name__ == '__main__':
	main()