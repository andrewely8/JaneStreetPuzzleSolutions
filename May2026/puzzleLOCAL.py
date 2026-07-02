import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Arc
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from collections import deque
import numpy as np
import copy

# #0 means no number in cell
# numbers = [
# 	[0,0,21,0,0,0,0,0,0],
# 	[21,0,0,0,27,0,0,25,0], 
# 	[0,27,0,0,0,15,0,0,9],
# 	[0,0,0,0,0,0,0,0,0],
# 	[25,0,0,27,0,45,0,0,9],
# 	[0,0,0,0,0,0,0,0,0],
# 	[9,0,0,63,0,0,0,45,0],
# 	[0,63,0,0,9,0,0,0,288],
# 	[0,0,0,0,0,0,35,0,0]
# ]

# #1 means green, 0 means white
# colors = [
# 	[1,0,0,1,0,1,0,1,0],
# 	[0,0,0,1,0,0,1,0,1],
# 	[1,0,0,0,0,0,0,1,0],
# 	[0,0,0,0,0,0,0,0,1],
# 	[1,0,0,0,1,0,0,0,0],
# 	[0,0,0,0,0,0,0,1,1],
# 	[0,0,0,0,0,0,0,0,0],
# 	[1,0,0,0,0,0,0,0,0],
# 	[0,1,0,0,1,0,1,0,1]
# ]

# #tl means topleft, br means bottom right, tr means top right, bl means bottom left, na means none
# curves = [
# 	["na","na","na","na","na","na","na","na","na"],
# 	["na","na","na","na","na","na","na","na","na"],
# 	["na","na","na","na","na","na","na","na","na"],
# 	["na","na","na","na","na","na","na","na","na"],
# 	["na","na","na","na","na","na","na","na","na"],
# 	["na","na","na","na","na","na","na","na","na "],
# 	["na","na","na","na","na","na","na","na","na"],
# 	["na","na","na","na","na","na","na","na","na"],
# 	["na","na","na","na","na","na","na","na","na"]
# ]

#4x4 example
numbers = [[3,0,9,0],
		   [0,0,0,6],
		   [8,0,0,0],
		   [0,6,0,24]]

colors = [[0,1,0,1],
		  [0,0,0,0],
		  [0,1,0,1],
		  [0,0,0,0]]

curves = [["na","na","na","na"],
		  ["na","na","na","na"],
		  ["na","na","na","na"],
		  ["na","na","na","na"]]


green = (0.7,1,0.7)
white = (1,1,1)
smallPieceArea = (4-np.pi)/4
largePieceArea = np.pi/4
PRINTSTATEMENTS = False

archOptions = {
	"innerCell": {
		"left_right" : ["na","tl","tr","bl","br"],
		"right_left" : ["na","tl","tr","bl","br"],
		"above_below": ["na","tl","tr","bl","br"],
		"below_above": ["na","tl","tr","bl","br"]
	},
	"topEdge": {
		"left_right" : ["na_t","tl_t","br_t","tr","bl"],
		"right_left" : ["na_t","tr_t","bl_t","tl","tr"],
		"below_above": ["na_t","tl","tr","bl","br"],
	},
	"bottomEdge": {
		"left_right" : ["na_b","tr_b","bl_b","tl","br"],
		"right_left" : ["na_b","tl_b","br_b","tr","bl"],
		"above_below": ["na_b","tl","tr","bl","br"],
	},
	"leftEdge": {
		"right_left" : ["na_l","tl","tr","bl","br"],
		"above_below": ["na_l","tl_l","br_l","tr","bl"],
		"below_above": ["na_l","tr_l","bl_l","tl","br"]
	},
	"rightEdge": {
		"left_right" : ["na_r","tl","tr","bl","br"],
		"above_below": ["na_r","tr_r","bl_r","tl","br"],
		"below_above": ["na_r","tl_r","br_r","tr","bl"]
	},
	"topLeftCorner": {
		"right_left" : ["na_lt","bl_t","tr_t"],
		"below_above": ["na_lt","bl_l","tr_l"]
	},
	"topRightCorner": {
		"left_right" : ["na_rt","br_t","tl_t"],
		"below_above": ["na_rt","br_r","tl_r"]
	},
	"bottomLeftCorner": {
		"right_left" : ["na_lb","tl_b","br_b"],
		"above_below": ["na_lb","tl_l","br_l"],
	},
	"bottomRightCorner": {
		"left_right" : ["na_rb","tr_b","bl_b"],
		"above_below": ["na_rb","tr_r","bl_r"],
	},
}


