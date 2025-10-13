import random
import numpy as np
from sympy import symbols,Eq,solve

atBats = 1000
games = 50

def Simulate(pitcherDecision,batterDecision,homerunProbabilty):
	
	total = 0
	fullCounts = 0
	
	#Simulate games:
	for game in range(games):
		score = 0
		#Simulate at bats
		for atBat in range(atBats):

			count = [0,0]
			pitcherStrike = False
			batterSwing = False
			while count[0] < 4 and count[1] < 3:
				randomNumber = random.randint(1,100) / 100
				
				if pitcherDecision >= randomNumber:
					pitcherStrike = True
				if batterDecision >= randomNumber:
					batterSwing = True

				if pitcherStrike and batterSwing:
					if homerunProbabilty >= randomNumber:
						score+=4
						count[0] = 5
					else:
						count[1]+=1
				elif pitcherStrike and not batterSwing:
					count[1]+=1
				elif not pitcherStrike and batterSwing:
					count[1]+=1
				elif not pitcherStrike and not batterSwing:
					count[0]+=1

				if count[0] == 4:
					score+=1
				if count[0] == 3 and count[1] == 2:

					fullCounts+=1
		total+=score

	return([int(total/games),fullCounts])


def MixedOptimal(p):
	print("---------------------------")
	print("Probabilty of Homerun: ", p)
	res1 = []
	for i in range(11):
		t = i/10
		diff = []
		for j in range(11):
			s = j/10
			simulation = Simulate(t,s,p)
			diff.append(simulation[0])
		print("With Pitcher fixed at t= ", t, " : ", diff)
		res1.append(max(diff)-min(diff))

	print("res  ", res1, "  selecting t = ", res1.index(min(res1))/10)

	res2 = []
	for i in range(11):
		s = i/10
		diff = []
		for j in range(11):
			t = j/10
			simulation = Simulate(t,s,p)
			diff.append(simulation[0])
		print("With Batter fixed at s= ", s, " : ", diff)
		res2.append(min(diff)-max(diff))

	print("res  ", res2, "  selecting s = ", res2.index(min(res2))/10)

	return([res1.index(min(res1))/10,res2.index(min(res2))/10])


def Test1():

	decimalPrecision = 2
	bestTrial = 0
	bestTrialP = 0
	bestExpectedFullCount = 0
	bestExpectedP = 0

	for i in range(0,10**decimalPrecision+1):

		p = i / 10**decimalPrecision	
		t = 7 / (52*p+7)
		s = 7 / (52*p+7)


		print("trial: p = ", p, " s = ", s, " t = ", t)

		fullCountExpected = (((1-t)*(1-s))**3)*((t)*(1-s)+(t)*(s)*(1-p)+(1-t)*(s))**2
		if fullCountExpected > bestExpectedFullCount:
			bestExpectedFullCount = fullCountExpected
			bestExpectedP = p
		print("fullCountExpected     = ", fullCountExpected) 
		trial = Simulate(t,s,p)
		print("Simulation: fullCount = ", trial[1], "    Score = ", trial[0])
		if trial[0] > bestTrial:
			bestTrial = trial[0]
			bestTrialP = p
		print("")

	print("---------")
	print("simulation: highest fullCount occured with p = ", bestTrialP)
	print("simulation: highest fullCount = ", bestTrial)
	print("calculation: highest expectedFullcount = ", bestExpectedFullCount)
	print("calculation: highest expectedFullcount occured with p = ", bestExpectedP)



def Test3(p):

	W = [[-1 for _ in range(4)] for _ in range(5)]
	W[-1] = [1,1,1,1]
	for row in W:
		row[-1] = 0
	W[-1][-1] = np.nan


	for row in range(len(W)-2,-1,-1):
		for col in range(len(W[row])-2,-1,-1):
			W[row][col] = min((1-p)*W[row][col+1]+4*p,max(W[row][col+1],W[row+1][col]))		

	P = [[-1 for _ in range(4)] for _ in range(5)]

	for row in range(len(P)-2,-1,-1):
		for col in range(len(P[row])-2,-1,-1):
			A = (1-p)*W[row][col+1]+4*p
			B = W[row][col+1]
			D = W[row+1][col] 

			if P[row][col] <= 0 or P[row][col] >= 1 or (D-B)/(A-2*B+D) == 0:
				print('pure')
			else:
				P[row][col] = (D-B)/(A-2*B+D)
	
	if p == 0.1 or p == 0.25 or p == 0.33 or p == 0.5 or p == 0.8:
		print("W(a,b) Matrix")
		print(np.array(W))
		print("")

		print(np.array(P))

		print("----------------")






