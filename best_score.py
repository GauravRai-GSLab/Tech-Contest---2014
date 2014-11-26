class BestTeamScore(object):

	def __init__(self, lines):

		self._lines = lines
		self._score = -1000
		self._team = []

	def __read_players(self):

		self._players = [(line.strip()[2:], int(line.strip()[:2])) for line in self._lines if line.strip() != '']
		
	def __calculate_score(self, _team):

		if len(_team) != 11:
			return 0
		team = dict(T=[], L=[], W=[])	
		total_score = 0
		for player in _team:
			team[player[0]].append(player[1])
			total_score += player[1]
		if len(team['W']) < 1:
			total_score -= 10
		elif len(team['W']) > 1:
			total_score -= (len(team['W']) - 1) * 3	
		if len(team['L']) < 4:
			total_score -= (4 - len(team['L'])) * 5
		elif len(team['L']) > 5:
			total_score -= (len(team['L']) - 5) * 5
		return total_score

	def __find(self, ind, acc, cnt, team):
		
		global debug

		if cnt == 11:
			score = self.__calculate_score(team)
			if self._score < score:
				self._score = score
				self._team = team
				if debug is True:
					self.print_current_best()
			return	
		if acc == 4 or ind == 40:
			return
		temp = []
		for i in range(11-cnt):
			if ind+i == 40:
				break
			temp.append(self._players[ind+i])
			self.__find(ind+i+1, acc+1, cnt+i+1, team+temp)	
		self.__find(ind+1, acc, cnt, team)	

	def start(self):

		self.__read_players()
		self.__find(0, 0, 0, [])

	def print_current_best(self):

		print self._score, self._team

	def get_best_score(self):

		return self._score

	def get_best(self):

		team = ' '.join(['%s%s'%(pl[1], pl[0]) if pl[1] < 0 else '+%s%s'%(pl[1], pl[0]) for pl in self._team])
		return self._score, team	

debug = False
if __name__ == '__main__':

	#debug = True
	obj = BestTeamScore('test cases/sample')
	obj.start()
	obj.print_current_best()