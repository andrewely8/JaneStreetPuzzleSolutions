#20 by 20 board flattened as a 400 element list of dictionaires, one for each cell.
#i,j represent row i and column j of a given cell. 
board = []
for i in range(20):
	for j in range(20):
		d = {"cell": (i,j), "filled": None, "arrows": "none", "number": -1}
		board.append(d)

#manually fill in the known cells 
board[1]["arrows"] = "right"
board[8]["arrows"] = "left,down"
board[12]["arrows"] = "down"
board[15]["arrows"] = "down"
board[19]["arrows"] = "left,down"
board[24]["arrows"] = "right"
board[33]["arrows"] = "left,down,right"
board[46]["arrows"] = "right"
board[49]["arrows"] = "left,down,right"
board[58]["arrows"] = "left,down,up"
board[61]["arrows"] = "down"
board[63]["arrows"] = "down,right"
board[80]["arrows"] = "right"
board[85]["arrows"] = "down,right"
board[95]["arrows"] = "left,right,up"
board[111]["arrows"] = "down,right"
board[123]["arrows"] = "down"
board[130]["arrows"] = "left,right"
board[133]["arrows"] = "left,down,up"
board[136]["arrows"] = "right"
board[139]["arrows"] = "left,down"
board[141]["arrows"] = "down,right"
board[154]["arrows"] = "left,down"
board[165]["arrows"] = "down,right,up"
board[169]["arrows"] = "left,down,right,up"
board[181]["arrows"] = "right,up"
board[192]["arrows"] = "left,right,up"
board[196]["arrows"] = "down,right"
board[198]["arrows"] = "left,down,up"
board[201]["arrows"] = "up"
board[203]["arrows"] = "down,up"
board[228]["arrows"] = "left,right,up"
board[230]["arrows"] = "left,right"
board[234]["arrows"] = "left,right,up"
board[237]["arrows"] = "left,up"
board[242]["arrows"] = "right,up"
board[245]["arrows"] = "left,down,right,up"
board[258]["arrows"] = "up"
board[260]["arrows"] = "right"
board[272]["arrows"] = "left,up"
board[276]["arrows"] = "up"
board[288]["arrows"] = "left,down,up"
board[291]["arrows"] = "down,up"
board[293]["arrows"] = "down"
board[302]["arrows"] = "right,up"
board[304]["arrows"] = "up"
board[309]["arrows"] = "left,down"
board[314]["arrows"] = "left,down"
board[319]["arrows"] = "left"
board[325]["arrows"] = "up"
board[327]["arrows"] = "right,up"
board[336]["arrows"] = "left"
board[338]["arrows"] = "left,up"
board[341]["arrows"] = "right"
board[350]["arrows"] = "left,down,up"
board[364]["arrows"] = "right,up"
board[366]["arrows"] = "right"
board[374]["arrows"] = "left,up"
board[380]["arrows"] = "right"
board[384]["arrows"] = "right,up"
board[387]["arrows"] = "right"
board[391]["arrows"] = "left"
board[398]["arrows"] = "left,up"

board[31]["number"] = 4
board[35]["number"] = 4
board[47]["number"] = 5
board[72]["number"] = 7
board[74]["number"] = 5
board[90]["number"] = 4
board[93]["number"] = 7
board[97]["number"] = 4
board[106]["number"] = 4
board[108]["number"] = 7
board[127]["number"] = 9
board[157]["number"] = 6
board[162]["number"] = 7
board[171]["number"] = 5
board[194]["number"] = 5
board[205]["number"] = 4
board[207]["number"] = 7
board[218]["number"] = 3
board[263]["number"] = 5
board[266]["number"] = 6
board[269]["number"] = 2
board[306]["number"] = 5
board[352]["number"] = 5
board[353]["number"] = 5
board[368]["number"] = 4

#all cells with arrows in them are unfilled,
#and all cells adjacent to cells with arrows in them are unfilled if they arent
#adjacent in the direciton of the arrow.
for cell in board:
	currentRow = cell["cell"][0]
	currentCol = cell["cell"][1]

	if cell["number"] != -1:
		cell["filled"] = True

	elif cell["arrows"] != "none":

		#first mark all orthogonally adjacent cells next to arrow cells unfilled
		if currentCol != 19:
			board[(currentRow*20)+currentCol+1]["filled"] = False
		if currentCol != 0:
		 	board[(currentRow*20)+currentCol-1]["filled"] = False
		if currentRow != 0:
		 	board[(currentRow*20 - 20)+currentCol]["filled"] = False
		if currentRow != 19:
		 	board[(currentRow*20 + 20)+currentCol]["filled"] = False

		#then reset cells (make them unmarked) orthogonally adjacent to cells which arrows points towards.
		if "left" in cell["arrows"] and currentCol != 0:
			board[(currentRow*20)+currentCol-1]["filled"] = None
		if "right" in cell["arrows"] and currentCol != 19:
			board[(currentRow*20)+currentCol+1]["filled"] = None
		if "up" in cell["arrows"] and currentRow != 0:
			board[(currentRow*20 - 20)+currentCol]["filled"] = None
		if "down" in cell["arrows"] and currentRow != 19:
			board[(currentRow*20 + 20)+currentCol]["filled"] = None