W = [[-12,-11,-10, 0],
	 [-9,-8,-7, 0],
	 [-6,-5,-4, 0],
	 [-3,-2,-1, 0],
	 [ 1, 1, 1   ]]

OPT = [[-12,-11,-10],
	   [-9,-8,-7],
	   [-6,-5,-4],
	   [-3,-2,-1]]

def SolveTable(W_a_bplus1,W_aplus1_b):
	t = symbols('t')
	s = symbols('s')
	p = symbols('p')
	strike_swing = (1-p)*W_a_bplus1 +4*p
	nashEq = [[strike_swing,W_a_bplus1],[W_a_bplus1,W_aplus1_b]]
	
	payoff_batter_swing = t*nashEq[0][0] + (1-t)*nashEq[1][0]
	payoff_batter_wait =  t*nashEq[0][1] + (1-t)*nashEq[1][1]
	payoff_pitcher_strike = s*nashEq[0][0] + (1-s)*nashEq[0][1]
	payoff_pitcher_ball =  s*nashEq[1][0] + (1-s)*nashEq[1][1]

	t = (W_aplus1_b-W_a_bplus1)/(strike_swing-2*W_a_bplus1+W_aplus1_b)  # t=s always 

	v = (strike_swing*W_aplus1_b - W_a_bplus1**2)/(strike_swing - 2*W_a_bplus1+W_aplus1_b)
	
	return [v,t]


for row in range(len(W)-2,-1,-1):
		for col in range(len(W[row])-2,-1,-1):
			W[row][col],OPT[row][col] = SolveTable(W[row][col+1],W[row+1][col])
			

p = symbols('p')


solW = [[-12,-11,-10, 0],
	    [-9,-8,-7, 0],
	    [-6,-5,-4, 0],
	    [-3,-2,-1, 0],
	    [ 1, 1, 1   ]]

solOPT = [[-12,-11,-10],
	      [-9,-8,-7],
	      [-6,-5,-4],
	      [-3,-2,-1]]

solP = [[   1,  -1,  -2],
	    [  -3,  -4,  -5],
	    [  -6,  -7,  -8],
	    [  -9, -10, -11]]

P = [[   1,  -1,  -2],
	 [  -3,  -4,  -5],
	 [  -6,  -7,  -8],
	 [  -9, -10, -11]]

for row in range(len(P)):
	for col in range(len(P[row])):
		if row == 0 and col == 0:
			pass
		elif row == 0:
			P[row][col] = P[row][col-1]*(2)*(OPT[row][col-1])*(1-OPT[row][col-1])+(1-p)*OPT[row][col-1]**2
		elif col == 0:
			P[row][col]=P[row-1][col]*(1-OPT[row-1][0])**2
		else:
			P[row][col] = (P[row-1][col])*((1-OPT[row-1][col])**2)+(P[row][col-1])*(2*(OPT[row][col-1])*(1-OPT[row][col-1])+(1-p)*OPT[row][col-1]**2)

decimalPrecision = 3


best = 0
bestP = 0
j=0

#for i in range(1,10**decimalPrecision+1):
for i in range(20000,30001):
	#homerunProbabilty = i / 10**decimalPrecision
	homerunProbabilty = i / 100000
	
	for row in range(len(W)-2,-1,-1):

			for col in range(len(W[row])-2,-1,-1):
				solW[row][col] = W[row][col].subs(p,homerunProbabilty).evalf()
				solOPT[row][col] = OPT[row][col].subs(p,homerunProbabilty).evalf()
				if row>0:
					solP[row][col] = P[row][col].subs(p,homerunProbabilty).evalf()
				elif col > 0:
					solP[row][col] = P[row][col].subs(p,homerunProbabilty).evalf()

			if solP[3][2]  > best:
				best = solP[3][2]
				bestP = homerunProbabilty

	if decimalPrecision <= 2:
		print("With Homerun Probabilty: p= ", homerunProbabilty)
		print("Expected value for final game score at each possible count (balls,strikes): ")
		for row in solW:
			print(row)
		print("")
		print("optimal mixed strategies (assuming t=s always) at each possible count (balls,strikes): ")
		for row in solOPT:
			print(row)
		print("")
		print("probabilities of counts occuring:")
		for row in solP:
			print(row)
		print("")
		print("PROBABILITY OF COUNT=(3,2): ", solP[3][2])
		print("------------------------------------")
		print("\n\n")
	else:
		#if homerunProbabilty in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]:
		if homerunProbabilty in [0.21,0.22,0.23,0.24,0.25,0.26,0.27,0.28,0.29]:
			j+=10
			print('progress: ', j,"%")
			


print("highest Probability for full count: ", best, "  occurred with homerun probability p= ", bestP)