directionsLookup = {
	"SOURCE": {"tl": [(0,1),(1,0)],"br": [(0,-1),(-1,0)],"bl": [(0,1),(-1,0)],"tr": [(0,-1),(1,0)],"na": [(0,1),(0,-1),(1,0),(-1,0)]},
	"left_right" : {"tl": [(-1,0)],"br": [(-1,0)],"bl": [(1,0)],"tr": [(1,0)],"na": [(0,1),(0,-1),(1,0),(-1,0)]},
	"right_left" : {"tl": [(1,0)],"br": [(1,0)],"bl": [(-1,0)],"tr": [(-1,0)],"na": [(0,1),(0,-1),(1,0),(-1,0)]},
	"above_below": {"tl": [(0,-1)],"br": [(0,-1)],"bl": [(0,1)],"tr": [(0,1)],"na": [(0,1),(0,-1),(1,0),(-1,0)]},
	"below_above": {"tl": [(0,1)],"br": [(0,1)],"bl": [(0,-1)],"tr": [(0,-1)],"na": [(0,1),(0,-1),(1,0),(-1,0)]},
	}


cellRelationLookup = {
	(0,1): "left_right", (0,-1): "right_left", (1,0): "above_below", (-1,0): "below_above", 
	(1,1): "topLeft_bottomRight", (-1,-1): "bottomRight_topLeft", (-1,1): "bottomLeft_topRight", (1,-1): "topRight_bottomLeft"
}

areaLookup = {
	"left_right" : {"na": 1, "tl": smallPieceArea, "tr": largePieceArea, "br": largePieceArea, "bl": smallPieceArea},
	"right_left" : {"na": 1, "tl": largePieceArea, "tr": smallPieceArea, "br": smallPieceArea, "bl": largePieceArea},
	"above_below": {"na": 1, "tl": smallPieceArea, "tr": smallPieceArea, "br": largePieceArea, "bl": largePieceArea},
	"below_above": {"na": 1, "tl": largePieceArea, "tr": largePieceArea, "br": smallPieceArea, "bl": smallPieceArea}
}


allArchs = ["tl","br","bl","br","na",
			"na_rb","na_lb","na_rt","na_lt","na_l","na_r","na_t","na_b",
			"tl_b","br_b","bl_b","tr_b",
			"tl_l","br_l","bl_l","tr_l",
			"tl_r","br_r","bl_r","tr_r",
			"tl_t","br_t","bl_t","tr_t"]



