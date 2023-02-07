#!/usr/bin/python3

import numpy as np

def input_(filename):
    with open(filename) as f:
        input_list = f.readlines()
        N = int(input_list[0])                                          
        d = [int(x) for x in input_list[1].strip().split()]             
        M = int(input_list[2])                                         
        c = [int(x) for x in input_list[3].strip().split()]            
        K = int(input_list[4])                                         
        conflicts = [list(map(lambda x: int(x) - 1, ij.split())) for ij in input_list[5:]]   
        return N,d,M,c,K,conflicts

def greedy(N, D, M, C, conflicts):
    time_table = np.array([(0,0,0) for _ in range(N)])
    scheduled = np.zeros((N, M, 4), dtype=int)
    cur_day = 0
    exclude = {}
    for i,j in conflicts:
        exclude[i] = exclude.get(i, []) + [j]
        exclude[j] = exclude.get(j, []) + [i]
    exams = [(d, i) for i, d in enumerate(D)]
    rooms = [(c, j) for j, c in enumerate(C)]
    
    # sort number of students registered for each subject in decreasing order
    exams.sort(reverse=True, key=lambda x: x[0])

    # sort capacity of rooms in decreasing order
     rooms.sort(reverse=True, key=lambda x: x[0])

# looping through each subject and assigning it to the earliest available shift in the first available room with enough capacity.
scheduled_subs = 0
while scheduled_subs < len(exams):
    exam = exams[scheduled_subs]
    d, i = exam
    for room in rooms:
        c, j = room
        for k in range(4):
            if (scheduled[cur_day][j][k] + d <= c) and (scheduled[cur_day][j][k] == 0):
                # check if there is another subject registered or full of capacity of room
                conflict = False
                for ii in range(i):
                    if (time_table[ii][0] == cur_day and time_table[ii][2] == k) and ((ii in exclude.get(i, [])) or time_table[ii][1] == j ): # check if there is another subject registered or conflict
                        conflict = True
                        break
                if conflict:
                    continue
                scheduled[cur_day][j][k] += d
                time_table[i] = (cur_day, j, k)
                break
        else:
            continue
        break
    else:
        #If there is no room left in the last period, increasing the current day by 1
        cur_day += 1
        scheduled_subs -=1
    scheduled_subs += 1
            
    # return the minimum days for the exam
    return cur_day + 1, time_table

def main():
    n,d,m,c,k,conflicts = input_(input())
    num_days, time_table = greedy(n,d,m,c, conflicts)
    for exam, (i,j,k) in enumerate(time_table):
        print(f"Subject {exam+1} is assigned at day {i+1}, room {j+1}, and shift {k+1}")
    print(f"Minimum days for the exams: {num_days}")

if __name__ == "__main__":
  main()
