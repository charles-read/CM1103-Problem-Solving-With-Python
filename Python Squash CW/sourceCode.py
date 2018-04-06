import random
import csv
import matplotlib.pyplot as plt
#Q1a--------------------------------------------------------------------------

def game(ra, rb):
	probA = ra / (ra + rb) #implemented Probability A win point formula.
	pointsA = 0
	pointsB = 0
	winPoint = 11 #Points required to win game.
	#while ahead by least 2 points and under winpoint(11)
	while abs(pointsA-pointsB)<2 or (pointsA<winPoint and pointsB<winPoint):
		prob = random.random() #probability between 0 and 1.
		if prob < probA:
			pointsA += 1 #adds point to player A.
		else:
			pointsB += 1 #adds point to player B.
	return(pointsA, pointsB) #returns score of game.

#random.seed(57)
#game(70,30)

#Q1b--------------------------------------------------------------------------

def winProb(ra, rb, n): #simulates n games to calc probability.
	pointCount = 0
	for matches in range(n):
		pointsA, pointsB = game(ra, rb) #calls game function to get score of 1 game.
		if pointsA > pointsB:
			pointCount += 1
	prob = round((pointCount / n), 2) #divides count by n to give prob. Rounded 2 dp.
	return prob

#random.seed(57)
#winProb(70, 30, 150)

#Q1c--------------------------------------------------------------------------

def listTuples(myfile): 
	data = list() #List initialized.
	with open(myfile) as csvfile: #opens csv file in correct format.
			rdr = csv.reader(csvfile)
			next(rdr)#skips first rows
			for a in rdr:
				data.append((int(a[0]), int(a[1]))) # places data into tuple w/ comma.
	return data #prints tuple data from csv file.

#listTuples("test.csv")

#Q1d--------------------------------------------------------------------------

def plotGraph(myList):
	X = list();Y = list() #Lists initialized.
	for num in myList: #adds values from 'myList'.
		X.append(winProb(int(num[0]), int(num[1]), 1000)) #uses winProb to plot probability of A win.
		Y.append(int(num[0]) / int(num[1]))
	plt.title('The probability of a player A win, against the relative abilities of players A & B')
	plt.xlabel('Probability of A Win')
	plt.ylabel('ra/rb')
	plt.axis([0,1,0,4])
	plt.plot(X, Y, 'bx') #plots lists in blue crosses.
	plt.show()

#plotGraph([(60, 20), (100, 55), (50, 40), (20, 70), (95, 85)])

#Q1e--------------------------------------------------------------------------

def simProb(ra, rb, prob): #calculates minimum games for given probability.
	n = 1
	#While 1 - Probability of 'A' to the power of n is less than Probability(0.9):
	while (1 - (ra / (ra + rb))**n) < prob:
		n += 1 #add 1 to count ns.
	return n
#5 is produced from this function if 'simProb(60,40,0.9)' is entered.
#this means 5 games is the minimum games that is required so a wins with a probability of a/

#simProb(60,40,0.9)

#Q2------------------------------------------------------------------------------

def engGame(ra, rb): #engGame returns score and rallies in English scoring.
	probA = ra / (ra + rb)
	server = 'q' #Values initialized.
	pointsA = 0 ;pointsB = 0
	winPoint = 9
	rallies = 0
	gameOver = False #game status.
	while gameOver == False:
		ran = random.random() #Generates pseudo random numbers from 0 to 1
		if ran < probA:
			if  server == 'a': #if A wins rally server, point acquired.
				pointsA += 1
			else:
				server = 'a'
		else:
			if server == 'b': #if B wins rally server, point acquired.
				pointsB += 1
			else:
				server = 'b'
		if pointsA == 8 and pointsB == 8: #if score is 8-8.
			if ran < 0.5: #random chance of playing on to 10.
				winPoint = 10
		rallies += 1
		reached_winPoint = (pointsA == winPoint) or (pointsB == winPoint)
		if reached_winPoint:
			gameOver = True	#game finishes and values returned.
	return pointsA, pointsB, rallies

def parsGameRallies(ra, rb, n): #outputs PARS rallies for Q2.
	ralliesP = 0
	for matches in range(n):
		pointsA, pointsB = game(ra, rb) #calls 1a function. Calcs score of game.
		ralliesP += (pointsA + pointsB)
	ralliesP = round((ralliesP / n),2) #divides count by n to give average rallies for match.
	return ralliesP
def engGameRallies(ra, rb, n): #outputs English rallies for Q2.
	ralliesE = 0
	for matches in range(0, n):
		temp = engGame(ra, rb)[2] #calls the engGame function.
		ralliesE += temp     	
	ralliesE = round((ralliesE / n),2) #divides count by n to give average rallies for match.
	return ralliesE


def scoringPlot(): #plots English vs PARS scoring system time vs relative ability.
	playerRange = listTuples('relativeAbilityRange.csv') #range using CSV file, contains player range from 0-9.
	engRallies=list(); parsRallies=list(); RA=list();
	for i in playerRange: #loops through CSV, adds values to lists from rally values.
		engRallies.append(engGameRallies(i[0], i[1], 10000))
		parsRallies.append(parsGameRallies(i[0], i[1], 10000)) 
		RA.append(i[0] / i[1])
	plt.plot(RA,engRallies,'b--',label='English Scoring') #plots points for relative ability VS English scoring rally. Adds legend labels.
	plt.plot(RA,parsRallies,'r--',label='Point-a-rally Scoring (PARS)') #plots points for relative ability VS pars scoring rally. Adds legend labels.
	plt.legend(loc='upper right')
	plt.axis([0,10,0,35])
	plt.xlabel('Relative abilities of the two players (ra / rb)');plt.ylabel('Average length of match in minutes.') #X and Y axes labeled correspondingly.
	plt.title('A graph showing relative abilities VS time for matches, for the English and PARS scoring systems')
	plt.show()

#scoringPlot()