#some cells with arrows were unmarked by previous step, this fixes that by 
#marking all cells with arrows in them as unfilled
for cell in board:
	if cell["arrows"] != "none":
		cell["filled"] = False
	



#For each unmarked cell, if we can't form a path from it to a filled cell, then 
#it is completely surrounded by unfilled cells, and must be marked unfilled.
for cell in board:
	if cell["filled"] == None:
		pass




#Performs a DFS that explores the entire board, checking some conditions.
def DFS():

	#0=false , 1=true
	visited = [[0 for _ in range(20)] for _ in range(20)]

	scc = []
	component = []

	def dfsRec(row,col,component):
		visited[row][col] = 1

		if isValid(row-1,col): #up
			dfsRec(row-1,col,component)


		if isValid(row+1,col): #down
			if board[row*20+col]["filled"] == board[(row+1)*20+col]["filled"]: #The cells the same filling, and neighbors (same component)
				component.append(board[(row+1)*20+col]["cell"]) #add the below cell to the same component
			else: #the cells are different fillings and neighbors (different components)
				scc.append(component) #store current component
				component = [] #reset current component
				new = True
				for c in scc: #check existing components, if already in a component, do nothing, if not, create a new one.
					if board[(row+1)*20+col]["cell"] in c:
						new = False
				if new:
					component = [board[(row+1)*20+col]["cell"]]

			dfsRec(row+1,col,component)


		if isValid(row,col-1): #left
			dfsRec(row,col-1,component)


		if isValid(row,col+1): #right
			dfsRec(row,col+1,component)

	def isValid(row,col):
		if -1 in (row,col) or 20 in (row,col) or visited[row][col] == 1:
			return False
		return True


	for cell in board:
		row,col = cell["cell"]
		if visited[row][col] == 0:
			component.append((row,col))
			dfsRec(row,col,component)

DFS()




#drawBoard function uses pygame to vizialize the board.
def drawBoard():

	import pygame, sys
	pygame.init()
	font = pygame.font.SysFont('Arial', 24)
	downArrow  = pygame.image.load('a1.png')
	rightArrow = pygame.image.load('a2.png')
	upArrow    = pygame.image.load('a3.png')
	leftArrow  = pygame.image.load('a4.png')
	screen = pygame.display.set_mode((650,650))
	screen.fill((255,255,255)) #white background

	for cell in board:

		#draw the 20x20 black outlined boxes
		pygame.draw.rect(screen, (0,0,0), (5+cell["cell"][1]*32,5+cell["cell"][0]*32,32,32), 2)

		#draw numbers in cells that have numbers
		if cell["number"] != -1:
			text_surface = font.render(str(cell["number"]), True, (0,0,0))
			text_rect = text_surface.get_rect()
			text_rect.center = (21+cell["cell"][1]*32,21+cell["cell"][0]*32)
			screen.blit(text_surface, text_rect)

		#Outline filled cells green, and unfilled cells red
		if cell["filled"]:
			pygame.draw.rect(screen, (0,255,0), (5+cell["cell"][1]*32,5+cell["cell"][0]*32,32,32), 2)
		if cell["filled"] == False:
			pygame.draw.rect(screen, (255,0,0), (5+cell["cell"][1]*32,5+cell["cell"][0]*32,32,32), 2)
		
		#Draw arrows in cells that have arrows
		if  "down" in cell["arrows"]:
			screen.blit(downArrow,(19+cell["cell"][1]*32,20+cell["cell"][0]*32))
		if "right" in cell["arrows"]:
			screen.blit(rightArrow,(20+cell["cell"][1]*32,19+cell["cell"][0]*32))
		if "up" in cell["arrows"]:
			screen.blit(upArrow,(19+cell["cell"][1]*32,7+cell["cell"][0]*32))
		if  "left" in cell["arrows"]:
			screen.blit(leftArrow,(7+cell["cell"][1]*32,19+cell["cell"][0]*32))

	#Game loop needed for pygame to work
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		pygame.display.flip()

drawBoard()

#We have 132,134,136, or 138 possible total surface areas
#This functions computes the possible length x width x height dimensions for each 
def possibleBoxDimensions(numberOfCells):
	S = numberOfCells // 2
	res = []
	for a in range(1, S):
		for c in range(a, S):
			num = S - a*c
			den = a + c
			if num > 0 and num % den == 0:
				b = num // den
				s = [a,b,c]
				s.sort()
				if s not in res:
					res.append(s)

	return res


def constructBox(dims):
	a = dims[0]
	b = dims[1]
	c = dims[2]
	face1 = [[0 for _ in range(a)] for _ in range(b)]
	face2 = [[0 for _ in range(a)] for _ in range(b)]
	face3 = [[0 for _ in range(b)] for _ in range(c)]
	face4 = [[0 for _ in range(b)] for _ in range(c)]
	face5 = [[0 for _ in range(a)] for _ in range(c)]
	face6 = [[0 for _ in range(a)] for _ in range(c)]

	print(face1)

