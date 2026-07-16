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






# def CheckRepeat(newMove,currentMoves):
# 	exploredCells = []
# 	for m in currentMoves:
# 		exploredCells.append((m['row'],m['col']))
# 	if (newMove['row'],newMove['col']) in exploredCells:
# 		return True
# 	return False



# def CheckMultipleTowers(newMove,currentMoves):
# 	regionsWithTowers = []
# 	for m in currentMoves:
# 		if m['tower']:
# 			regionsWithTowers.append(m['region'])
# 	if newMove['tower'] and newMove['region'] in regionsWithTowers:
# 		return True
# 	return False



# def CheckCellNumber(newMove,currentMoves,modulo,moveCountOffset=0):
# 	if (len(currentMoves)-moveCountOffset) % modulo == 0:
# 		if board[newMove['row']][newMove['col']]['num'] == newMove['num']:
# 			return True
# 		else:
# 			return False
# 	return True



# def CheckFinished(currentMoves):
# 	explored = []
# 	numberedCells = [(0,5),(0,7),(2,3),(2,5),(3,0),(4,1),(4,4),(5,1),(5,3),(5,5),(5,6),(7,0)]
# 	for m in currentMoves:
# 		explored.append((m['row'],m['col']))
# 	for n in numberedCells:
# 		if n not in explored:
# 			return False

# 	regionsWithTowers = []
# 	regions = ["f","i","l","n","p","t","u","v","w","x","y","z","s"]
# 	for m in currentMoves:
# 		if m['tower'] and m['region'] not in regionsWithTowers:
# 			regionsWithTowers.append(m['region'])
# 	for r in regions:
# 		if r not in regionsWithTowers:
# 			return False
# 	return True



# def GetFirst18():
# 	while trackedMoves:
# 		currentMoves = trackedMoves.pop()
# 		currentCell = currentMoves[-1]
# 		possibleMoves = getPossibleMoves(currentCell,currentMoves)
# 		for p in possibleMoves:
# 			if (not CheckRepeat(p,currentMoves) 
# 			    and not CheckMultipleTowers(p,currentMoves)
# 			    and CheckCellNumber(p,currentMoves,3)):
# 				copy = currentMoves.copy()
# 				copy.append(p)
# 				trackedMoves.append(copy)
# 		if len(currentMoves) == 19:
# 			first18Moves.append(currentMoves)



# def GetRest():
# 	cnt = 0
# 	for k in range(4,10):
# 		trackedMoves = first18Moves.copy()
# 		print("TRYING k = ",k)
# 		while trackedMoves:
# 			cnt+=1
# 			currentMoves = trackedMoves.pop()
# 			currentCell = currentMoves[-1]
# 			possibleMoves = getPossibleMoves(currentCell,currentMoves)
# 			for p in possibleMoves:
# 				if (not CheckRepeat(p,currentMoves) 
# 				    and not CheckMultipleTowers(p,currentMoves)
# 				    and CheckCellNumber(p,currentMoves,k,moveCountOffset=18)):
# 					copy = currentMoves.copy()
# 					copy.append(p)
# 					trackedMoves.append(copy)
# 					if CheckFinished(copy):
# 						print("---FOUND SOLUTION---")
# 						print(copy)
# 						print("---FOUND SOLUTION---")
# 						visual(copy,animate=False)
# 						return(copy)



# GetFirst18()
# SOL = GetRest()

# if SOL:
# 	ds = [(0,1),(0,-1),(-1,0),(1,0)]
# 	finalSum = 0
# 	visited = []
# 	numMap = {}

# 	for m in SOL:
# 		visited.append((m['row'],m['col']))
# 		t = (m['row'],m['col'])
# 		numMap[t] = m['num']

# 	for i in range(NUM_ROWS):
# 		for j in range(NUM_COLS):
# 			if (i,j) not in visited:
# 				for d in ds:
# 					neighbor = (i+d[0],j+d[1])
# 					if neighbor in visited:
# 						print(numMap[(neighbor[0],neighbor[1])])
# 						finalSum += numMap[(neighbor[0],neighbor[1])]

# 	print("\n\nFinal Answer: ",finalSum)