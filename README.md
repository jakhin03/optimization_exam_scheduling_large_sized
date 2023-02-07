# MiniProject: Xếp lịch thi học kỳ
Miniproject học phần tối ưu hóa HUST-20221

## Chủ đề:
  + Có N môn 1, 2, ..., N cần được xếp lịch thi học kỳ
  + Môn i có số lượng sinh viên đăng ký là d(i)
  + Giữa N môn thi có danh sách các cặp 2 môn (i,j) không thể xếp trùng kíp ngày do cùng sinh viên đăng ký thi
  + Có M phòng thi 1, 2, ..., M; trong đó phòng j có số lượng chỗ ngồi là c[j]
  + Mỗi ngày được chia thành 4 kíp
  + Hãy lập kế hoạch bố trí lịch và phòng cho các môn thi sao cho tổng số ngày diễn ra N môn thi là nhỏ nhất
  
## Input:
  + Dòng 1: ghi N, M
  + Dòng 2: d[1], d[2], ..., d[N]
  + Dòng 3: c[1], c[2], ..., c[M]
  + Dòng 4: ghi số nguyên dương K
  + Dòng 4+k (k = 1, ..., k): ghi i và j (là 2 môn thi trùng sinh viên đăng ký -> không thể xếp trùng ngày, kíp)

## Output:
  + Dòng i (i = 1, ..., N): ghi 3 số nguyên i, s[i], r[i] (trong đó s[i] là kíp và r[i] là phòng mà môn i được xếp vào)
 
## Cấu trúc thư mục:
'''
.
├── Code
│   ├── Constraint Programming
│   │   └── CP_Ortools.py
│   ├── Heuristic
│   │   ├── backtracking.py
│   │   └── greedy.py
│   └── Interger Programming
│       ├── answer.py
│       └── SCIP_Ortools.py
├── Model
│   ├── CP
│   │   └── Model_CP.pdf
│   ├── Heuristic
│   └── IP
├── README.md
└── Test case
    ├── data2.txt
    ├── data3.txt
    ├── data4.txt
    └── data.txt
'''
