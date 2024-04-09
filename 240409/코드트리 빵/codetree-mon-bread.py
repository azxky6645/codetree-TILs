n, m = map(int, input().split())

arr = [list(map(int, input().split())) for _ in range(n)]

cur = [(-1,-1)]*(m+1)   #각 사람들의 현재 좌표
base = [(-1,-1)]*(m+1)  #각 사람이 배치될 베이스캠프좌표 초기화
target = [(-1,-1)]*(m+1) #각 사람의 목표 편의점 좌표 초기화

for idx in range(1,m+1):
    i,j = list(map(int, input().split()))
    target[idx] = [i-1,j-1]

ans = 1 #while문 돌면서 ans(=시간)를 한번씩 증가시키기

# 갈수있는곳 = -1이 아닌곳
# 사람이 가면 + 100
# 베이스캠프 위치 = 1
# 베이스캠프에 도착하는 사람이 목적이면 -2
# 편의점위치 = 2
# 편의점에 도착하는사람이 목적이면 -3
# 사람이 빠져나오면 -100 다시
di = [1,0,0,-1]
dj = [0,-1,1,0]
while True:
    for idx in range(1, m + 1):
        # 1) 격자위의 사람들 -> 편의점쪽으로 이동
        if cur[idx] != (-1,-1): # 격자위에있는 사람이면
            si, sj = cur[idx]   # 현재위치에서
            ti, tj = target[idx]
            for d in range(4):
                ni = si + di[d]
                nj = sj + dj[d]
                if abs(ni-ti) < abs(si-ti) or abs(nj-tj) < abs(sj-tj):
                    if arr[ni][nj] >= 0:
                        cur[idx] = [ni, nj]  # 사람의 새로운 좌표 저장
                        arr[si][sj] -= 100  # 원래 위치를 빠져나옴 처리
                        arr[ni][nj] += 100
                        break

            if (ni, nj) == (ti, tj):    # 만약 목표편의점에 도착한다면
                cur[idx] = (-1, -1)     # 사람은 퇴장처리하고
                arr[ni][nj] -= 103      # 해당 좌표의 한사람빼기 -100, 해당편의점 제거

        # 각 사람별 목표 편의점에 가장 가까운 베이스 찾기
        if idx == ans:
            ti, tj = target[idx]    # idx번 사람의 목표 편의점 좌표
            bi, bj = n+1, n+1
            mn = 2*n
            for i in range(n):
                for j in range(n):
                    if arr[i][j] == 1:
                        if abs(ti-i)+abs(tj-j)<mn:
                            mn = abs(ti-i)+abs(tj-j)
                            bi, bj = i, j
                        elif abs(ti-i)+abs(tj-j)==mn:
                            if bi > i:
                                bi, bj = i, j
                            if bi == i and bj > j:
                                bj = j
            base[idx] = [bi,bj]     # 베이스 위치 결정
            cur[idx] = [bi,bj]      # 사람의 현재위치 = 베이스 위치
            arr[bi][bj] = -2        # 베이스에 들어간사람이 있으면 앞으로 거긴 못감

    cnt = 0
    for i in cur:
        if i != (-1,-1):
            cnt += 1
    if cnt == 0:
        break

    ans += 1

print(ans)