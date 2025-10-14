import numpy as np
from sympy import symbols,Eq,solve

W = [[0, 0, 0, 0],
	 [0 ,0, 0, 0],
	 [0, 0, 0, 0],
	 [0, 0, 0, 0],
	 [1, 1, 1   ]]

OPT = [[0, 0, 0],
	   [0, 0, 0],
	   [0, 0, 0],
	   [0, 0, 0]]

P = [[1, 0, 0],
	 [0, 0, 0], 
	 [0, 0, 0],
	 [0, 0, 0]]


def compute(p):

	#Finds optimal mixed strategy and expected score for a p,
	#based on the expected value resulting from going to the next strike count (W_a_bplus1)
	#and the the expected value resulting from going to the next ball count (W_aplus1_b)
	def SolveTable(W_a_bplus1,W_aplus1_b):
		A = (1-p)*W_a_bplus1 +4*p
		B = W_a_bplus1
		D = W_aplus1_b
		t = (D-B)/(A-2*B+D)  # t=s always 
		v = (A*D - B**2)/(A - 2*B+D)
		return [v,t]

	#Fill our expected value of scores matrix. We go backwards since we know last column is all 0s and last row is all 1s.
	#Opt matrix shape "fits into" the top left portion of the W matrix we iterate over.
	for row in range(len(W)-2,-1,-1):
		for col in range(len(W[row])-2,-1,-1):
			W[row][col],OPT[row][col] = SolveTable(W[row][col+1],W[row+1][col])

	#Fill our probability table
	for row in range(len(P)):
		for col in range(len(P[row])):
			if row == 0 and col == 0: #skip over the top left entry which is initialized to 1 since count (0,0) always happens
				pass
			elif row == 0: #Top row: all strikes are thrown
				P[row][col] = P[row][col-1] * (2*OPT[row][col-1]*(1-OPT[row][col-1])+(1-p)*(OPT[row][col-1]**2))
			elif col == 0: #First column: all balls are thrown
				P[row][col]=  P[row-1][col] * ((1-OPT[row-1][col])**2)
			else:          #Inner entires: mix of strikes and balls
				P[row][col] = (P[row-1][col] * ((1-OPT[row-1][col])**2)) + ((P[row][col-1]) * (2*OPT[row][col-1]*(1-OPT[row][col-1])+(1-p)*(OPT[row][col-1]**2)))

	#Return the probabilty we reach 3 balls and 2 strikes, a full count
	return(P[3][2])

print(compute(0.226))
