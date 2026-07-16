import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Arc
from matplotlib.patches import ConnectionPatch
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from collections import deque
import numpy as np
import copy

#0 means no number in cell
numbers = [
	[0,0,21,0,0,0,0,0,0],
	[21,0,0,0,27,0,0,25,0], 
	[0,27,0,0,0,15,0,0,9],
	[0,0,0,0,0,0,0,0,0],
	[25,0,0,27,0,45,0,0,9],
	[0,0,0,0,0,0,0,0,0],
	[9,0,0,63,0,0,0,45,0],
	[0,63,0,0,9,0,0,0,288],
	[0,0,0,0,0,0,35,0,0]
]

#1 means green, 0 means white
colors = [
	[1,0,0,1,0,1,0,1,0],
	[0,0,0,1,0,0,1,0,1],
	[1,0,0,0,0,0,0,1,0],
	[0,0,0,0,0,0,0,0,1],
	[1,0,0,0,1,0,0,0,0],
	[0,0,0,0,0,0,0,1,1],
	[0,0,0,0,0,0,0,0,0],
	[1,0,0,0,0,0,0,0,0],
	[0,1,0,0,1,0,1,0,1]
]

#tl means topleft, br means bottom right, tr means top right, bl means bottom left, na means none
curves = [
	["na","na","na","na","na","na","na","na","na"],
	["na","na","na","na","na","na","na","na","na"],
	["na","na","na","na","na","na","na","na","na"],
	["na","na","na","na","na","na","na","na","na"],
	["na","na","na","na","na","na","na","na","na"],
	["na","na","na","na","na","na","na","na","na"],
	["na","na","na","na","na","na","na","na","na"],
	["na","na","na","na","na","na","na","na","na"],
	["na","na","na","na","na","na","na","na","na"]
]


#4x4 example
# numbers = [[3,0,9,0],
# 		   [0,0,0,6],
# 		   [8,0,0,0],
# 		   [0,6,0,24]]

# colors = [[0,1,0,1],
# 		  [0,0,0,0],
# 		  [0,1,0,1],
# 		  [0,0,0,0]]

# curves = [["na","na","na","na"],
# 		  ["na","na","na","na"],
# 		  ["na","na","na","na"],
# 		  ["na","na","na","na"]]


green = (0.7,1,0.7)
white = (1,1,1)
smallPieceArea = (4-np.pi)/4
largePieceArea = np.pi/4
archOptions = ["bl_tr","br_tl"]

