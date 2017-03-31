import random

def getRoll():
	ret = []
	ret.append(random.randint(1, 6))
	ret.append(random.randint(1, 6))
	if (ret[0] == ret[1]):
		ret.append(ret[0])
		ret.append(ret[0])
	return ret

def makeBoard():
	a = {}
	for i in range(1, 7):
		a[i] = 0
	for i in range(15):
		x = random.randint(1, 6)
		a[x] += 1
	b = dict(a)
	c = dict(a)
	return a, b, c

def empty(b):
	ret = []
	for i in range(1, 7):
		if b[i] == 0:
			ret.append(i)
	return ret

def canfill(b, em, i):
	for x in em:
		if x+i in range(1, 7) and b[x+i] > 0:
			return [x+i, x]
	return []

def build(b):
	eaten = 0
	moves = 0
	prev = []
	while eaten < 15:
		roll = getRoll()
		prev.append(roll)
		for i in roll:
			if eaten > 14:
				break
			x = 6
			while b[x] == 0:
				x -= 1
			if x <= i:
				eaten += 1
			else:
				b[x-i] += 1
			b[x] -= 1
		moves += 1
	return moves, prev

def eat(b, r):
	eaten = 0
	moves = 0
	prev = []
	index = 0
	l = len(r)
	while eaten < 15:
		if index >= l:
			roll = getRoll()
			prev.append(roll)
		else:
			roll = r[index]
			index += 1
		for i in roll:
			if eaten > 14:
				break
			if b[i] > 0:
				b[i] -= 1
				eaten += 1
			else:
				em = empty(b)
				fill = canfill(b, em, i) #body mass index lol
				if em and fill:
					b[fill[0]] -= 1
					b[fill[1]] += 1
				else:
					x = 6
					while b[x] == 0:
						x -= 1
					if x <= i:
						eaten += 1
					else:
						b[x-i] += 1
					b[x] -= 1	
		moves += 1
	r.extend(prev)
	return moves, r

def prettyprint(b):
	height = 0
	for i in range(1, 7):
		if b[i] > height:
			height = b[i]
	i = height
	while i > 0:
		for x in range(1, 7):
			if b[x] >= i:
				print("O ", end="")
			else:
				print("  ", end="")
		i -= 1
		print()
	print("-----------")
	print("1 2 3 4 5 6")

def sim():
	runs = 10000
	unexpected = []
	buildTotal = 0
	eatTotal = 0
	buildWins = 0
	eatWins = 0
	buildDisparity = 0
	eatDisparity = 0
	ties = 0
	for i in range(runs):
		roundNum = i + 1
		a, b, c = makeBoard()
		bMoves, brolls = build(a)
		eMoves, rolls = eat(b, brolls)
		buildTotal += bMoves
		eatTotal += eMoves
		if eMoves >= bMoves:
			if eMoves == bMoves:
				ties += 1
			else:
				diff = eMoves - bMoves
				buildDisparity += diff
				unexpected.append([c, brolls, diff, roundNum])
			buildWins += 1
		else:
			eatDisparity += bMoves - eMoves
			eatWins += 1
	print("A total of " + str(runs) + " simulations were run")
	print("It took an average of " + str(buildTotal/runs) + " moves for the build strategy")
	print("It took an average of " + str(eatTotal/runs) + " moves for the eat strategy")
	print("That is an average difference of " + str(abs(eatTotal - buildTotal)/runs) + " moves per game")
	print("There were " + str(ties) + " ties out of " + str(runs) + " games for a tie rate of " + str(100*ties/runs) + "%")
	print("The build strategy won " + str(buildWins) + " times (including ties) for a win rate of " + str(100*buildWins/runs) + "%")
	print("The build strategy won " + str(buildWins - ties) + " times (NOT including ties) for a win rate of " + str(100*(buildWins-ties)/runs) + "%")
	print("The eat strategy won " + str(eatWins + ties) + " times (including ties) for a win rate of " + str(100*(eatWins+ties)/runs) + "%")
	print("The eat strategy won " + str(eatWins) + " times (NOT including ties) for a win rate of " + str(100*eatWins/runs) + "%")
	print("That is a difference of " + str(abs(eatWins - buildWins)) + " games (including ties)")
	print("That is a difference of " + str(abs(eatWins - buildWins + ties)) + " games (NOT including ties)")
	if buildWins - ties > 0:
		print("When the build strategy won, it won by an average of " + str(buildDisparity/(buildWins - ties)) + " moves")
	if eatWins > 0:
		print("When the eat strategy won, it won by an average of " + str(eatDisparity/eatWins) + " moves")
	print("By analyzing the games for which the build strategy won, one can determine what type of board setup and rolls leads to a victory when employing the build strategy")
	input("Press enter to see the boards and rolls for which the build strategy won...")
	print()
	for x in unexpected:
		print("GAME " + str(x[3]))
		print()
		prettyprint(x[0])
		print()
		print("The rolls in the game were:")
		for r in range(len(x[1])):
			print("Roll " + str(r+1) + ": ", end="")
			for i in x[1][r]:
				print(str(i) + " ", end="")
			print()
		print("The build strategy beat the eat strategy by " + str(x[2]) + " move") #seems to ALWAYS be 1 so singular works
		for x in range(4):
			print()
sim()
