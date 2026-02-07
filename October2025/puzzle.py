#Finds optimal mixed strategy and expected score for a p,
#based on the expected value resulting from going to the next strike count (W_a_bplus1)
#and the the expected value resulting from going to the next ball count (W_aplus1_b)
def compute(p):

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

	def SolveTable(W_a_bplus1,W_aplus1_b):
		A = (1-p)*W_a_bplus1 +4*p
		B = W_a_bplus1
		D = W_aplus1_b
		t = (D-B)/(A-2*B+D)  # t=s always 
		v = (A*D - B**2)/(A - 2*B+D)
		return [v,t]

	#Fill our expected value of scores matrix. We go backwards since we know last column is all 0s and last row is all 1s.
	#Opt matrix shape "fits into" the top left portion of the W matrix we iterate over. (even though they aren't same dimension)
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


#We need accuracy to 10 decimal places for p, so we need to narrow our search space down.
#tr : top range as an integer
#br : bottom range as an integer
#per : decimal percision as an integer
def Trial(br, tr, per):
	
	best = 0
	bestP = 0
	prog = 0
	progStep = (tr-br)/10
	progPoints = [br,br+progStep,br+progStep*2,br+progStep*3,br+progStep*4,br+progStep*5,br+progStep*6,br+progStep*7,br+progStep*8,br+progStep*9,tr]

	for i in range(br,tr):
		p = i/per
		c = compute(p)
		
		if c > best:
			best = c
			bestP = p

		if i in progPoints:
			prog+=10
			print(f"Progress: {prog}%")

	return(best, bestP)

# We want 10 decimal places of accuracy which is 10,000,000,000 disctinct options for p.
# if we start from p=0 we get division by 0 errors. But we know p won't be 0 so we can just start from bottom range + 1.
# Our top range is exclusive so we need to go to topRange+1
# Theres ways we could automate prunning for this value but lets just 'semi-manually' do it...

#print(Trial(1,101,100)) # ->                       (0.29594350457912, 0.23)        fast
#print(Trial(1,1001,1000)) # ->                     (0.29596799145239616, 0.227)    fast
#print(Trial(1,10001,10000)) # ->                   (0.29596799145239616, 0.227)    fast
#print(Trial(1,100001,100000)) # ->                 (0.29596799334624274, 0.22697)  fast
#print(Trial(1,10000001,10000000)) # ->             (0.2959679933742692, 0.2269732) slow
#print(Trial(224443000,229503010,1000000000)) # ->  (0.2959679933742721, 0.226973229) slow, but accurate up to 12 decimal places.

#Final probabilty for homerun:    0.226973229
#Final probabilty for full count: 0.2959679933742721

print("Maximum probability count reaches (3,2): ", compute(0.226973229))
