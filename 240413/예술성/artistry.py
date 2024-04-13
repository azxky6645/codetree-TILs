from collections import deque
n = int(input())

arr = [list(map(int, input().split())) for i in range(n)]
t_arr = [[0] * n for i in range(n)]

di = [-1,1,0,0]
dj = [0,0,1,-1]

def grouping(i, j, idx):
    q = deque()
    q.append((i,j))
    cnt = 0
    while q:
        ci, cj = q.popleft()
        visited[ci][cj] = 1
        t_arr[ci][cj] = idx
        cnt += 1
        for d in range(4):
            ni, nj = ci+di[d], cj+dj[d]
            if 0<=ni<n and 0<=nj<n and \
                    not visited[ni][nj] and arr[ci][cj] == arr[ni][nj]:
                t_arr[ni][nj] = idx
                visited[ni][nj] = 1
                q.append((ni,nj))

    group[idx] = (arr[i][j], cnt, (i,j))

def cal(a, b):
    an, acnt, (ai, aj) = group[a]
    bn, bcnt, _ = group[b]
    meet = 0
    q = deque()
    q.append((ai, aj))
    v = [[0] * n for i in range(n)]
    while q:
        i, j = q.popleft()
        v[i][j] = 1
        for d in range(4):
            ni, nj = i+di[d], j+dj[d]
            if 0 > ni or ni >= n or 0 > nj or nj >= n or v[ni][nj]:
                continue
            # 움직인 위치의 그룹 인덱스가 b이면 카운팅
            if t_arr[ni][nj] == b:
                meet += 1
            # 움직인 위치가 a로 같으면 그 좌표 q에 추가 및 방문처리
            if t_arr[ni][nj] == t_arr[i][j]:
                v[ni][nj] = 1
                q.append((ni,nj))

    score = (acnt + bcnt) * an * bn * meet
    return score



ans = 0
for t in range(4):  # 전체 게임은 3회인데,
    #[1] 예술 점수 계산
    # 그룹핑
    group = {}  # 인덱스: (해당그룹을 이루는 숫자, 칸 개수, (내부의 아무좌표))
    visited = [[0] * n for i in range(n)]  # bfs 돌때마다 방문처리용
    idx = 0 # 그룹핑에 필요한 그룹인덱스
        # 그룹화된 배열
    for i in range(n):
        for j in range(n):
            if visited[i][j] == 0:
                idx += 1
                grouping(i,j,idx)

    # 각 그룹별 조화 점수의 합산 계산
    harmony = 0
    for a in range(1,idx):
        for b in range(a+1,idx+1):
            harmony += cal(a, b)

    ans += harmony

    # 0초기값 + 1,2,3회 회전한 조화점수의 합산 계산 후 종료
    if t == 3:
        print(ans)
        break

    # [2]부위별 회전
    m = n//2                  # 중앙 행,열 좌표

    for i in range(m):
        for j in range(m):
            for si,sj in (0, 0),(0, m+1),(m+1, 0),(m+1, m+1):
                t_arr[si+i][sj+j] = arr[si+m-1-j][sj+i]

    for i in range(n):
        for j in range(n):
            if i == m or j == m:
                t_arr[n-1-j][i] = arr[i][j]

    arr = [i[:] for i in t_arr]