class board(object):
	def __init__(self,numbers,colors,curves):
		self.board = []
		self.board_dim = len(numbers)
		self.allPathRecords = []
		for i in range(self.board_dim):
			temp = []
			for j in range(self.board_dim):
				color = green if colors[i][j] == 1 else white
				num = None if numbers[i][j] == 0 else numbers[i][j]
				curve = curves[i][j]
				temp.append({"curve":curve, "color": color, "number":num})
			self.board.append(temp)

	def updateCurve(self,i,j,newCurve):
		self.board[i][j]['curve'] = newCurve

	def getCellNumber(self,i,j):
		return self.board[i][j]['number']

	def getCellColor(self,i,j):
		return self.board[i][j]['color']


	def BuildPaths(self,currentCell,currentPath):
		newPaths = []
		directions = []
		if currentCell["arch"] == "br_tl":
			if "tl" in currentCell['openPoints']:
				directions = [(0,-1),(-1,0),(-1,-1)]
			elif "br" in currentCell['openPoints']:
				directions = [(0,1),(1,0),(1,1)]
			directionsArchMap = {
				(0,-1) : {"arch": "bl_tr", "openPoint": "bl"}, 
				(0,1)  : {"arch": "bl_tr", "openPoint": "tr"}, 
				(-1,0) : {"arch": "bl_tr", "openPoint": "tr"}, 
				(1,0)  : {"arch": "bl_tr", "openPoint": "bl"}, 
				(-1,-1): {"arch": "br_tl", "openPoint": "tl"}, 
				(1,1)  : {"arch": "br_tl", "openPoint": "br"}
			}
		elif currentCell["arch"] == "bl_tr":
			if "bl" in currentCell['openPoints']:
				directions = [(0,-1),(1,0),(1,-1)]
			elif "tr" in currentCell['openPoints']:
				directions = [(0,1),(-1,0),(-1,1)]
			directionsArchMap = {
				(0,-1) : {"arch": "br_tl", "openPoint": "tl"}, 
				(0,1)  : {"arch": "br_tl", "openPoint": "br"}, 
				(-1,0) : {"arch": "br_tl", "openPoint": "tl"}, 
				(1,0)  : {"arch": "br_tl", "openPoint": "br"}, 
				(1,-1) : {"arch": "bl_tr", "openPoint": "bl"}, 
				(-1,1) : {"arch": "bl_tr", "openPoint": "tr"}
			}
			
		for currentOpenPoint in currentCell["openPoints"]:
			currentCell["openPoints"].pop() #Throw away currentOpenPoint since we are closing it now.
			for d in directions:
				new_row = currentCell["row"]+d[0]
				new_col = currentCell["col"]+d[1]

				if 0 <= new_row < self.board_dim and 0 <= new_col < self.board_dim and self.getCellColor(currentCell["row"]+d[0],currentCell["col"]+d[1]) != green:
					copyPath = copy.deepcopy(currentPath)
					visited = {(c["row"],c["col"]) for c in copyPath}
					copyPath.append(currentCell) 
					newOpenPoints = []
					newOpenPoints.append(directionsArchMap[d]["openPoint"])
					newCell = {"row":  currentCell["row"]+d[0], "col": currentCell["col"]+d[1], "arch": directionsArchMap[d]["arch"], "openPoints": newOpenPoints}
					if (new_row,new_col) not in visited: 
						copyPath.append({"row": currentCell["row"]+d[0], "col": currentCell["col"]+d[1], "arch": directionsArchMap[d]["arch"], "openPoints": newOpenPoints})
						newPaths.append(copyPath)
		return newPaths

	def Search(self,source,targetArea):
		source_row, source_col = source[0],source[1]
		source_number = self.getCellNumber(source_row,source_col)
		paths = deque()

		# if source_row == 0:
		# 	paths.append(deque([{"row": source_row, "col": source_col, "arch": "bl_tr", "openPoints": ["bl"]}]))
		# 	paths.append(deque([{"row": source_row, "col": source_col, "arch": "br_tl", "openPoints": ["br"]}]))
		# if source_col == 0:
		# 	paths.append(deque([{"row": source_row, "col": source_col, "arch": "bl_tr", "openPoints": ["tr"]}]))
		# 	paths.append(deque([{"row": source_row, "col": source_col, "arch": "br_tl", "openPoints": ["br"]}]))
		# if source_row == self.board_dim-1:
		# 	paths.append(deque([{"row": source_row, "col": source_col, "arch": "bl_tr", "openPoints": ["tr"]}]))
		# 	paths.append(deque([{"row": source_row, "col": source_col, "arch": "br_tl", "openPoints": ["tl"]}]))
		# if source_col == self.board_dim-1:
		# 	paths.append(deque([{"row": source_row, "col": source_col, "arch": "bl_tr", "openPoints": ["bl"]}]))
		# 	paths.append(deque([{"row": source_row, "col": source_col, "arch": "br_tl", "openPoints": ["tl"]}]))
		# else:
		# 	paths.append(deque([{"row": source_row, "col": source_col, "arch": "bl_tr", "openPoints": ["bl","tr"]}]))
		# 	#paths.append(deque([{"row": source_row, "col": source_col, "arch": "br_tl", "openPoints": ["br","tl"]}]))

		
		paths.append(deque([{"row": source_row, "col": source_col-1, "arch": "br_tl", "openPoints": ["tl"]}]))

		
		maxLen = 240
		maxPathLen = targetArea+1
		i=0
		while paths and i < maxLen:
			i+=1
			currentPath = paths.pop()
			self.allPathRecords.append(copy.deepcopy(currentPath))
			print("\nEXPLORING PATH:  ", currentPath)
			while currentPath:
				currentCell = currentPath.pop()
				if currentCell["openPoints"]:
					print("\tEXPLORING CELL:  ", currentCell)
					print("\t\tFOUND NEW PATHS:  ")
					newPaths = self.BuildPaths(currentCell,currentPath)
					for p in newPaths:
						if len(p)<=maxPathLen:
							print("\t\t\t",p)
							paths.append(p)


		print("\nALL PATH RECORDS")
		for p in self.allPathRecords:
			print("\n",p)




