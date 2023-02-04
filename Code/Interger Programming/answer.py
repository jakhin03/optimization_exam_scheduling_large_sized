from ortools.linear_solver import pywraplp
def input(filename):
   global M, N, c, conflict, d

   with open(filename) as f:
       N = int(f.readline())
       d = [int(i) for i in f.readline().split()]
       M = int(f.readline())
       c = [int(i) for i in f.readline().split()]
       ##lines = []
       #for i in range(M):
        #   lines.append([int(x) for x in f.readline().split()])
       K = int(f.readline())
       conflict = []
       for k in range(K):
           conflict.append([int(x) for x in f.readline().split()])
   return M, N, c, d, conflict
M, N, c, d, conflict = input("/home/conmeobeou1253/Documents/Study material/123.txt")


# Solver
# Create the mip solver with the SCIP backend.
solver = pywraplp.Solver.CreateSolver('SCIP')


# Variables
#tc [i,j,h] is an array of 0-1 variables ,which will be 1 if subject i is assigned to class j in slot h
slot = 4
days = 10
#tc = {}
#for i in range(N) :
    #for j in range(M):
        #for h in range(slot) : 
            #tc[i,j,h] = solver.IntVar(0, 1, "")  

tc = [[[[solver.IntVar(0,1, 'tc({i}, {j}, {h} , {a})'.format(i=i, j=j, h=h , a=a)) for i in range(N)] for j in range(M)] for h in range(slot)] for a in range(days)]
#y = solver.IntVar(0,N, 'y')
#Constraints
#Each subjects is choosed only once per room per slot
for i in range(N):
    cstr = solver.Constraint(1,1)
    for j in range(M) :   
        for h in range(slot) :
            for a in range(days) :   
                cstr.SetCoefficient(tc[a][h][j][i] , 1)
            

#Each room is choosed only once per slot per days
for a in range(days):
    
    for h in range(slot) :
           
        for j in range(M):
            cstr = solver.Constraint(0,1)
            for i in range(N) :
                cstr.SetCoefficient(tc[a][h][j][i],1)
            

#Each slot is choosed only once per room per subjects
#for h in range(slot) :
#    solver.Add(
#        solver.Sum([tc[i,j,h] for i in range (N) for j in range(M)]) <= 1
#    )

#2 subjects can not be assigned same day and same slot
for conf in conflict:
    c1, c2 = conf
    for j in range(len(M)):
        for h in range(slot) :
            for a in range(days) :
                cstr = solver.Constraint(0, 1)
                cstr.SetCoefficient(tc[a][h][j][c1], 1)
                cstr.SetCoefficient(tc[a][h][j][c2], 1)
            
# The number of seats must larger than number of students
for a in range(days) :
    for h in range(slot) :
        for j in range(M) :
            cstr = solver.Constraint(0, c[j])
        #print(c[j])
            for i in range(N):
                cstr.SetCoefficient(tc[a][h][j][i],d[i])
            
        #solver.Add(d[i] <= c[j])

# Objective

objective_terms = []
for i in range(N):
    for j in range(M):
        for h in range(slot) :
            for a in range(days) : 
                objective_terms.append(tc[a][h][j][i] * a)

#print(count)
#print(objective_terms)            
solver.Minimize(solver.Sum(objective_terms))

# Solve
status = solver.Solve()

# Print solution.
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    #print(f'Total day = {solver.Objective().Value()}\n')
    for a in range(days) :
        for h in range(slot):
            for j in range(M):
                for i in range(N) :
                    if tc[a][h][j][i].solution_value() > 0:
                        print(f'Subject {i+1} assigned to room {j+1} in slot {h+1} in day {a+1}.' )
                        #print(tc[a][h][j][i])
else:
    print('No solution found.')
print(f'Time = {solver.WallTime()} ms')