def checkDangling(currentCellArch,nextCellArch,cellRelation):
	ConnectionsNeeded = np.array([0,0,0,0]) #Top left corner, Top right corner, bottom right corner, bottom left corner
	currentCellArchPrefix = currentCellArch[0:2]
	currentCellArchSuffix = None
	if len(currentCellArch) >= 3:
		currentCellArchSuffix = currentCellArch[3:]

	ConnectionPoints = np.array([0,0,0,0])
	nextCellArchPrefix = nextCellArch[0:2]
	nextCellArchSuffix = None
	if len(nextCellArch) >= 3:
		nextCellArchSuffix = nextCellArch[3:]

	if currentCellArchPrefix == "tl":
		ConnectionsNeeded[1] = 1
		ConnectionsNeeded[3] = 1
	if currentCellArchPrefix == "tr":
		ConnectionsNeeded[0] = 1
		ConnectionsNeeded[2] = 1
	if currentCellArchPrefix == "br":
		ConnectionsNeeded[1] = 1
		ConnectionsNeeded[3] = 1
	if currentCellArchPrefix == "bl":
		ConnectionsNeeded[0] = 1
		ConnectionsNeeded[2] = 1
	if currentCellArchSuffix == "t":
		ConnectionsNeeded[0] = 1
		ConnectionsNeeded[1] = 1
	if currentCellArchSuffix == "r":
		ConnectionsNeeded[1] = 1
		ConnectionsNeeded[2] = 1
	if currentCellArchSuffix == "l":
		ConnectionsNeeded[0] = 1
		ConnectionsNeeded[3] = 1
	if currentCellArchSuffix == "b":
		ConnectionsNeeded[2] = 1
		ConnectionsNeeded[3] = 1
	if currentCellArchSuffix == "lb":
		ConnectionsNeeded[0] = 1
		ConnectionsNeeded[2] = 1
	if currentCellArchSuffix == "rb":
		ConnectionsNeeded[1] = 1
		ConnectionsNeeded[3] = 1
	if currentCellArchSuffix == "lt":
		ConnectionsNeeded[1] = 1
		ConnectionsNeeded[3] = 1
	if currentCellArchSuffix == "rt":
		ConnectionsNeeded[0] = 1
		ConnectionsNeeded[2] = 1

	if nextCellArchPrefix == "tl":
		ConnectionPoints[1] = 1
		ConnectionPoints[3] = 1
	if nextCellArchPrefix == "tr":
		ConnectionPoints[0] = 1
		ConnectionPoints[2] = 1
	if nextCellArchPrefix == "br":
		ConnectionPoints[1] = 1
		ConnectionPoints[3] = 1
	if nextCellArchPrefix == "bl":
		ConnectionPoints[0] = 1
		ConnectionPoints[2] = 1
	if nextCellArchSuffix == "t":
		ConnectionPoints[0] = 1
		ConnectionPoints[1] = 1
	if nextCellArchSuffix == "r":
		ConnectionPoints[1] = 1
		ConnectionPoints[2] = 1
	if nextCellArchSuffix == "l":
		ConnectionPoints[0] = 1
		ConnectionPoints[3] = 1
	if nextCellArchSuffix == "b":
		ConnectionPoints[2] = 1
		ConnectionPoints[3] = 1
	if nextCellArchSuffix == "lb":
		ConnectionPoints[0] = 1
		ConnectionPoints[2] = 1
	if nextCellArchSuffix == "rb":
		ConnectionPoints[1] = 1
		ConnectionPoints[3] = 1
	if nextCellArchSuffix == "lt":
		ConnectionPoints[1] = 1
		ConnectionPoints[3] = 1
	if nextCellArchSuffix == "rt":
		ConnectionPoints[0] = 1
		ConnectionPoints[2] = 1

	if cellRelation == "topLeft_bottomRight":
		if ConnectionsNeeded[2]+ConnectionPoints[0] == 2:
			if (currentCellArchPrefix,nextCellArchPrefix) in [("bl","bl"),("tr","tr")]:
				return 1
			else:
				return 0
	elif cellRelation == "bottomRight_topLeft":
		if ConnectionsNeeded[0]+ConnectionPoints[2] == 2:
			if (currentCellArchPrefix,nextCellArchPrefix) in [("bl","bl"),("tr","tr")]:
				return 1
			else:
				return 0
	elif cellRelation == "bottomLeft_topRight":
		if ConnectionsNeeded[1]+ConnectionPoints[3] == 2:
			if (currentCellArchPrefix,nextCellArchPrefix) in [("br","br"),("tl","tl")]:
				return 1
			else:
				return 0
	elif cellRelation == "topRight_bottomLeft":
		if ConnectionsNeeded[3]+ConnectionPoints[1] == 2:
			if (currentCellArchPrefix,nextCellArchPrefix) in [("br","br"),("tl","tl")]:
				return 1
			else:
				return 0
	elif cellRelation == "left_right":
		if ConnectionsNeeded[1]+ConnectionPoints[0] == 2:
			if (currentCellArchPrefix,nextCellArchPrefix) in [("tl","bl"),("br","bl"),("br","tr"),("bl","tl"),("tr","tl"),("tr","br")]:
				return 1
			else:
				return 0
		if ConnectionsNeeded[2]+ConnectionPoints[3] == 2:
			if (currentCellArchPrefix,nextCellArchPrefix) in [("tl","bl"),("br","bl"),("br","tr"),("bl","tl"),("tr","tl"),("tr","br")]:
				return 1
			else:
				return 0
	elif cellRelation == "right_left":
		if ConnectionsNeeded[0]+ConnectionPoints[1] == 2:
			if (nextCellArchPrefix,currentCellArchPrefix) in [("tl","bl"),("br","bl"),("br","tr"),("bl","tl"),("tr","tl"),("tr","br")]:
				return 1
			else:
				return 0
		if ConnectionsNeeded[3]+ConnectionPoints[2] == 2:
			if (nextCellArchPrefix,currentCellArchPrefix) in [("tl","bl"),("br","bl"),("br","tr"),("bl","tl"),("tr","tl"),("tr","br")]:
				return 1
			else:
				return 0
	elif cellRelation == "above_below":
		if ConnectionsNeeded[2]+ConnectionPoints[1] == 2:
			if (currentCellArchPrefix,nextCellArchPrefix) in [("tl","tr"),("br","bl"),("br","tr"),("bl","tl"),("bl","br"),("tr","tl")]:
				return 1
			else:
				return 0
		if ConnectionsNeeded[3]+ConnectionPoints[0] == 2:
			if (currentCellArchPrefix,nextCellArchPrefix) in [("tl","tr"),("br","bl"),("br","tr"),("bl","tl"),("bl","br"),("tr","tl")]:
				return 1
			else:
				return 0
	elif cellRelation == "below_above":
		if ConnectionsNeeded[0]+ConnectionPoints[3] == 2:
			if (nextCellArchPrefix,currentCellArchPrefix) in [("tl","tr"),("br","bl"),("br","tr"),("bl","tl"),("bl","br"),("tr","tl")]:
				return 1
			else:
				return 0
		if ConnectionsNeeded[1]+ConnectionPoints[2] == 2:
			if (nextCellArchPrefix,currentCellArchPrefix) in [("tl","tr"),("br","bl"),("br","tr"),("bl","tl"),("bl","br"),("tr","tl")]:
				return 1
			else:
				return 0

	#return None means the arch is dangling, we had no connections. 
	return None



