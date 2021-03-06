import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
DIRE = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
random.seed(0)

#don't change the class name
class AI(object):
    #chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        #You are white or black
        self.color = color
        #the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your decision.
        self.candidate_list = []
        self.depth = 3
        self.inf = 0x7FFFFFFF

    # The input is current chessboard.
    def go(self, chessboard):
        start = time.perf_counter()
        # Clear candidate_list, must do this step
        self.candidate_list.clear()
        #==================================================================
        #Write your algorithm here
        vlist = self.get_valid_point(self.color, chessboard, True, True)
        for (i, j) in vlist:
            self.candidate_list.append((i, j))
        value, action = self.alpha_beta(-self.inf, self.inf, self.depth, self.color, chessboard)
        if action != (-1,-1):
            self.candidate_list.append(action)
        # idx = np.where(chessboard == COLOR_NONE)
        # idx = list(zip(idx[0], idx[1]))
        # size = len(idx)
        # if size <= 10:
        #     self.depth = 9
        # elif size <= 13:
        #     self.depth = 8
        # elif size <= 54:
        #     self.depth = 3
        # else:
        #     self.depth = 4
        # while True:
        #     value, action = self.alpha_beta(-self.inf, self.inf, self.depth, self.color, chessboard)
        #     if action != (-1,-1):
        #         self.candidate_list.append(action)
        #     self.depth += 1
        #     end = time.perf_counter()
        #     if end - start > self.time_out/5 or not (-1000000 < value < 1000000 ):
        #         break

    #refer to https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/O-Thell-Us/Othellus.pdf
    def alpha_beta(self, alpha, beta, depth, color, chessboard, p=0):
        best_value = -self.inf
        best_action = (-1, -1)
        list = self.get_valid_point(color, chessboard)
        if len(list) == 0:
            if p == 1:
                return (self.get_score(color, chessboard) - self.get_score(-color, chessboard)) * 1000000, (-1, -1)
            else:
                best_value = -(self.alpha_beta(-beta, -alpha, depth, -color, chessboard, p=1)[0])
        for (i, j) in list:
            valid_list = self.place(i, j, color, chessboard)
            value = -self.judge(-color, chessboard) if depth <= 1 else -self.alpha_beta(-beta, -alpha, depth - 1, -color, chessboard)[0]
            self.unplace(i, j, color, chessboard, valid_list)
            if value >= beta:
                return value, (i, j)
            if value > best_value:
                best_value = value
                best_action = (i, j)
                if value > alpha:
                    alpha = value
        return best_value, best_action

    def judge(self, color, chessboard):
        #refer to those researchers from University of Washington
        #https://docs.google.com/viewer?a=v&q=cache:jTw8-AIiLT4J:www.cs.washington.edu/education/courses
        #/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf+&hl=en&gl=in&pid=bl&srcid=ADGEESj0Uu5_18RXpKD5
        #XpUDDghEHy3AcK2s1B8Nc7TRGg2ZOc3PMwu25wrpU7QMVU2_Q1LEdBW63bw9DuCfiNZy5Yy63-otuqCrICcg8OITB93G9z3
        #NvqjZUnRN4YDbHQlhH5yrpsx4&sig=AHIEtbTNLnl6496wPiyJKMfoqu0YocErdg
        #And
        #https://kartikkukreja.wordpress.com/2013/03/30/heuristic-function-for-reversiothello/
        size = self.chessboard_size
        weight = np.array([
            [20, -3, 11, 8, 8, 11, -3, 20],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [20, -3, 11, 8, 8, 11, -3, 20]
            ])
        count = 2 * color * np.sum(chessboard * weight)
        my_chess = 0
        opp_chess = 0
        my_tiles = 0
        opp_tiles = 0
        my_inside = 0
        opp_inside = 0
        for i in range(size):
            for j in range(size):
                if chessboard[i][j] == COLOR_NONE:
                    continue
                if chessboard[i][j] == color:
                    my_chess += 1
                elif chessboard[i][j] == -color:
                    opp_chess += 1
                for d in range(8):
                    x = i + DIRE[d][0]
                    y = j + DIRE[d][1]
                    if 0 <= x < size and 0 <= y < size and chessboard[x][y] == COLOR_NONE:
                        if chessboard[i][j] == color:
                            my_tiles += 1
                        else:
                            opp_tiles += 1
                        break
                time = 8
                for d in range(8):
                    x = i + DIRE[d][0]
                    y = j + DIRE[d][1]
                    if 0 <= x < size and 0 <= y < size and chessboard[x][y] != COLOR_NONE:
                        time -= 1
                if time != 0:
                    continue
                if chessboard[i][j] == color:
                    my_inside += 1
                else:
                    opp_inside += 1
                    
        i = 0
        if my_inside > opp_inside:
            i = ((100 * my_inside) // (my_inside + opp_inside))
        elif my_inside < opp_inside:
            i = -((100 * opp_inside) // (my_inside + opp_inside))
                
        c = 0
        if my_chess > opp_chess:
            c = ((100 * my_chess) // (my_chess + opp_chess)) * 2
        elif my_chess < opp_chess:
            c = -((100 * opp_chess) // (my_chess + opp_chess)) * 2

        t = 0
        if my_tiles > opp_tiles:
            t = -(100.0 * my_tiles) // (my_tiles + opp_tiles) * 15
        elif my_tiles < opp_tiles:
            t = (100.0 * opp_tiles) // (my_tiles + opp_tiles) * 15

        s = (self.get_stable(color, chessboard) -
             self.get_stable(-color, chessboard)) * 1000
        
        my_mobility = len(self.get_valid_point(color, chessboard, sort=False))
        opp_mobility = len(self.get_valid_point(-color, chessboard, sort=False))
        m = 0
        if my_mobility > opp_mobility:
            m = ((100 * my_mobility) // (my_mobility + opp_mobility)) * 16
        elif my_mobility < opp_mobility:
            m = -((100 * opp_mobility) // (my_mobility + opp_mobility)) * 16
            
        count += (s + m + c + t)
        return count

    def get_stable(self, color, chessboard):
        stable = np.array(
            [[False, False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False, False],
             [False, False, False, False, False, False, False, False]])
        count = 0
        size = self.chessboard_size
        if chessboard[0][0] == color:
            count += 3
            for x in range(size):
                for y in range(size):
                    if chessboard[x][y] == color:
                        stable[x][y] = True
                    else:
                        break
                if chessboard[x][0] != color:
                    break
        if chessboard[0][size - 1] == color:
            count += 3
            for x in range(size):
                for y in range(size - 1, -1, -1):
                    if chessboard[x][y] == color:
                        stable[x][y] = True
                    else:
                        break
                if chessboard[x][size - 1] != color:
                    break
        if chessboard[size - 1][0] == color:
            count += 3
            for x in range(size - 1, -1, -1):
                for y in range(size):
                    if chessboard[x][y] == color:
                        stable[x][y] = True
                    else:
                        break
                if chessboard[x][0] != color:
                    break
        if chessboard[size - 1][size - 1] == color:
            count += 3
            for x in range(size - 1, -1, -1):
                for y in range(size - 1, -1, -1):
                    if chessboard[x][y] == color:
                        stable[x][y] = True
                    else:
                        break
                if chessboard[x][size - 1] != color:
                    break
        cp = 0
        if chessboard[0][0] == COLOR_NONE:
            if chessboard[0][1] == color and not stable[0][1]:
                cp -= 1
            if chessboard[1][0] == color and not stable[1][0]:
                cp -= 1
            if chessboard[1][1] == color and not stable[1][1]:
                cp -= 1
        if chessboard[0][size - 1] == COLOR_NONE:
            if chessboard[0][size - 2] == color and not stable[0][size - 2]:
                cp -= 1
            if chessboard[1][size - 1] == color and not stable[1][size - 1]:
                cp -= 1
            if chessboard[1][size - 2] == color and not stable[1][size - 2]:
                cp -= 1
        if chessboard[size - 1][0] == COLOR_NONE:
            if chessboard[size - 1][1] == color and not stable[size - 1][1]:
                cp -= 1
            if chessboard[size - 2][0] == color and not stable[size - 2][0]:
                cp -= 1
            if chessboard[size - 2][1] == color and not stable[size - 2][1]:
                cp -= 1
        if chessboard[size - 1][size - 1] == COLOR_NONE:
            if chessboard[size -1][size -2] == color and not stable[size - 1][size - 2]:
                cp -= 1
            if chessboard[size -2][size -1] == color and not stable[size - 2][size - 1]:
                cp -= 1
            if chessboard[size -2][size -2] == color and not stable[size - 2][size - 2]:
                cp -= 1
        if (self.color == color and self.depth % 2 == 1) or (self.color == -color and self.depth % 2 == 0):
            cp *= 2
        count += cp
        idx = np.where(stable == True)
        idx = list(zip(idx[0], idx[1]))
        count += len(idx)
        return count

    def place(self, x, y, color, chessboard):
        size = self.chessboard_size
        list = []
        chessboard[x][y] = color
        for d in range(8):
            i = x + DIRE[d][0]
            j = y + DIRE[d][1]
            while 0 <= i < size and 0 <= j < size and chessboard[i][j] == -color:
                i += DIRE[d][0]
                j += DIRE[d][1]
            if 0 <= i < size and 0 <= j < size and chessboard[i][j] == color:
                while True:
                    i -= DIRE[d][0]
                    j -= DIRE[d][1]
                    if i == x and j == y:
                        break
                    chessboard[i][j] = color
                    list.append((i, j))
        return list

    def unplace(self, x, y, color, chessboard, list):
        chessboard[x][y] = COLOR_NONE
        for (i, j) in list:
            chessboard[i][j] = -color

    def get_score(self, color, chessboard):
        idx = np.where(chessboard == color)
        idx = list(zip(idx[0], idx[1]))
        return len(idx)

    def get_valid_point(self, color, chessboard, sort = True, reverse = False):
        size = self.chessboard_size
        weight = np.array([
            [20, -3, 11, 8, 8, 11, -3, 20],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [20, -3, 11, 8, 8, 11, -3, 20]
            ])
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        valid_list = []
        for (m, n) in idx:
            for d in range(8):
                i = m + DIRE[d][0]
                j = n + DIRE[d][1]
                time = 0
                while 0 <= i < size and 0 <= j < size and chessboard[i][j] == -color:
                    i += DIRE[d][0]
                    j += DIRE[d][1]
                    time += 1
                if 0 <= i < size and 0 <= j < size and chessboard[i][j] == color and time > 0:
                    valid_list.append((m, n))
                    break
        if sort:
            if reverse:
                valid_list = sorted(valid_list, key=lambda v: weight[v[0]][v[1]])
            else:
                valid_list = sorted(valid_list, key=lambda v: -weight[v[0]][v[1]])
        return valid_list