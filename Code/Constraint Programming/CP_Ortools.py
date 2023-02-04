import sys
import time
from ortools.sat.python import cp_model

class CPOrTools:
    def __init__(self):
        # self.read_data(data)
        self.cp_model = cp_model.CpModel()
        self.N = int(input())
        self.d = [int(x) for x in sys.stdin.readline().split()]
        self.M = int(input())
        self.c = [int(x) for x in sys.stdin.readline().split()]
        self.K = int(input())
        self.conflict = []
        for _ in range(self.K):
            self.conflict.append([int(x) for x in sys.stdin.readline().split()])

    def print_solution(self):
        if self.status == cp_model.cp_model_pb2.OPTIMAL:
            print("[RUNTIME]:", self.runtime, "(ms)")
            print("Số kíp tối thiểu:", self.solver.Value(self.obj))
            for i in range(self.N):
                room = 0
                for j in range(self.M):
                    if self.solver.Value(self.Y[i][j]) == 1:
                        room = j + 1
                        break
                print("Môn thi %2d: Kíp %d, Phòng %d" % (i + 1, self.solver.Value(self.X[i]), room))

    def solve(self):
        start = time.time()
        self.setup_variables()
        self.setup_constraints()
        self.setup_objective()
        self.cp_model.Minimize(self.obj)
        self.solver = cp_model.CpSolver()
        self.status = self.solver.Solve(self.cp_model)
        self.runtime = time.time() - start

    def setup_variables(self):
        self.X = [self.cp_model.NewIntVar(1, self.N, "X[%d]" % i) for i in range(1,self.N+1)]
        self.Y = [[self.cp_model.NewIntVar(0, 1, "Y[%d][%d]" % (i, j)) for j in range(self.M)] for i in range(self.N)]

    def setup_constraints(self):
        #1st constraint: hai mon conflict khong xep chung mot kip
        for i in range(self.K):
            self.cp_model.Add(self.X[self.conflict[i][0]-1] != self.X[self.conflict[i][1]-1])

        #2nd constraint: hai mon cung kip khong duoc chung phong
        for j in range(self.M):
            for i1 in range(self.N - 1):
                for i2 in range(i1 + 1, self.N):
                    boolvar = self.cp_model.NewBoolVar("boolvar[%d][%d][%d]" % (j, i1, i2))
                    self.cp_model.Add(self.Y[i1][j] + self.Y[i2][j] < 2).OnlyEnforceIf(boolvar)
                    self.cp_model.Add(self.X[i1] == self.X[i2]).OnlyEnforceIf(boolvar)
                    self.cp_model.Add(self.X[i1] != self.X[i2]).OnlyEnforceIf(boolvar.Not())

        #3rd constraint: mot mon chi xep vao mot phong duy nhat
        for i in range(self.N):
            self.cp_model.Add(sum(self.Y[i]) == 1)

        #4th constraint: xep mon vao phong sao cho sinh vien ngoi du trong phong
        for i in range(self.N):
            self.cp_model.Add(sum([self.Y[i][j] * self.c[j] for j in range(len(self.Y[i]))]) >= self.d[i])
    def setup_objective(self):
        self.obj = self.cp_model.NewIntVar(1,self.N, "objective")
        self.cp_model.AddMaxEquality(self.obj, self.X)

#running
cstr = CPOrTools()
cstr.solve()
cstr.print_solution()
