import sys
import time
from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
start_time = time.time()

def getinput():
    N = int(input())
    d = [int(x) for x in sys.stdin.readline().split()]
    M = int(input())
    c = [int(x) for x in sys.stdin.readline().split()]
    K = int(input())
    conflict = []
    for _ in range(K):
        conflict.append([int(x) for x in sys.stdin.readline().split()])
    return N,c,M,d,conflict
N,c,M,d,conflict = getinput()

#Decision Variable
x = [[[solver.IntVar(0,1, 'x({i}, {j}, {k})'.format(i=i, j=j, k=k)) for k in range(N)] for j in range(M)] for i in range(N)]
y = solver.IntVar(0,N-1, 'y')

#1st constraint: hai môn thi conflict không được xếp trùng kíp.
for conf in conflict:
    c1,c2 = conf
    for k in range(N):
        cstr = solver.Constraint(0, 1)
        for j in range(M):
            cstr.SetCoefficient(x[c1-1][j][k], 1)
            cstr.SetCoefficient(x[c2-1][j][k], 1)

#2nd constraint: một môn i chỉ được xếp duy nhất một lần.
for i in range(N):
    cstr  = solver.Constraint(1,1)
    for j in range(M):
        for k in range(N):
            cstr.SetCoefficient(x[i][j][k], 1)

#3rd constraint: một phòng chỉ được xếp tối đa một môn vào một kíp.
for j in range(M):
    for k in range(N):
        cstr = solver.Constraint(0,1)
        for i in range(N):
            cstr.SetCoefficient(x[i][j][k],1)

#4th constraint: xếp môn thi vào phòng sao cho lượng sinh viên ngồi đủ trong phòng.
for i in range(N):
    for j in range(M):
        for k in range(N):
            cstr = solver.Constraint(0, c[j])
            cstr.SetCoefficient(x[i][j][k],d[i])

#5th constraint: x[i][j][k]*k <= y
#tìm phương án sao cho tổng của tất cả các kíp là nhỏ nhất
for i in range(N):
    for j in range(M):
        for k in range(N):
            cstr = solver.Constraint(-solver.infinity(),0)
            cstr.SetCoefficient(y,-1)
            cstr.SetCoefficient(x[i][j][k],k)

#define object
obj = solver.Objective()
obj.SetCoefficient(y,1)
obj.SetMinimization()

#result
result_status = solver.Solve()
if result_status == pywraplp.Solver.OPTIMAL:
    y = 1
    for i in range(N):
        for j in range(M):
            for k in range(N):
                if x[i][j][k].solution_value() > 0:
                    print('Xếp môn {i} vào phòng {j} trong kíp {k}'.format(i=i+1, j=j+1,k=k+1))
                    y = max(y,k)
    print('tổng số ngày diễn ra kì thi là {t}'.format(t=y//4+1))
else:
    print("No Solution")

print("--- %s seconds ---" % (time.time() - start_time))