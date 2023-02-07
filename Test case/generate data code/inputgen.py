import random

# Số lượng môn cần xếp lịch
N = 10
# Số lượng phòng thi
M = 5
# Số lượng sinh viên đăng ký mỗi môn
d = [random.randint(50, 100) for _ in range(N)]
# Số lượng chỗ ngồi trong mỗi phòng
c = [random.randint(100, 200) for _ in range(M)]
# Danh sách các cặp môn không thể xếp trùng kíp
conflicts = [(random.randint(0, N-1), random.randint(0, N-1)) for _ in range(N//2)]

# In ra các tham số
print("Number of subjects: ", N)
print("Number of rooms: ", M)
print("Enrollment of each subject: ", d)
print("Capacity of each room: ", c)
print("Conflicts list: ", conflicts)
