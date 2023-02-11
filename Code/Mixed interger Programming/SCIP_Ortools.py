import sys
import time
from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

def getinput():
    filename = input()
    with open(filename) as f:
        [N] = [int(x) for x in f.readline().split()]
        d = [int(x) for x in f.readline().split()]
        [M] = [int(x) for x in f.readline().split()]
        c = [int(x) for x in f.readline().split()]
        [K] = [int(x) for x in f.readline().split()]
        conflict = []
        for _ in range(K):
            conflict.append([int(x)-1 for x in f.readline().split()])
    return N, c, M, d, K, conflict
N,c,M,d,K,conflict = getinput()

#Decision Variable
X = [[[solver.IntVar(0,1, 'X({i}, {j}, {k})'.format(i=i, j=j, k=k)) for k in range(N)] for j in range(M)] for i in range(N)]
Y = solver.IntVar(0,N-1, 'Y')

#1st constraint: hai môn thi conflict không được xếp trùng kíp.
for conf in conflict:
    c1,c2 = conf
    for k in range(N):
        schedule = solver.Constraint(0, 1)
        for j in range(M):
            schedule.SetCoefficient(X[c1-1][j][k], 1)
            schedule.SetCoefficient(X[c2-1][j][k], 1)

#2nd constraint: một môn i chỉ được xếp duy nhất một lần.
for i in range(N):
    schedule  = solver.Constraint(1,1)
    for j in range(M):
        for k in range(N):
            schedule.SetCoefficient(X[i][j][k], 1)

#3rd constraint: một phòng chỉ được xếp tối đa một môn vào một kíp.
for j in range(M):
    for k in range(N):
        schedule = solver.Constraint(0,1)
        for i in range(N):
            schedule.SetCoefficient(X[i][j][k],1)

#4th constraint: xếp môn thi vào phòng với sức chứa phù hợp.
for i in range(N):
    for j in range(M):
        for k in range(N):
            schedule = solver.Constraint(0, c[j])
            schedule.SetCoefficient(X[i][j][k],d[i])

#5th constraint: x[i][j][k]*k <= y
#tìm phương án sao cho tổng của tất cả các kíp là nhỏ nhất
for i in range(N):
    for j in range(M):
        for k in range(N):
            schedule = solver.Constraint(-solver.infinity(),0)
            schedule.SetCoefficient(Y,-1)
            schedule.SetCoefficient(X[i][j][k],k)

#define object
obj = solver.Objective()
obj.SetCoefficient(Y,1)
obj.SetMinimization()

#result
start_time = time.time()
result_status = solver.Solve()
if result_status == pywraplp.Solver.OPTIMAL:
    y = 1
    for i in range(N):
        for j in range(M):
            for k in range(N):
                if X[i][j][k].solution_value() == 1:
                    print('Xếp môn {i} vào phòng {j} trong kíp {k}'.format(i=i+1, j=j+1,k=k+1))
                    y = max(y,k)
    print('tổng số ngày diễn ra kì thi là {t}'.format(t=y//4+1))
else:
    print("No Solution")

print("--- %s seconds ---" % (time.time() - start_time))
