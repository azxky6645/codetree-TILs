from collections import deque

n, m, k = map(int, input().split())

arr = [list(map(int, input().split())) for _ in range(n)]
t_arr = [x[:] for x in arr]

visited = [[0]*n for _ in range(n)]

di = [-1,0,1,0]     #상우하좌, 방향순서는 상관없음
dj = [0,1,0,-1]

line = 0
point_d = 0
opp = {0:1,1:0,2:3,3:2}     # 화살표의 방향 인덱싱

def move(ti, tj, arr):
    q = deque()
    q.append((ti, tj))
    qset = []
    global visited

    while q:
        i, j = q.popleft()
        for d in range(4):
            ni = i + di[d]
            nj = j + dj[d]
            # 격좌내 좌표고, 그것이 동선상이 아니면 제거
            if 0 > ni or n <= ni or 0 > nj or n <= nj:
                continue
            if visited[nj][ni] == 1 or arr[ni][nj] == 0:
                continue
            if visited[nj][ni] == 0:
                if arr[i][j] >= arr[ni][nj] or (arr[i][j] == 1 and arr[ni][nj]==4):
                    if arr[i][j] != 4:
                        qset.append((ni,nj))
                    t_arr[ni][nj] = arr[i][j]
                    q.append((ni, nj))
                    visited[nj][ni] = 1

                else: continue


    arr = [x[:] for x in t_arr]
    visited = [[0]*n for _ in range(n)]

    return arr, qset

# def hit(hi, hj):  # 공에 맞은사람 순서 및 득점 출력 및 맞았으면, 머리꼬리 번호바꾸기
#     h_idx = 1
#     q = deque()
#     q.append((hi, hj))
#     global visited
#
#     while q:
#         i, j = q.popleft()
#         visited[i][j] = 1
#         if arr[i][j] == 3:
#             arr[i][j] = 1
#         elif arr[i][j] == 1:
#             arr[i][j] = 3
#             return h_idx
#
#         for d in range(4):
#             ni = i + di[d]
#             nj = j + dj[d]
#             if 0 > ni or n <= ni or 0 > nj or n <= nj or arr[ni][nj] == 4 or arr[ni][nj] == 0:
#                 continue
#             if visited[ni][nj] == 1:
#                 continue
#             if visited[ni][nj] == 0:
#                 h_idx += 1
#                 visited[ni][j] = 1
#                 q.append((ni,nj))
#
#

ans = 0


point = [line, point_d]

for t in range(1,k+1):
    #전체 행렬을 돌면서;
    head_set = set()
    set_list = []
    for i in range(n):
        for j in range(n):
            # 각 조의 머리 찾기
            if arr[i][j] == 3:
                head_set.add((i,j))

    for ti, tj in head_set:
        arr, p_set = move(ti, tj, arr) #꼬리가 속한 모든 집단들을 한칸씩 이동시키기
        set_list.append(p_set[::-1])

    if point[1] % n == 0:       # 우로 향하는 화살표
        for i in range(n):
            if arr[point[0]][i] != 4 and arr[point[0]][i] != 0:
                for idx in range(len(set_list)):
                    if (point[0],i) in set_list[idx]:
                        hit_idx = set_list[idx].index((point[0],i)) + 1
                        tail = set_list[idx][-1]
                        head = set_list[idx][0]
                        # arr[tail[0]][tail[1]] = 1
                        # arr[head[0]][head[1]] = 3
                        break
                ans += hit_idx**2
                break

    elif point[1] % n == 1: # 위로 향하는 화살표
        for i in range(n-1,-1,-1):
            if arr[i][point[0]] != 4 and arr[i][point[0]] != 0:
                for idx in range(len(set_list)):
                    if (i, point[0]) in set_list[idx]:
                        hit_idx = set_list[idx].index((i, point[0])) + 1
                        tail = set_list[idx][-1]
                        head = set_list[idx][0]
                        arr[tail[0]][tail[1]] = 1
                        arr[head[0]][head[1]] = 3
                        break
                ans += hit_idx**2
                break

    elif (n-point[1]) % n == 2: # 좌로 향하는 화살표
        for i in range(n-1, -1, -1):
            if arr[point[0]][i] != 4 and arr[point[0]][i] != 0:
                for idx in range(len(set_list)):
                    if (point[0], i) in set_list[idx]:
                        hit_idx = set_list[idx].index((point[0], i)) + 1
                        tail = set_list[idx][-1]
                        head = set_list[idx][0]
                        arr[tail[0]][tail[1]] = 1
                        arr[head[0]][head[1]] = 3
                        break
                ans += hit_idx**2
                break

    elif (n-point[1]) % n == 3: # 아래로 향하는 화살표
        for i in range(n):
            if arr[i][point[0]] != 4 and arr[i][point[0]] != 0:
                for idx in range(len(set_list)):
                    if (i, point[0]) in set_list[idx]:
                        hit_idx = set_list[idx].index((i, point[0])) + 1
                        tail = set_list[idx][-1]
                        head = set_list[idx][0]
                        arr[tail[0]][tail[1]] = 1
                        arr[head[0]][head[1]] = 3
                        break
                ans += hit_idx**2
                break

    point[0] = (point[0] + 1) % n
    if point[0] % n == 0 and t > 1:   #마지막줄에 닿으면 방향전환
        point[1] += 1


print(ans)