class board(object):
	def __init__(self,numbers,colors,curves):
		self.numbers = numbers
		self.colors = colors
		self.curves = curves
		self.board = []
		self.board_dim = len(numbers)
		self.possiblePaths = []
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
		
	def getPossiblePaths(self):
		return self.possiblePaths

	def getPossibleCurves(self):
		possibleCurves = []
		for p in self.possiblePaths:
			possibleCurves.append(p["explored"])
		return possibleCurves

	def getCellNumber(self,i,j):
		return self.board[i][j]['number']

	def getCellColor(self,i,j):
		return self.board[i][j]['color']


	def CheckFeasible(self,currCell,tryCell,cellRelation,currPath,source,sourceNumber):
		if PRINTSTATEMENTS:
			print("\nCHECKING: ", currPath, "\nWITH: ", tryCell)

		tryCellArch = tryCell[2]
		currCellArch = currCell[2]
		tryCellArchPrefix = tryCellArch[0:2]
		currCellArchPrefix = currCellArch[0:2]

		if self.board[tryCell[0]][tryCell[1]]["curve"] != "na" and tryCellArchPrefix != self.board[tryCell[0]][tryCell[1]]["curve"][0:2]:
			if PRINTSTATEMENTS:
				print("\t FAILED FOR overwritting current arch")
			return None

		if self.getCellColor(tryCell[0],tryCell[1]) == green and tryCellArchPrefix != 'na':
			if PRINTSTATEMENTS:
				print("\t FAILED FOR assinging Green cell an arch")
			return None

		#check area
		addArea = areaLookup[cellRelation][tryCellArchPrefix]
		if currPath["area"] + addArea > sourceNumber:
			if PRINTSTATEMENTS:
				print("\t FAILED FOR too large area")
			return None

		#Check placing on a cell with a different number in a direction that includes it into the path.
		#Using area for this since area increase is based on directional relation, exactly what we need.
		if addArea in [largePieceArea,1] and self.getCellNumber(tryCell[0],tryCell[1]) != None:
			if self.getCellNumber(tryCell[0],tryCell[1]) != sourceNumber:
				if PRINTSTATEMENTS:
					print("\t FAILED FOR Number in Cell Check")
				return None


		addCont = 0
		if tryCellArch in ["na_lt","na_rt","na_lb","na_rb"]:
			addCont+=1
		if tryCellArchPrefix != "na":
			check = False
			#Get diagonal neighbors that are currently part of the constructed path
			explored_toExplore = []
			for i in currPath["toExplore"]:
				explored_toExplore.append(i)
			for i in currPath['explored']:
				explored_toExplore.append(i)
			neighbors = []
			for d in [(1,1),(-1,-1),(-1,1),(1,-1),(0,1),(1,0),(0,-1),(-1,0)]:
				neighbor = (d[0]+tryCell[0],d[1]+tryCell[1])
				for cell in explored_toExplore:
					if neighbor == (cell[0],cell[1]):
						relation = cellRelationLookup[d]
						neighbors.append((cell[0],cell[1],cell[2],relation))
			for neighbor in neighbors:
				t = checkDangling(tryCellArch,neighbor[2],neighbor[3])
				if t!= None:
					check = True
					addCont +=t

			if check == False:
				if PRINTSTATEMENTS:
					print("\t FAILED FOR dangling")
				return None
		

		# if currPath["cont"] + addCont > sourceNumber:
		# 	if PRINTSTATEMENTS:
		# 		print("\t FAILED FOR too large cont")
		# 	return None

		# if (currPath["cont"] + addCont) * (currPath["area"] + addArea) > sourceNumber:
		# 	if PRINTSTATEMENTS:
		# 		print("\t FAILED FOR too large cont times area")
		# 	return None

		if PRINTSTATEMENTS:
			print("CHECK PASSED, ADDING AREA: ", addArea, "ADDING CONT: ", addCont, "\n")

		return {"addArea": addArea, "addCont": addCont}



	def RecBuildPaths(self,currCell,nextCell,buildPaths,source,sourceNumber):
		newBuildPaths = []
		cellRelation = nextCell[2]
		c = self.board_dim-1
		if nextCell[0] == 0 and nextCell[1] == 0: #Top left corner
			aOptions = archOptions["topLeftCorner"][cellRelation]
		elif nextCell[0] == 0 and nextCell[1] == c: #Top right corner
			aOptions = archOptions["topRightCorner"][cellRelation]
		elif nextCell[0] == c and nextCell[1] == 0: #Bottom Left corner
			aOptions = archOptions["bottomLeftCorner"][cellRelation]
		elif nextCell[0] == c and nextCell[1] == c: #bottom right corner
			aOptions = archOptions["bottomRightCorner"][cellRelation]
		elif nextCell[1] == 0: #Left edge
			aOptions = archOptions["leftEdge"][cellRelation]
		elif nextCell[1] == c: #Right edge
			aOptions = archOptions["rightEdge"][cellRelation]
		elif nextCell[0] == 0: #Top Edge
			aOptions = archOptions["topEdge"][cellRelation]
		elif nextCell[0] == c: #Bottom Edge
			aOptions = archOptions["bottomEdge"][cellRelation]
		else:
			aOptions = archOptions["innerCell"][cellRelation]



		for path in buildPaths:
			for a in aOptions:
				tryCell = (nextCell[0],nextCell[1],a,nextCell[2])
				check = self.CheckFeasible(currCell,tryCell,cellRelation,path,source,sourceNumber)
				if check != None:
					copyCurrPath = copy.deepcopy(path)
					copyCurrPath['toExplore'].append(tryCell)
					copyCurrPath["area"] = copyCurrPath["area"] + check['addArea'] 
					copyCurrPath["cont"] = copyCurrPath["cont"] + check['addCont']
					newBuildPaths.append(copyCurrPath)
		return newBuildPaths
				

	def BuildPaths(self,currCell,neighborsFound,currPath,source,sourceNumber):
		newPaths = []
		buildPaths = [currPath]

		while neighborsFound:
			currentNeighbor = neighborsFound.pop()
			buildPaths = self.RecBuildPaths(currCell,currentNeighbor,buildPaths,source,sourceNumber)
		
		if PRINTSTATEMENTS:
			print("\t\t  FOUND NEW PATHS ", buildPaths)
		return(buildPaths)



	def RecBFS(self,currCell,toExplore,explored):
		currCell_row,currCell_col,currCell_arch,currCell_cameFrom = currCell[0],currCell[1],currCell[2],currCell[3]

		temp = []
		for i in toExplore:
			temp.append((i[0],i[1]))
		toExplore = temp
		temp= []
		for i in explored:
			temp.append((i[0],i[1]))
		explored = temp

		currCell_archPrefix = currCell_arch[0:2]
		directions = directionsLookup[currCell_cameFrom][currCell_archPrefix]

		neighborsFound = []
		for d in directions:
			nextCell = (currCell_row+d[0],currCell_col+d[1],cellRelationLookup[d])
			if (nextCell[0],nextCell[1]) not in explored and (nextCell[0],nextCell[1]) not in toExplore:
				if nextCell[0] >= 0 and nextCell[0] < self.board_dim and nextCell[1] >= 0 and nextCell[1] < self.board_dim:
					neighborsFound.append(nextCell)
					if PRINTSTATEMENTS:
						print("\t FOUND NEIGHBOR", nextCell)
		return(neighborsFound)



	def BFS(self,source):
		
		allPathsRecords = []
		allPathsData = deque()
		source_row,source_col = source[0],source[1]
		sourceNumber = self.getCellNumber(source_row,source_col)

		#initialize possible paths based on source node location
		#Hardcoded cases for now
		if source == (0,0): #top left corner
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "na_lt", "SOURCE")]), "area": 1, "cont": 2})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "tr_l", "SOURCE")]), "area": largePieceArea, "cont": 2})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "bl_t", "SOURCE")]), "area": largePieceArea, "cont": 2})
		elif source == (self.board_dim-1,self.board_dim-1): #bottom right corner
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "na_rb", "SOURCE")]), "area": 1, "cont": 2})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "tr_b", "SOURCE")]), "area": largePieceArea, "cont": 2})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "bl_r", "SOURCE")]), "area": largePieceArea, "cont": 2})
		elif source[1] == self.board_dim-1: #right edge
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "tl_r", "SOURCE")]), "area": largePieceArea, "cont": 2})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "br",   "SOURCE")]), "area": largePieceArea, "cont": 1})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "bl_r", "SOURCE")]), "area": largePieceArea, "cont": 2})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "tr",   "SOURCE")]), "area": largePieceArea, "cont": 1})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "na_r", "SOURCE")]), "area": 1, "cont": 1})
		elif source[1] == 0: #left edge
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "br_l", "SOURCE")]), "area": largePieceArea, "cont": 2})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "tl",   "SOURCE")]), "area": largePieceArea, "cont": 1})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "tr_l", "SOURCE")]), "area": largePieceArea, "cont": 2})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "bl",   "SOURCE")]), "area": largePieceArea, "cont": 1})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "na_l", "SOURCE")]), "area": 1, "cont": 1})
		elif source[0] == self.board_dim-1: #bottom edge
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "tr_b", "SOURCE")]), "area": largePieceArea, "cont": 2})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "br",   "SOURCE")]), "area": largePieceArea, "cont": 1})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "tl_b", "SOURCE")]), "area": largePieceArea, "cont": 2})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "bl",   "SOURCE")]), "area": largePieceArea, "cont": 1})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "na_b", "SOURCE")]), "area": 1, "cont": 1})
		elif source[0] == 0: #top edge
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "br_t", "SOURCE")]), "area": largePieceArea, "cont": 2})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "tl",   "SOURCE")]), "area": largePieceArea, "cont": 1})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "bl_t", "SOURCE")]), "area": largePieceArea, "cont": 2})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "tr",   "SOURCE")]), "area": largePieceArea, "cont": 1})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "na_t", "SOURCE")]), "area": 1, "cont": 1})
		else:
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "tl", "SOURCE")]), "area": largePieceArea, "cont": 1})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "br", "SOURCE")]), "area": largePieceArea, "cont": 1})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "bl", "SOURCE")]), "area": largePieceArea, "cont": 1})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "tr", "SOURCE")]), "area": largePieceArea, "cont": 1})
			allPathsData.append({"explored": [], "toExplore":deque([(source_row,source_col, "na", "SOURCE")]), "area": 1, "cont": 1})

			
		if PRINTSTATEMENTS:
			print("INITIAL PATH DATA")
			for p in allPathsData:
				print(p)
			print("\n\n\n")

		while allPathsData:
			path = allPathsData.popleft()
			if PRINTSTATEMENTS:
				print("EXPLORING PATH ", path)
			toExplore = path["toExplore"]
			explored = path["explored"]
			if path not in allPathsRecords:
				allPathsRecords.append(path)
			while toExplore:
				currentCell = toExplore.popleft()
				explored.append(currentCell)
				if PRINTSTATEMENTS:
					print("EXPLORING CELL ", currentCell)
				neighborsFound = self.RecBFS(currentCell,toExplore,explored)
				if PRINTSTATEMENTS:
					print("\t\tBUILDING PATHS WITH ", neighborsFound)
				newPaths = self.BuildPaths(currentCell,neighborsFound,path,source,sourceNumber)
				for p in newPaths:
					allPathsData.appendleft(p)
			if PRINTSTATEMENTS:
				print("CURRENT PATH DATA")
				for p in allPathsData:
					print(p)
				print("\n\n\n")
				print("CURRENT PATH RECORD")
				for p in allPathsRecords:
					print(p)
				print("\n\n\n")
		for p in allPathsRecords:
			self.possiblePaths.append(p)
				


