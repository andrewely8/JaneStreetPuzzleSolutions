import sympy
from sympy.solvers import solve
from sympy import symbols
import pprint
from collections import defaultdict
from collections import deque
a,b,c,x = symbols('a b c x')

#expressions = [{'eq': <sympyExpression>, 'row': rowIndex, 'col': colIndex},...]
expressions = [
{'eq':6*c-4*b,'row': 0, 'col': 4},
{'eq':8-b,'row': 1, 'col': 7},
{'eq':(a**b-4)/(6*c+1),'row': 2, 'col': 1},
{'eq':(b+c)/(c-1),'row': 2, 'col': 3},
{'eq':b**2 - b/c,'row': 2, 'col': 6},
{'eq':((30+a)**(1/2))/(c),'row': 2, 'col': 8},
{'eq':(a+b)/(c-3*a),'row': 2, 'col': 10},
{'eq':(b-3*a)/(a-c),'row': 3, 'col': 4},
{'eq':8*a-2*b,'row': 3, 'col': 7},
{'eq':b/(a-c),'row': 3, 'col': 9},
{'eq':(b+9)/((c-a)**(1/2)),'row': 3, 'col': 11},
{'eq':18/(a*c+1),'row': 4, 'col': 1},
{'eq':c**b,'row': 4, 'col': 5},
{'eq':(3+b**2)/((3+2*c)**(1/2)),'row': 4, 'col': 10},
{'eq':b/(a**2-c**2),'row': 5, 'col': 3},
{'eq':((a+2)**(1/2))/a,'row': 5, 'col': 12},
{'eq':a**b-12/a,'row': 6, 'col': 2},
{'eq':2*c+c/a,'row': 6, 'col': 4},
{'eq':4*a-5*b,'row': 6, 'col': 6},
{'eq':c+2*a,'row': 6, 'col': 8},
{'eq':b/(9*a-5*c),'row': 6, 'col': 10},
{'eq':(b**3+2*c)/(b+2*c),'row': 7, 'col': 0},
{'eq':b/(a-1),'row': 7, 'col': 9},
{'eq':(c-b)/(2*a),'row': 8, 'col': 2},
{'eq':b/(a-c),'row': 8, 'col': 7},
{'eq':(b+c)/(a-c),'row': 8, 'col': 11},
{'eq':sympy.log(a,c),'row': 9, 'col': 1},
{'eq':(c**2-b)/(a),'row': 9, 'col': 3},
{'eq':(b-1)**2,'row': 9, 'col': 5},
{'eq':((43-a*c)**(1/3))/(a),'row': 9, 'col': 8},
{'eq':(b-a)/(a-c),'row': 10, 'col': 2},
{'eq':11-b,'row': 10, 'col': 4},
{'eq':(b-2*a)/(a-c),'row': 10, 'col': 6},
{'eq':(c+3)/a,'row': 10, 'col': 9},
{'eq':8*c-b/c,'row': 10, 'col': 11},
{'eq':b**2,'row': 11, 'col': 5},
{'eq':(2**b+1)/(a*c),'row': 12, 'col': 8},
]


# eq1 = c**(-2)-x
# eq2 = 6*c+8

# for i in range(18):
# 	sol = solve(eq1.subs({x:i}))
# 	print('\n\nif equation c^b = ', i, ' then c is one of: ', sol)

# 	for s in sol:
# 		print('if c = ', s, 'then 6c-4b = ', eq2.subs({c:s}))

# c_options = [-1 , -1/2 , 1/2 , -1/3 , 1/3 ]
# eq1 = (-2+c)/(c-1)

# for i in c_options:
# 	print('c = ', i, 'eq =', eq1.subs(c,i))

# c_options = [-1 , 1/2 , 1/3 ]
# eq1 = 8*c - (-2)/c

# for i in c_options:
# 	print('c = ', i, 'eq =', eq1.subs(c,i))

# eq1 = 3.25/a - x
# eq2 = 8*a+6

# for i in range(18):
# 	sol = solve(eq1.subs({x:i}))
# 	print('\n\nif equation (c^2-b)/a = ', i, ' then a is one of: ', sol)

# 	for s in sol:
# 		print('if a = ', s, 'then 8a-2b = ', eq2.subs({a:s}))
# 	

# i = 1
# for expr in expressions:
# 	print(i, '    ', expr.subs({b:-3,c:0.5,a:0.25}))
# 	print('\n')
# 	i+=1


def isValid(row,col):
	if row < 0 or row > 12 or col < 0 or col > 12:
		return False
	if grid[row][col] != '_':
		return False
	return True

def dfs(targetNum,remaining,currentRow,currentCol):
	currentPath.append((currentRow,currentCol))
	print(f'\n currently at cell {currentRow}, {currentCol} with remaining={remaining} ')
	print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
	print(f'\n current path: {currentPath}')
	print('\n\n\n')

	if remaining == 0:
		#We also need to check if this path contains all the required cells
		save = True
		for req in required[targetNum]:
			if req not in currentPath:
					save = False
		if save:
			print('**save path**') #We need a way to save this current grid
		grid[currentRow][currentCol] = '_'
		currentPath.pop()
		return

	for direction in directions:
		if isValid(currentRow+direction[0],currentCol+direction[1]):
			grid[currentRow+direction[0]][currentCol+direction[1]] = targetNum
			dfs(targetNum,remaining-1,currentRow+direction[0],currentCol+direction[1])

	 #We searched all neighbors, but there is still remaining space. We should preform a DFS from the node we came from originally, with this remaining space.
	#We also need to clear this cell once we finish the origin cell DFS with leftover remaining space.
	# if remaining != 0:
	# 	tmp = currentPath.pop()
	# 	orig = currentPath.pop()
	# 	currentPath.appendleft(tmp)
	# 	#orig = currentPath[-2] # last element of currentPath is our current cell, we want the previous one which is second to last.
	# 	dfs(targetNum,remaining,orig[0],orig[1]) 

grid = [['_' for _ in range(13)] for _ in range(13)]
directions = [(-1,0),(1,0),(0,-1),(0,1)]

for expr in expressions:
	grid[expr['row']][expr['col']] = round(expr['eq'].subs({a:0.25,b:-3,c:0.5}))


required = {}
for i in range(1,17):
	required[i] = []
for row in range(len(grid)):
	for col in range(len(grid[row])):
		if grid[row][col] != '_':
			required[grid[row][col]].append((row,col))

print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
print('\n\n\n')


target = 1
for i in range(1,17):
	for row in range(len(grid)):
		for col in range(len(grid[row])):
			if grid[row][col] == target:
				currentPath = deque()
				if target == 4: #for testing search around 4
					dfs(target,target-len(required[i]),row,col)
				target += 1

