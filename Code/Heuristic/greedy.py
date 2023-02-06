#!/usr/bin/python3

import numpy as np
import sys

# def input_():
#     [N,M] = [int(x) for x in sys.stdin.readline().split()]                                      # n: number of subjects, m number of rooms
#     d = [int(x) for x in sys.stdin.readline().split()]                                          # d: list of number of students registered for each subject  (d[i] is number of students registerd subject i)
#     c = [int(x) for x in sys.stdin.readline().split()]                                          # c: list of capacity of rooms (c[j] is the capacity of room j)
#     K = int(input())
#     conflicts = [list(map(lambda x: int(x)-1, sys.stdin.readline().split())) for _ in range(K)] # conflicts: list of 2 non-conflicting subjects (i,j)
#     return N,d,M,c,K,conflicts

def input_(filename):
    with open(filename) as f:
        input_list = f.readlines()
        N = int(input_list[0])                                          # n: number of subjects, m number of rooms
        d = [int(x) for x in input_list[1].strip().split()]             # n: number of subjects, m number of rooms
        M = int(input_list[2])                                          # d: list of number of students registered for each subject  (d[i] is number of students registerd subject i)
        c = [int(x) for x in input_list[3].strip().split()]             # c: list of capacity of rooms (c[j] is the capacity of room j)
        K = int(input_list[4])                                          # k: number of conflicting pair
        conflicts = [list(map(lambda x: int(x) - 1, ij.split())) for ij in input_list[5:]]    # conflicts: list of 2 conflicting subjects (i,j)
        return N,d,M,c,K,conflicts

def greedy(N, D, M, C, conflicts):
    time_table = [(0,0,0) for _ in range(N)]
    scheduled = np.zeros((N, M, 4), dtype=int)
    cur_day = 0
    exclude = {}
    for i,j in conflicts:
        exclude[i] = exclude.get(i, []) + [j]
        exclude[j] = exclude.get(j, []) + [i]

    # sort number of students registered for each subject in decreasing order
    exams = [(d, i) for i, d in enumerate(D)]
    exams.sort(reverse=True, key=lambda x: x[0])

    # sort capacity of rooms in decreasing order
    rooms = [(c, j) for j, c in enumerate(C)]
    rooms.sort(reverse=True, key=lambda x: x[0])

    # assign subject to earliest available period
    for exam in exams:
        d, i = exam
        for room in rooms:
            c, j = room
            for k in range(4):
                if (scheduled[cur_day][j][k] + d <= c) and (scheduled[cur_day][j][k] == 0):
                    # check if there is another subject registered or full of capacity of room
                    conflict = False
                    for ii in range(i):
                        if (time_table[ii][0] == cur_day and time_table[ii][2] == k) and ((ii in exclude.get(i, [])) or time_table[ii][1] == j ):
                            conflict = True
                            break
                    if conflict:
                        continue
                    scheduled[cur_day][j][k] += d
                    time_table[i] = (cur_day, j, k)
                    # print(f"Subject {i+1} is scheduled at day {cur_day+1}, room {j+1}, period {k+1}") debug
                    break
            else:
                continue
            break
        else:
            cur_day += 1
            
    # return the minimum days for the exam
    return cur_day + 1, time_table

def main():
    n,d,m,c,k,conflicts = input_(input())
    num_days, time_table = greedy(n,d,m,c, conflicts)
    for exam, (i,j,k) in enumerate(time_table):
        print(f"Subject {exam+1} is assigned at day {i+1}, room {j+1}, and period {k+1}")
    print(f"Minimum days for the exams: {num_days}")

if __name__ == "__main__":
  main()
