class Game(object):

    def __init__(self):

        #Constants
        self.AVG_SCORE_PER_PLAYER = 4
        self.AVG_ORIGINAL_SCORE_PER_PLAYER = 4

        self.no_of_negative_to_come = 18
        self.no_of_positive_to_come = 22

        self.discard_all = False
        self.accumulate_all = False
        self.acquire_these = False
        self.discard_any = False

        self.no_of_bm_to_come = 18
        self.no_of_bl_to_come = 18
        self.no_of_wk_to_come = 4
        self.no_of_players_to_come = 40

        self.no_of_bm_acquired = 0
        self.no_of_bl_acquired = 0
        self.no_of_wk_acquired = 0
        self.no_of_players_acquired = 0

        self.no_of_bm_accumulated = 0
        self.no_of_bl_accumulated = 0
        self.no_of_wk_accumulated = 0
        self.no_of_players_accumulated = 0

        self.acquired_score = -30
        self.accumulated_score = 0
        self.accumulated_origional_score = 0
        self.accumulated_or_score = 0

        self.accumulated_players = []
        self.acquired_players = []
        self.players_to_come = [
                (1, 'T'), (2, 'T'), (3, 'T'), (4, 'T'), (5, 'T'), (6, 'T'), (7, 'T'), (8, 'T'), (9, 'T'),
                (-1, 'T'), (-2, 'T'), (-3, 'T'), (-4, 'T'), (-5, 'T'), (-6, 'T'), (-7, 'T'), (-8, 'T'), (-9, 'T'),
                (1, 'L'), (2, 'L'), (3, 'L'), (4, 'L'), (5, 'L'), (6, 'L'), (7, 'L'), (8, 'L'), (9, 'L'),
                (-1, 'L'), (-2, 'L'), (-3, 'L'), (-4, 'L'), (-5, 'L'), (-6, 'L'), (-7, 'L'), (-8, 'L'), (-9, 'L'),
                (5, 'W'), (5, 'W'), (5, 'W'), (5, 'W')
            ]
        self.players_to_come.sort()
        self.combinations = [2, 3, 3, 3]
        self.can_change_combinations = True
        self.no_of_acquires_to_go = 4

        self.decide_next_strategy()

    def accumulate_bm(self, player):

        self.no_of_bm_accumulated += 1

    def accumulate_bl(self, player):

        self.no_of_bl_accumulated += 1

    def accumulate_wk(self, player):

        self.no_of_wk_accumulated += 1

    def accumulate_player(self, player):

        score, typ = player[0], player[1]
        if typ == 'T':
            self.accumulate_bm(player)
        elif typ == 'L':
            self.accumulate_bl(player)
        else:
            self.accumulate_wk(player)
        self.accumulated_players.append(player)
        self.no_of_players_accumulated += 1
        self.accumulated_score += player[2]
        self.accumulated_origional_score += player[0]
        self.accumulated_or_score += player[0]
        if self.total_players() == 11:
            return self.acquire_player()
        if self.no_of_acquires_to_go >= 3 and self.no_of_players_accumulated == self.combinations[0] and self.accumulated_origional_score >= 27 and self.accumulated_or_score > 12:
            del(self.combinations[0])
            return self.acquire_player()

        if self.no_of_acquires_to_go >= 2 and self.accumulated_or_score < 8 and self.no_of_players_accumulated == self.combinations[-1]:
            if  11 - self.no_of_players_acquired < self.no_of_players_to_come:
                return self.discard_player(player)

        if self.no_of_players_accumulated == self.combinations[-1]:
            del(self.combinations[-1])
            return self.acquire_player()
        return 1

    def acquire_player(self):

        self.acquired_players += self.accumulated_players
        self.no_of_players_acquired += self.no_of_players_accumulated
        self.no_of_bm_acquired += self.no_of_bm_accumulated
        self.no_of_bl_acquired += self.no_of_bl_accumulated
        self.no_of_wk_acquired += self.no_of_wk_accumulated
        self.acquired_score += self.accumulated_score

        self.accumulated_players = []
        self.no_of_players_accumulated = 0
        self.no_of_bm_accumulated = 0
        self.no_of_bl_accumulated = 0
        self.no_of_wk_accumulated = 0
        self.accumulated_score = 0
        self.accumulated_or_score = 0

        self.no_of_acquires_to_go -= 1

        if self.no_of_players_acquired == 11 and self.acquired_score < 0:
            self.discard_all = True
            return 3
        return 2

    def discard_player(self, player):

        self.accumulated_players = []
        self.no_of_players_accumulated = 0
        self.no_of_bm_accumulated = 0
        self.no_of_bl_accumulated = 0
        self.no_of_wk_accumulated = 0
        self.accumulated_score = 0

        self.accumulated_or_score = 0
        return 3

    def total_players(self):

        return self.no_of_players_acquired + self.no_of_players_accumulated

    def add_actual_score(self, player):

        if player[1] == 'W':
            if self.no_of_wk_acquired >= 1:
                player += (player[0]-3,)
            else:
                player += (player[0]+10,)
        elif player[1] == 'L':
            if self.no_of_bl_accumulated + self.no_of_bl_acquired >= 5:
                player += (player[0]-5,)
            elif self.no_of_bl_accumulated + self.no_of_bl_acquired < 4:
                player += (player[0]+5,)
            else:
                player += (player[0],)
        else:
            player += (player[0],)
        return player

    def parse_player(self, player):

        player = self.add_actual_score((int(player[:2]), player[2]))
        if player[1] == 'W':
            self.no_of_wk_to_come -= 1
        elif player[1] == 'L':
            self.no_of_bl_to_come -= 1
        else:
            self.no_of_bm_to_come -= 1
        self.no_of_players_to_come -= 1

        if player[0] > 0:
            self.no_of_negative_to_come -= 1
        else:
            self.no_of_positive_to_come -= 1

        return player

    def can_discard(self, player):

        if player[2] < 4:
            return True
        return False

    def decide_move(self, player):

        if self.no_of_players_accumulated == 0:
            if self.can_discard(player):
                return self.discard_player(player)
            else:
                return self.accumulate_player(player)

        if (self.accumulated_origional_score + player[2])/(self.no_of_players_accumulated + 1)+1 <= self.AVG_ORIGINAL_SCORE_PER_PLAYER:
            return self.discard_player(player)

        if (self.accumulated_score + player[2])/(self.no_of_players_accumulated + 1)+1 >= self.AVG_SCORE_PER_PLAYER:
            return self.accumulate_player(player)
        return self.discard_player(player)

    def get_scores_to_come(self):

        scores = []
        no_of_wk_acquired = self.no_of_wk_acquired
        no_of_bl_acquired = self.no_of_bl_acquired

        for player in self.players_to_come:
            score = player[0]
            if player[1] == 'W':
                if no_of_wk_acquired >= 1:
                    score -= 3
                else:
                    score += 10
                no_of_wk_acquired += 1
            elif player[1] == 'L':
                if no_of_bl_acquired >= 5:
                    score -= 5
                elif no_of_bl_acquired < 4:
                    score += 5
                no_of_bl_acquired += 1
            scores.append((player[0], player[1], score))
        scores.sort(key=lambda x: x[2])
        return scores

    def decide_next_strategy(self):

        self.discard_all = False
        self.accumulate_all = False
        self.acquire_these = False
        self.discard_any = False

        if self.no_of_players_to_come == 0:
            return
        no_of_players_require = 11 - self.total_players()
        if self.no_of_players_to_come == no_of_players_require:
            score_to_come = sum([self.add_actual_score(player)[2] for player in self.players_to_come])
            if self.accumulated_score + self.acquired_score + score_to_come >= 0:
                self.accumulate_all = True
            else:
                self.discard_all = True
        elif self.no_of_players_to_come <= 11 - self.no_of_players_acquired:
            self.accumulate_all = True
        elif self.no_of_acquires_to_go == 1 and self.combinations[0] == 1:
            scores_to_come = self.get_scores_to_come()
            self.acquire_these = [scores_to_come[0]]
        elif self.no_of_acquires_to_go == 2 and self.no_of_players_accumulated == 0 and self.no_of_wk_acquired > 0 and self.no_of_bl_acquired > 4:
            scores_to_come = self.get_scores_to_come()
            self.discard_any = [self.add_actual_score((score[0], score[1])) for score in scores_to_come[:-no_of_players_require]]
        elif self.no_of_acquires_to_go == 1 and self.no_of_players_accumulated == 0 and self.no_of_wk_acquired == 0:
            scores_to_come = self.get_scores_to_come()

        if 11 - self.no_of_players_acquired + 5 > self.no_of_positive_to_come:# and self.no_of_players_accumulated == 0:
            self.AVG_SCORE_PER_PLAYER = 3

    def yourMove(self, player):

        player = self.parse_player(player)
        self.players_to_come.remove((player[0], player[1]))

        if self.no_of_bm_to_come > 16 and player[1] == 'T' and player[0] < 4:
            return self.discard_player(player)
        elif self.no_of_bl_to_come > 16 and player[1] == 'L' and player[0] < 3:
            return self.discard_player(player)
        elif self.discard_all is not False:
            return self.discard_player(player)
        elif self.accumulate_all is not False:
            return self.accumulate_player(player)
        elif self.acquire_these is not False:
            if player in self.acquire_these:
                return self.acquire_player()
            return self.discard_player(player)
        elif self.discard_any is not False and player in self.discard_any:
            self.discard_any = False
            move = self.discard_player(player)
        elif self.no_of_players_to_come >= 37 and self.no_of_players_accumulated == 0 and player[0] >= 7 and self.combinations[0] == 2:
            self.accumulate_player(player)
            move = self.acquire_player()
            self.combinations[-1] += 1
            del(self.combinations[0])
        else:
            move = self.decide_move(player)
        self.decide_next_strategy()
        return move
