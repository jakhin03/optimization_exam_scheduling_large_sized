#!/usr/bin/python3

import numpy as np
import sys

def input_():
    [N,M] = [int(x) for x in sys.stdin.readline().split()]                                      # n: số môn thi, m số lượng phòng thi
    d = [int(x) for x in sys.stdin.readline().split()]                                          # d: danh sách số lượng sinh viên đăng ký mỗi môn (d[i] là số lượng sinh viên đăng ký môn i)
    c = [int(x) for x in sys.stdin.readline().split()]                                          # c: danh sách số lượng chỗ ngồi mỗi phòng (c[j] là số lượng chỗ ngồi của phòng j)
    K = int(input())
    conflicts = [list(map(lambda x: int(x)-1, sys.stdin.readline().split())) for _ in range(K)] # conflicts: danh sách 2 môn thi (i,j) trùng sinh viên đăng ký 
    return N,d,M,c,K,conflicts
    
def greedy(N, D, M, C, conflicts):
    time_table = [(0,0,0) for _ in range(N)]
    scheduled = np.zeros((N, M, 4), dtype=int)
    current_day = 0
    exclude = {}
    for i,j in conflicts:
        exclude[i] = exclude.get(i, []) + [j]
        exclude[j] = exclude.get(j, []) + [i]

    # sắp xếp các môn thi theo số lượng đăng ký giảm dần
    exams = [(d, i) for i, d in enumerate(D)]
    exams.sort(reverse=True, key=lambda x: x[0])

    # sắp xếp các phòng thi theo sức chứa giảm dần
    rooms = [(c, j) for j, c in enumerate(C)]
    rooms.sort(reverse=True, key=lambda x: x[0])

    # gán môn thi vào kíp sớm nhất
    for exam in exams:
        d, i = exam
        for room in rooms:
            c, j = room
            for k in range(4):
                if (scheduled[current_day][j][k] + d <= c) and (scheduled[current_day][j][k] == 0):
                    # kiểm tra trường hợp có môn đã đăng ký hoặc phòng không đủ sức chứa
                    conflict = False
                    for ii in range(i):
                        if (time_table[ii][0] == current_day and time_table[ii][2] == k) and ((ii in exclude.get(i, [])) or time_table[ii][1] == j ):
                            conflict = True
                            break
                    if conflict:
                        continue
                    scheduled[current_day][j][k] += d
                    time_table[i] = (current_day, j, k)
                    print("Subject %d is time_tabled on day %d room %d and period %d"%(i+1, current_day+1, j+1, k+1))
                    break
            else:
                continue
            break
        else:
            current_day += 1
            
    # trả về số ngày tối thiểu để diễn ra kì thi
    return current_day + 1, time_table

def main():
  n,d,m,c,k,conflicts = input_()
  num_days, time_table = greedy(n,d,m,c, conflicts)
  for exam, (i,j,k) in enumerate(time_table):
    print(exam+1,k+1,j+1) #môn, kíp, phòng
  
if __name__ == "__main__":
  main()