def drawArch(arch,i,j,cell_size):
	if arch == "tl":
		a = 180
		x,y = (j+1)*cell_size,(i+1)*cell_size
	elif arch == "tr":
		a = 270
		x,y = (j)*cell_size,(i+1)*cell_size
	elif arch == "bl":
		a = 90
		x,y = (j+1)*cell_size,(i)*cell_size
	elif arch == "br":
		a = 0
		x,y = (j)*cell_size,(i)*cell_size
	return patches.Arc((x,y),cell_size*2,cell_size*2,angle=a,theta1=0,theta2=90,lw=2,color="red")


'''
Note: our board is stored row,col but visual draws on the x,y plane. We use arr[j][i] to flip to x,y interpretation for drawing purposes.
For archs, we handle the flip in the drawArch function, hence we pass arr[i][j] for drawArch call.
'''
def visual(arr,num_rows=4,num_cols=4,cell_size=16,cell_color='white',edge_color='black',animate=False):
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
			if arr[i][j]["curve"][0:2] != "na" and arr[i][j]["curve"][0:2] != "RD":
				arch = drawArch(arr[i][j]["curve"][0:2],i,j,cell_size)
				archs.append(arch)
			elif arr[i][j]["curve"][0:2] == "RD":
				ax.add_patch(plt.Rectangle([j*cell_size+4, i*cell_size+4], cell_size/3, cell_size/3, facecolor="red",zorder=2))
			if arr[i][j]["curve"][3:] == "l":
				ax.add_patch(plt.Rectangle([j*cell_size, i*cell_size], 0.5, cell_size, facecolor="red",zorder=2))
			elif arr[i][j]["curve"][3:] == "r":
				ax.add_patch(plt.Rectangle([j*cell_size+16, i*cell_size], 0.5, cell_size, facecolor="red",zorder=2))
			elif arr[i][j]["curve"][3:] == "t":
				ax.add_patch(plt.Rectangle([j*cell_size, i*cell_size], cell_size, 0.5, facecolor="red",zorder=2))
			elif arr[i][j]["curve"][3:] == "b":
				ax.add_patch(plt.Rectangle([j*cell_size, i*cell_size+16], cell_size, 0.5, facecolor="red",zorder=2))
			elif arr[i][j]["curve"][3:] == "lt":
				ax.add_patch(plt.Rectangle([j*cell_size, i*cell_size], 0.5, cell_size, facecolor="red",zorder=2))
				ax.add_patch(plt.Rectangle([j*cell_size, i*cell_size], cell_size, 0.5, facecolor="red",zorder=2))
			elif arr[i][j]["curve"][3:] == "rt":
				ax.add_patch(plt.Rectangle([j*cell_size+16, i*cell_size], 0.5, cell_size, facecolor="red",zorder=2))
				ax.add_patch(plt.Rectangle([j*cell_size, i*cell_size], cell_size, 0.5, facecolor="red",zorder=2))
			elif arr[i][j]["curve"][3:] == "lb":
				ax.add_patch(plt.Rectangle([j*cell_size, i*cell_size], 0.5, cell_size, facecolor="red",zorder=2))
				ax.add_patch(plt.Rectangle([j*cell_size, i*cell_size+16], cell_size, 0.5, facecolor="red",zorder=2))
			elif arr[i][j]["curve"][3:] == "rb":
				ax.add_patch(plt.Rectangle([j*cell_size+16, i*cell_size], 0.5, cell_size, facecolor="red",zorder=2))
				ax.add_patch(plt.Rectangle([j*cell_size, i*cell_size+16], cell_size, 0.5, facecolor="red",zorder=2))
	for arch in archs:
		ax.add_patch(arch)

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


b = board(numbers,colors,curves)
source = (3,3)
sourceNumber = b.getCellNumber(source[0],source[1])
b.BFS(source)

possibleCurves = b.getPossiblePaths()
print("Number of explored paths: ", len(possibleCurves))

for p in possibleCurves:
	#if p["area"] * p["cont"] == sourceNumber:
	print(p)
	newBoard = board(numbers,colors,curves)
	for c in p['explored']:
		if c[2] == "na":
			makeNaRed = (c[0],c[1],"RD")
		else:
			makeNaRed = c
		newBoard.updateCurve(makeNaRed[0],makeNaRed[1],makeNaRed[2])
	visual(newBoard.board, num_rows=newBoard.board_dim, num_cols=newBoard.board_dim,animate=True)

visual(b.board, num_rows=b.board_dim, num_cols=b.board_dim)