'''
Note: our board is stored row,col but visual draws on the x,y plane. We use j as x and i as y to flip to x,y interpretation for drawing purposes.
'''
def visual(arr,num_rows,num_cols,cell_size=16,cell_color='white',edge_color='black',animate=False):
	ax = plt.gca()
	archs = []
	if animate:
		mngr = plt.get_current_fig_manager()
		mngr.window.geometry('600x600+10+10')
	for i in range(num_rows):
		for j in range(num_cols):
			rect = plt.Rectangle([i*cell_size, j*cell_size], cell_size, cell_size, facecolor=arr[j][i]['color'], edgecolor=edge_color)
			ax.add_patch(rect)
			plt.text(i*cell_size+cell_size/2,j*cell_size+cell_size/2, arr[j][i]['number'],fontsize="12",weight=500,ha="center",va="center")
			if arr[i][j]["curve"] == "bl_tr":
				ax.add_patch(ConnectionPatch((j*cell_size, i*cell_size+cell_size),(j*cell_size+cell_size, i*cell_size),"data",color="red",zorder=2,lw=2))
			elif arr[i][j]["curve"] == "br_tl":
				ax.add_patch(ConnectionPatch((j*cell_size, i*cell_size),(j*cell_size+cell_size, i*cell_size+cell_size),"data",color="red",zorder=2,lw=2))
	ax.axis('off')
	ax.autoscale_view()
	ax.invert_yaxis()
	ax.set_aspect('equal', 'box')
	ax.xaxis.set_major_locator(plt.NullLocator())
	ax.yaxis.set_major_locator(plt.NullLocator())
	if animate:
		plt.show(block=False)
		plt.pause(0.5)
		plt.clf()
	else:
		plt.show()


# b = board(numbers,colors,curves)
# b.Search((8,6),7)


# possibleCurves = b.allPathRecords
# print(possibleCurves)
# print("Number of explored paths: ", len(possibleCurves))

# for p in possibleCurves:
# 	print("\n",p)
# 	newBoard = board(numbers,colors,curves)
# 	for c in p:
# 		newBoard.updateCurve(c["row"],c["col"],c["arch"])
# 	visual(newBoard.board, num_rows=newBoard.board_dim, num_cols=newBoard.board_dim,animate=True)


finalNumbers = [
	[21,21,21,27,27,288,288,15,25],
	[21,21,21,27,27,15,15,25,25], 
	[21,27,27,288,288,15,15,25,9],
	[25,27,27,288,288,45,45,25,9],
	[25,25,25,27,288,45,45,45,9],
	[288,25,288,63,288,288,288,45,45],
	[9,9,63,63,288,35,35,45,45],
	[9,63,63,288,9,9,35,288,288],
	[63,63,288,288,9,35,35,35,35]
]

colors = [
	[1,0,0,1,0,1,0,1,0],
	[0,0,0,1,0,0,1,0,1],
	[1,0,0,0,0,0,0,1,0],
	[0,0,0,0,0,0,0,0,1],
	[1,0,0,0,1,0,0,0,0],
	[0,0,0,0,0,0,0,1,1],
	[0,0,0,0,0,0,0,0,0],
	[1,0,0,0,0,0,0,0,0],
	[0,1,0,0,1,0,1,0,1]
]

#tl means topleft, br means bottom right, tr means top right, bl means bottom left, na means none
finalCurves = [
	["na","na","na","na","na","na","na","na","na"],
	["na","na","na","na","na","na","na","na","na"],
	["na","na","na","na","na","na","na","na","na"],
	["na","na","na","na","na","na","na","na","na"],
	["na","na","na","na","na","na","na","na","na"],
	["na","na","na","na","na","na","na","na","na"],
	["na","na","na","na","na","na","na","na","na"],
	["na","na","na","na","na","na","na","na","na"],
	["na","na","na","na","na","na","na","na","na"]
]

# finalNumbers = [
# 	[3,9,9,6],
# 	[8,8,9,6],
#     [8,8,24,24],
#     [6,6,24,24]
# ]

# colors = [[0,1,0,1],
# 		  [0,0,0,0],
# 		  [0,1,0,1],
# 		  [0,0,0,0]]

# finalCurves = [["na","na","na","na"],
# 		  ["na","na","na","na"],
# 		  ["na","na","na","na"],
# 		  ["na","na","na","na"]]

rowSums = []
colSums = []
rowSquares = 0
colSquares = 0
for row in finalNumbers:
	rowSums.append(sum(row))

for i in range(len(finalNumbers)):
	col = []
	for row in finalNumbers:
		col.append(row[i])
	colSums.append(sum(col))
for i in rowSums:
	rowSquares += i**2
for i in colSums:
	colSquares += i**2

print("ROW SUMS: ", rowSums)
print("COL SUMS: ", colSums)
print("ROW SUM OF SQUARES: ", rowSquares)
print("COL SUM OF SQUARES: ", colSquares)
print("FINAL ANSWER: ", rowSquares+colSquares)



finalBoard = board(finalNumbers,colors,finalCurves)
visual(finalBoard.board, num_rows=finalBoard.board_dim, num_cols=finalBoard.board_dim,animate=False)
