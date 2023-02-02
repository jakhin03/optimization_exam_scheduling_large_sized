from collections import defaultdict
import sys

def input_():
    [N,M] = [int(x) for x in sys.stdin.readline().split()]  # n: số môn thi, m số lượng phòng thi
    d = [int(x) for x in sys.stdin.readline().split()]      # d: danh sách số lượng sinh viên đăng ký mỗi môn (d[i] là số lượng sinh viên đăng ký môn i)
    c = [int(x) for x in sys.stdin.readline().split()]      # c: danh sách số lượng chỗ ngồi mỗi phòng (c[j] là số lượng chỗ ngồi của phòng j)
    K = int(input())
    conflicts = []                                          # conflicts: danh sách 2 môn thi (i,j) trùng sinh viên đăng ký 
    for _ in range(K):
        conflicts.append([int(x)-1 for x in sys.stdin.readline().split()])
    return N,d,M,c,K,conflicts
def schedule_exams(N, D, M, C, conflicts):
    schedule = [[0]*N] * N
    days = defaultdict(lambda : [[0, 0, 0, 0] for j in range(M)])
    current_day = 0
    
    # sắp xếp các môn thi theo số lượng đăng ký giảm dần
    exams = [(d, i) for i, d in enumerate(D)]
    exams.sort(reverse=True)
    
    # sắp xếp các phòng thi theo sức chứa giảm dần
    rooms = [(c, j) for j, c in enumerate(C)]
    rooms.sort(reverse=True)
    
    # gán môn thi vào kíp sớm nhất
    for exam in exams:
        d, i = exam
        assigned = False
        for room in rooms:
            c, j = room
            for k in range(4):
                if days[current_day][j][k] + d <= c:
                    # check if there is any conflict with assigned exams
                    conflict = False
                    for ii in range(i):
                        if schedule[ii][0] == current_day and schedule[ii][1] == j and schedule[ii][2] == k:
                            conflict = True
                            break
                    if conflict:
                        continue
                    days[current_day][j][k] += d
                    schedule[i] = (current_day, j, k)
                    assigned = True
                    break
            if assigned:
                break
        if not assigned:
            current_day += 1
    
    # trả về số ngày tối thiểu để diễn ra kì thi
    return current_day + 1, schedule

def main():
  n,d,m,c,k,conflicts = input_()
  num_days, schedule = schedule_exams(n,d,m,c, conflicts)
  for exam, (i,j,k) in enumerate(schedule):
    print(exam+1,k+1,j+1) 
  
if __name__ == "__main__":
  main()

