from collections import deque
N, M, K = map(int, input().split())

arr = [list(map(int, input().split())) for i in range(N)]
record = [[0]*M for _ in range(N)] #포탑이 제일 최근에 발사한 턴을 기록하는 배열

di = [0,1,0,-1,1,1,-1,-1]
dj = [1,0,-1,0,1,-1,1,-1]


def attack(si,sj,ti,tj):
    q = deque()
    v = [[[] for _ in range(M)] for _ in range(N)]  # 경로 저장용

    q.append((si,sj))
    v[si][sj] = (si,sj)
    damage = arr[si][sj]

    while q:
        ci,cj = q.popleft()
        if (ci,cj) == (ti,tj):
            arr[ti][tj] = max(arr[ti][tj]-damage, 0) # 목표물에 타격
            while True:
                ci,cj = v[ci][cj]   #직전좌표
                if (ci,cj) == (si,sj):
                    return True
                arr[ci][cj] = max(0, arr[ci][cj]-damage//2)
                fset.add((ci,cj))

        for d in range(4):
            ni = (ci+di[d]) % N
            nj = (cj+dj[d]) % M  # 반대편으로 연결함
            if len(v[ni][nj]) ==0 and arr[ni][nj] >0:
                q.append((ni,nj))
                v[ni][nj] = (ci,cj)
    return False

def bomb(si,sj,ti,tj):
    damage = arr[si][sj]
    arr[ti][tj] = max(arr[ti][tj] - damage, 0)
    for d in range(8):
        ni = (ti+di[d]) % N
        nj = (tj+dj[d]) % M
        if (ni, nj) != (si, sj):
            arr[ni][nj] = max(arr[ni][nj] - damage//2, 0)
            fset.add((ni,nj))


for t in range(1, K+1):
    # 가장 약한 공격자 선정
    mn = 5001
    last = 0
    si, sj = -1,-1
    remained = N*M

    for i in range(N):
        for j in range(M):
            if arr[i][j] != 0 and mn >= arr[i][j] and last <= record[i][j]:  #안부서진, 공격력이 낮은, 가장 최근에 공격한
                mn = arr[i][j]
                si, sj = i, j
                last = record[i][j]

    #가장 공격력 높은 대상 선정
    mx = 0
    oldest = K+1
    ti, tj = -1, -1
    for i in range(M-1, -1, -1):  #거꾸로돌면 자동으로 행열이 작은것으로 저장해줌
        for j in range(N-1, -1, -1):
            if arr[i][j] != 0 and mx <= arr[i][j] and oldest >= record[i][j]:  #안부서진, 공격력 높은, 가장 처음에 공격한
                mx = arr[i][j]
                ti, tj = i, j

    arr[si][sj] += M + N  # M+N만큼 공격력 증가
    record[si][sj] = t

    fset = set()
    fset.add((si, sj))
    fset.add((ti, tj))
    if attack(si,sj,ti,tj) == False:    #레이저공격이 실패한경우
        bomb(si,sj,ti,tj)               # 포탄공격

    for i in range(N):
        for j in range(M):
            if arr[i][j] != 0 and (i,j) not in fset:
                arr[i][j] += 1

    for i in range(N):
        remained -= arr[i].count(0)
    if remained <= 1:
        break

result = 0
for i in range(N):
    for j in range(M):
        result = max(result, arr[i][j])

print(result)