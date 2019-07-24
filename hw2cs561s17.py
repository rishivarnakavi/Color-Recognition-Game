import sys
import re
import operator
import time
start_time = time.time()

class assignment:
    def __init__(self):
        self.max_int = float('inf')
        self.min_int = float('-inf')

    def mainFunction(self):
        self.file1 = open("t4.txt", "r")
        self.file2 = open("output.txt", "w")
        num_lines = sum(1 for line in open("t4.txt"))
        self.colors = self.file1.readline().strip().split(", ")
        self.initial_map = self.file1.readline().rstrip()
        map = {}
        initial_map1 = re.findall(r"[\w']+", self.initial_map)
        length_map = len(initial_map1)
        for k in range(length_map):
            if k % 3 == 0:
                map[initial_map1[k]] = [initial_map1[k+1], initial_map1[k+2]]
            else:
                continue
        self.maximum_depth = int(self.file1.readline().rstrip())
        self.preference1 = {}
        p1 = self.file1.readline().rstrip()
        p1_temp = re.findall(r"[\w']+", p1)
        for i in range(len(p1_temp)):
            if i % 2 == 0:
               self.preference1[p1_temp[i]] = p1_temp[i + 1]
            else:
                continue
        self.preference2 = {}
        p2 = self.file1.readline().rstrip()
        p2_temp = re.findall(r"[\w']+", p2)
        for j in range(len(p2_temp)):
            if j % 2 == 0:
                self.preference2[p2_temp[j]] = p2_temp[j + 1]
            else:
                continue
        self.Node_list = {}
        for i in range(4, num_lines - 1):
            temp_array = self.file1.readline().rstrip().split(": ")
            self.Node_list[temp_array[0]] = temp_array[1].split(", ")
        prevAssignment = [initial_map1[length_map-3], initial_map1[length_map-2]]
        self.values = {}
        v = self.max_function(map, self.values, 0, prevAssignment, self.min_int, self.max_int)
        last_line = str(self.values[v][0]) + ', ' + str(self.values[v][1]) + ', ' + str(v)
        self.file2.write(last_line)
        self.file2.close()
        print(str(time.time() - start_time))

    def max_function(self, current_map, value, depth, previous_assignment, alpha, beta):
        if not bool(self.find_moves(current_map)) or depth == self.maximum_depth:
            total = 0
            for temp_map in current_map.values():
                if temp_map[1] == '1':
                    temp_total = self.preference1[temp_map[0]]
                    total += int(temp_total)
                else:
                    temp_total = self.preference2[temp_map[0]]
                    total -= int(temp_total)
            v = total
            self.file2.write(", ".join([str(previous_assignment[0]), str(previous_assignment[1]), str(depth), str(v), str(alpha), str(beta)]))
            self.file2.write("\n")
            return v
        v = self.min_int
        for move in self.find_moves(current_map):
            self.file2.write(", ".join([str(previous_assignment[0]), str(previous_assignment[1]), str(depth), str(v), str(alpha), str(beta)]))
            self.file2.write("\n")
            min_value = self.min_function(self.final_result(current_map, move, 1), {}, depth+1, move, alpha, beta)
            v = max(v, min_value)
            self.return_value(value, v, move)
            if v >= beta:
                break
            alpha = max(alpha, v)
        self.file2.write(", ".join([str(previous_assignment[0]), str(previous_assignment[1]), str(depth), str(v), str(alpha), str(beta)]))
        self.file2.write("\n")
        return v

    def min_function(self, current_map, value, depth, previous_assignment, alpha, beta):
        if not bool(self.find_moves(current_map)) or depth == self.maximum_depth:
            total = 0
            for temp_map in current_map.values():
                if temp_map[1] == '1':
                    temp_total = self.preference1[temp_map[0]]
                    total += int(temp_total)
                else:
                    temp_total = self.preference2[temp_map[0]]
                    total -= int(temp_total)
            v = total
            self.file2.write(", ".join([str(previous_assignment[0]), str(previous_assignment[1]), str(depth), str(v), str(alpha), str(beta)]))
            self.file2.write("\n")
            return v
        v = self.max_int
        for move in self.find_moves(current_map):
            self.file2.write(", ".join([str(previous_assignment[0]), str(previous_assignment[1]), str(depth), str(v), str(alpha), str(beta)]))
            self.file2.write("\n")
            max_value = self.max_function(self.final_result(current_map, move, 2), {}, depth+1, move, alpha, beta)
            v = min(v, max_value)
            self.return_value(value, v, move)
            if v <= alpha:
                break
            beta = min(beta, v)
        self.file2.write(", ".join([str(previous_assignment[0]), str(previous_assignment[1]), str(depth), str(v), str(alpha), str(beta)]))
        self.file2.write("\n")
        return v

    def final_result(self, current_map, move, player):
        current_map1 = dict(current_map)
        data = [move[1], str(player)]
        current_map1[move[0]] = data
        return current_map1

    def return_value(self, value, v, move):
        if v in value:
            if (move[0], move[1]) > (value[v][0], value[v][1]):
                return
        value[v] = move

    def find_moves(self, current_map):
        visited = []
        valid_moves = set()
        for state in current_map.keys():
            for node in self.Node_list[state]:
                if node not in visited and node not in current_map.keys():
                    visited.append(node)
                    last = []
                    valid_colors = set(self.colors)
                    for next_node in self.Node_list[node]:
                        if next_node in current_map and current_map[next_node][0] in valid_colors:
                            valid_colors.remove(current_map[next_node][0])
                    for remaining_color in valid_colors:
                        x = (node, remaining_color)
                        last.append(x)
                    valid_moves = valid_moves.union(last)
        return sorted(list(valid_moves), key=operator.itemgetter(0, 1))

def main():
    flag = "true"
    if flag == "true":
        obj = assignment()
        obj.mainFunction()
        flag == "false"
    else:
        pass

main()