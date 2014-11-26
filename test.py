import sys
from solution import Game
from best_score import BestTeamScore

class IPLTeamBuilding(object):

	def __init__(self, lines):

		self._lines = lines
		self._accumulate = []
		self._acquire = 0
		self._no_of_acquires = 0
		self._discard = 0
		self._team = []

	def __read_players(self):

		self._players = [(line.strip()[2:], int(line.strip()[:2]), line.strip()) for line in self._lines if line.strip() != '']

	def __accumulate(self, player):
		
		self._accumulate.append(player)

	def __acquire(self, player):
		
		self.__accumulate(player)
		self._team += self._accumulate
		self._accumulate = []
		self._no_of_acquires += 1

	def __discard(self, player):
		
		self._accumulate = []

	def _calculate_score(self):

		#print "\n", self._players
		team = ' '.join(['%s%s'%(pl[1], pl[0]) if pl[1] < 0 else '+%s%s'%(pl[1], pl[0]) for pl in self._team])
		print "Our Team:  %s"%team
		if len(self._team) != 11:
			return 0
		
		team = dict(T=[], L=[], W=[])	
		total_score = 0
		for player in self._team:
			team[player[0]].append(player[1])
			total_score += player[1]
		if len(team['W']) > 1:
			total_score -= (len(team['W']) - 1) * 3
		elif len(team['W']) < 1:
			total_score -= 10
		
		if len(team['L']) < 4:
			total_score -= (4 - len(team['L'])) * 5
		elif len(team['L']) > 5:
			total_score -= (len(team['L']) - 5) * 5
		return total_score	
			
	def start(self):

		self.__read_players()
		game = Game()

		for i in range(40):
			move = game.yourMove(self._players[i][2])
			#print "Move: ", self._players[i][2], move
			if move == 1:
				self.__accumulate(self._players[i])
			elif move == 2:
				self.__acquire(self._players[i])
				if len(self._team) >= 11 or self._no_of_acquires == 4:
					break
			elif move == 3:
				self.__discard(self._players[i])		
		return self._calculate_score()		

if __name__ == '__main__':

	fi = open(sys.argv[1], 'r')	
	lines = fi.readlines()
	fi.close()
	text = ""

	sum_best_score = 0.0
	sum_score = 0.0
	cnt = 0

	for line in lines:
		cnt += 1
		print "Test Case #%s" % cnt

		line = line.strip()
		if line == '':
			continue
		values = line.split(',')
		if len(values) != 40:
			best_score = int(values[40])
			best_team = values[41]
			values = values[:40]
		else:
			bestScore = BestTeamScore(values)
			bestScore.start()
			best_score, best_team = bestScore.get_best()
		
		print "Players: %s" % ' '.join(values)	
		obj = IPLTeamBuilding(values)
		score = obj.start()
		text += "%s,%s,%s\n"%(','.join(values), best_score, best_team)
		
		print "Best Team: %s" % best_team
		print "Score: %s out of %s\n" % (score, best_score)
		sum_score += score
		sum_best_score += best_score
	fo = open(sys.argv[1], 'w')
	fo.write(text)
	fo.close()
	print "\nAverage score: %.2f out of %.2f" % (sum_score/cnt, sum_best_score/cnt)
	print "Accuracy: %.2f%%" % (sum_score * 100.0 / sum_best_score)
