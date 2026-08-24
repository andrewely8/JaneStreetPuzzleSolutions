#Andrew Ely
#Jane Street Puzzle July 2026
#Solution
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Arc
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

NUM_ROWS = 8
NUM_COLS = 8
colors = {
	"f" : (1, 0.33, 0.33),  "i" : (1, 0.58, 0.33),  "l" : (1, 0.98, 0.33),  "n" : (0.89, 0.98, 0.67),  
	"p" : (0.33, 0.33, 1),  "t" : (0.87, 0.67, 0.9),  "u" : (0.18, 0.65, 0.18),  "v" : (1, 0.67, 0.99),  
	"w" : (0.87, 0.66, 0.53),  "x" : (1, 0.53, 0),  "y" : (1, 1, 0),  "z" : (0, 1, 0),  "s" : (0.5, 1, 0.9), 
}

board = [[{} for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

trackedMoves = [
	[{'row': 7, 'col': 0, 'num': 0, 'tower':  True, 'region': 't'}],
	[{'row': 7, 'col': 0, 'num': 0, 'tower': False, 'region': 't'}],
]
first18Moves = []

#moveDirections is a list of the possible ways the knight can move.
#a move [x,y,z] represents the number of moves to make along each dimension.
# x is left and right, y is up an down, z is on top or below (tower dimension).
moveDirections = [
	[ 2, 1,0],[-2, 1,0],[ 2,-1,0],[-2,-1,0],
	[ 1, 2,0],[-1, 2,0],[ 1,-2,0],[-1,-2,0],
	[0, 2, 1],[0,-2, 1],[0, 2,-1],[0,-2,-1],
	[ 2,0, 1],[-2,0, 1],[ 2,0,-1],[-2,0,-1],
]

regions = {
	"f" : [(3,5),(4,5),(5,5),(5,4),(4,6)],
	"i" : [(0,0),(0,1),(0,2),(0,3),(0,4)],
	"l" : [(4,7),(5,7),(6,7),(7,7),(7,6)],
	"n" : [(2,1),(3,1),(3,2),(4,2),(5,2)],
	"p" : [(1,3),(1,4),(2,3),(2,4),(2,5)],
	"t" : [(7,0),(7,1),(7,2),(6,1),(5,1)],
	"u" : [(1,0),(1,1),(1,2),(2,0),(2,2)],
	"v" : [(0,5),(0,6),(0,7),(1,7),(2,7)],
	"w" : [(7,4),(7,5),(6,5),(6,6),(5,6)],
	"x" : [(7,3),(6,3),(5,3),(6,2),(6,4)],
	"y" : [(3,0),(4,0),(5,0),(6,0),(4,1)],
	"z" : [(1,5),(1,6),(2,6),(3,6),(3,7)],
	"s" : [(3,3),(3,4),(4,3),(4,4)],
}


for i in range(NUM_ROWS):
	for j in range(NUM_COLS):
		board[i][j]['row'] = i
		board[i][j]['col'] = j
		board[i][j]['num'] = None
		board[i][j]['tower'] = None
		for r in regions:
			if (i,j) in regions[r]:
				board[i][j]['region'] = r

board[0][5]['num'] = 37
board[0][7]['num'] = 1100
board[2][3]['num'] = 23
board[2][5]['num'] = 138
board[3][0]['num'] = 528
board[4][1]['num'] = 449
board[4][4]['num'] = 16
board[5][1]['num'] = 750
board[5][3]['num'] = 88
board[5][5]['num'] = 272
board[5][6]['num'] = 1
board[7][0]['num'] = 0


#If we are currently on a tower,
#Then "normal" knight moves must be onto other towers,
#And Z dimensional moves must be down onto no tower cells.
#
#If we are currently not on a tower,
#Then normal knight moves must be onto other non tower cells,
#And Z dimensional moves must be up onto tower cells.
#
#
#Normal knight move: add moveNumber to current score
#Move down: divide current score by moveNumber
#Move up: multiply current score by moveNumber
#
#Moving down must result in an evenly divisble operation
#
def getPossibleMoves(currentCell,currentMoves):
	currentScore = currentCell['num']
	currentMoveNumber = len(currentMoves)
	possibleMoves = []
	if currentCell['tower'] == True: # We are on a tower
		for move in moveDirections:
			next_row = currentCell['row']+move[0] 
			next_col = currentCell['col']+move[1]
			if 0 <= next_row <= 7 and 0 <= next_col <= 7: 
				if move[2] == 0: # Normal knight move, must be onto a tower.
					if board[next_row][next_col]['tower'] == None:
						m = {'row': next_row, 'col': next_col, 
							 'num': currentScore+currentMoveNumber, 
							 'tower': True, 
							 'region': board[next_row][next_col]['region']}
						if board[next_row][next_col]['num'] == None:
							possibleMoves.append(m)
						elif board[next_row][next_col]['num'] == m['num']:
							possibleMoves.append(m)
				elif move[2] == -1: # Z-dim move, must be down to a non tower.
					if board[next_row][next_col]['tower'] == None and currentScore % currentMoveNumber == 0:
						m = {'row': next_row, 'col': next_col, 
							 'num': currentScore // currentMoveNumber, 
							 'tower': False, 
							 'region': board[next_row][next_col]['region']}
						if board[next_row][next_col]['num'] == None:
							possibleMoves.append(m)
						elif board[next_row][next_col]['num'] == m['num']:
							possibleMoves.append(m)

	elif currentCell['tower'] == False: # We are not on a tower
		for move in moveDirections:
			next_row = currentCell['row']+move[0] 
			next_col = currentCell['col']+move[1]
			if 0 <= next_row <= 7 and 0 <= next_col <= 7: 
				if move[2] == 0: # Normal knight move, must be onto non tower cell.
					if board[next_row][next_col]['tower'] == None:
						m = {'row': next_row, 'col': next_col, 
							 'num': currentScore+currentMoveNumber, 
							 'tower': False, 
							 'region': board[next_row][next_col]['region']}
						if board[next_row][next_col]['num'] == None:
							possibleMoves.append(m)
						elif board[next_row][next_col]['num'] == m['num']:
							possibleMoves.append(m)
				elif move[2] == 1: # Z-dim move, must be up to a tower.
					if board[next_row][next_col]['tower'] == None:
						m = {'row': next_row, 'col': next_col, 
							 'num': currentScore * currentMoveNumber, 
							 'tower': True, 
							 'region': board[next_row][next_col]['region']}
						if board[next_row][next_col]['num'] == None:
							possibleMoves.append(m)
						elif board[next_row][next_col]['num'] == m['num']:
							possibleMoves.append(m)

	return possibleMoves



def visual(moves,num_rows=NUM_ROWS,num_cols=NUM_COLS,cell_size=16,edge_color='black',animate=True):
	ax = plt.gca()
	if animate:
		mngr = plt.get_current_fig_manager()
		mngr.window.geometry('600x600+10+10')

	for i in range(num_rows):
		for j in range(num_cols):
			cell_color = colors[board[j][i]['region']]
			rect = plt.Rectangle([i*cell_size, j*cell_size], cell_size, cell_size, facecolor=cell_color, edgecolor=edge_color)
			ax.add_patch(rect)
			if board[j][i]['num'] != None:
				plt.text(i*cell_size+cell_size/2,j*cell_size+cell_size/2, board[j][i]['num'],fontsize="12",weight=500,ha="center",va="center")

	for i,move in enumerate(moves):
		if move['tower']:
			plt.text(move['col']*cell_size+4,move['row']*cell_size+4, "T",fontsize="12",color=(1,0,0),weight=500,ha="center",va="center")
		rect = plt.Rectangle([move['col']*cell_size, move['row']*cell_size], cell_size, cell_size, facecolor=(0,0,0,0), edgecolor=(1,0,0))
		ax.add_patch(rect)
		rect = plt.Rectangle([move['col']*cell_size+cell_size-cell_size/3, move['row']*cell_size], cell_size/3, cell_size/3, facecolor=(0,0,0,0), edgecolor=(1,0,0))
		ax.add_patch(rect)
		plt.text(move['col']*cell_size+cell_size-2,move['row']*cell_size+3, i,fontsize="8",color=(1,0,0),weight=500,ha="center",va="center")
		if board[move['row']][move['col']]['num'] == None:
			plt.text(move['col']*cell_size+cell_size/2,move['row']*cell_size+cell_size/2, move['num'],fontsize="12",color=(0,0,1),weight=500,ha="center",va="center")
	ax.axis('off')
	ax.autoscale_view()
	ax.invert_yaxis()
	ax.set_aspect('equal', 'box')
	ax.xaxis.set_major_locator(plt.NullLocator())
	ax.yaxis.set_major_locator(plt.NullLocator())
	if animate:
		plt.show(block=False)
		plt.pause(1)
		plt.clf()
	else:
		plt.show()



def CheckRepeat(newMove,currentMoves):
	exploredCells = []
	for m in currentMoves:
		exploredCells.append((m['row'],m['col']))
	if (newMove['row'],newMove['col']) in exploredCells:
		return True
	return False



def CheckMultipleTowers(newMove,currentMoves):
	regionsWithTowers = []
	for m in currentMoves:
		if m['tower']:
			regionsWithTowers.append(m['region'])
	if newMove['tower'] and newMove['region'] in regionsWithTowers:
		return True
	return False



def CheckCellNumber(newMove,currentMoves,modulo,moveCountOffset=0):
	if (len(currentMoves)-moveCountOffset) % modulo == 0:
		if board[newMove['row']][newMove['col']]['num'] == newMove['num']:
			return True
		else:
			return False
	return True



def CheckFinished(currentMoves):
	explored = []
	numberedCells = [(0,5),(0,7),(2,3),(2,5),(3,0),(4,1),(4,4),(5,1),(5,3),(5,5),(5,6),(7,0)]
	for m in currentMoves:
		explored.append((m['row'],m['col']))
	for n in numberedCells:
		if n not in explored:
			return False

	regionsWithTowers = []
	regions = ["f","i","l","n","p","t","u","v","w","x","y","z","s"]
	for m in currentMoves:
		if m['tower'] and m['region'] not in regionsWithTowers:
			regionsWithTowers.append(m['region'])
	for r in regions:
		if r not in regionsWithTowers:
			return False
	return True



def GetFirst18():
	while trackedMoves:
		currentMoves = trackedMoves.pop()
		currentCell = currentMoves[-1]
		possibleMoves = getPossibleMoves(currentCell,currentMoves)
		for p in possibleMoves:
			if (not CheckRepeat(p,currentMoves) 
			    and not CheckMultipleTowers(p,currentMoves)
			    and CheckCellNumber(p,currentMoves,3)):
				copy = currentMoves.copy()
				copy.append(p)
				trackedMoves.append(copy)
		if len(currentMoves) == 19:
			first18Moves.append(currentMoves)



def GetRest():
	cnt = 0
	for k in range(4,10):
		trackedMoves = first18Moves.copy()
		print("TRYING k = ",k)
		while trackedMoves:
			cnt+=1
			currentMoves = trackedMoves.pop()
			currentCell = currentMoves[-1]
			possibleMoves = getPossibleMoves(currentCell,currentMoves)
			for p in possibleMoves:
				if (not CheckRepeat(p,currentMoves) 
				    and not CheckMultipleTowers(p,currentMoves)
				    and CheckCellNumber(p,currentMoves,k,moveCountOffset=18)):
					copy = currentMoves.copy()
					copy.append(p)
					trackedMoves.append(copy)
					if CheckFinished(copy):
						print("---FOUND SOLUTION---")
						print(copy)
						print("---FOUND SOLUTION---")
						visual(copy,animate=False)
						return(copy)



GetFirst18()
SOL = GetRest()

if SOL:
	ds = [(0,1),(0,-1),(-1,0),(1,0)]
	finalSum = 0
	visited = []
	numMap = {}

	for m in SOL:
		visited.append((m['row'],m['col']))
		t = (m['row'],m['col'])
		numMap[t] = m['num']

	for i in range(NUM_ROWS):
		for j in range(NUM_COLS):
			if (i,j) not in visited:
				for d in ds:
					neighbor = (i+d[0],j+d[1])
					if neighbor in visited:
						print(numMap[(neighbor[0],neighbor[1])])
						finalSum += numMap[(neighbor[0],neighbor[1])]

	print("\n\nFinal Answer: ",finalSum)
else:
	print("CANNOT FIND SOLUTION")