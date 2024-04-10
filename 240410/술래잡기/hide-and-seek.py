n, m, h, k = map(int, input().split())

arr = [[-1]*(n+2)] + [[-1] + [0]*n + [-1] for _ in range(n)] + [[-1]*(n+2)]
visited = [[-1]*(n+2)] + [[-1] + [0]*n + [-1] for _ in range(n)] + [[-1]*(n+2)]

for i in range(1,n+1):
    for j in range(1,n+1):
        arr[i][j] = [0,0,[]] #0은 술래, # 1은 나무 인덱스 #2는 도망자 인덱스

di = [-1,0,1,0,] # 상우하좌 (달팽이모양)
dj = [0,1,0,-1]

ci, cj = int(n/2)+1, int(n/2)+1
cd = 0          # 첫번째 방향은 항상 위
visited[ci][cj] = 1
arr[ci][cj][0] = 1  #술래 위치 초기화
 # 1은 우좌, 2는 하상
direct = [(0, 1), (1, 0), (0, -1), (-1, 0)]

run = {}    # 행, 열, 우좌/하상 방향, 생존여부
ans = 0     #정답
for idx in range(1,m+1):    # 도망자 입력받기
    i, j, d = map(int, input().split())
    run[idx] = [i, j, d-1, True]    # 행, 열, 우좌/하상 방향, 생존True, 죽음False
    arr[i][j][2] = [idx]    #각 위치의 도망자 초기화

for idx in range(h):        #나무 입력 받기 좌표 상관없으니 0부터
    i, j = map(int,input().split())
    arr[i][j][1] = 'tree'

def chaser_move(ci, cj, cd, t, visited,di,dj): #좌표, 방향, 현재 턴
    nci = ci + di[cd]
    ncj = cj + dj[cd]
    ncd = (cd + 1) % 4

    if t!= 1:
        if visited[nci+di[ncd]][ncj+dj[ncd]] == 1:
            ncd = cd
            if visited[nci+di[ncd]][ncj+dj[ncd]] == -1:
                di = di[::-1]
                dj = dj[::-1]
                ncd = (cd + 1) % 4
                for i in range(1,n+1):
                    for j in range(1,n+1):
                        visited[i][j] = 0

    visited[nci][ncj] = 1
    arr[nci][ncj][0] = 1
    arr[ci][cj][0] = 0
    return nci, ncj, ncd


for t in range(1, k+1):
    move = []
    # [1] 도망자 먼저 도망 치기
    for idx in range(1,m+1):
        if run[idx][3] == True:
            si, sj, sd, ss = run[idx]   #초기 도망자의 행,열,방향좌표, 방향, start survive
            nd = sd
            # 각 도망자가 술래와의 거리가 3이하인 경우에만 움직임
            if abs(ci-si) + abs(cj-sj) <= 3:
                ni = si + direct[sd][0]
                nj = sj + direct[sd][1]
                # 다음 위치가 격자 밖이라면
                if arr[ni][nj] == -1:
                    nd = (sd + 2) % 4        #방향을 반대로 틀어줌
                    ni = si + direct[nd][0]
                    nj = sj + direct[nd][1]
                    # 그런데 그 위치에 술래가있으면, 가만히있자
                    if arr[ni][nj][0] == 1:
                        ni = si
                        nj = sj

                # 다음 위치가 격자 밖이 아니라면, 방향 안바꿈
                else:
                    #술래가 있으면 안감
                    if arr[ni][nj][0] == 1:
                        ni = si
                        nj = sj

                # 도망자 이동 처리 및 도망자 정보 업데이트
                arr[si][sj][2].remove(idx)
                arr[ni][nj][2].append(idx)
                run[idx] = ni, nj, nd, ss   # 여기선 딱히 생존여부를 가리지않으니까 ss넣기

    # [2] 술래 움직이기
    # 이동한 후, 좌표와 보는 방향 필요
    ci, cj, cd = chaser_move(ci, cj, cd, t, visited, di, dj)

    # [3] 술래가 시야 보면서 도망자 잡기
    # 술래 시야 방향이 상 이면, 위로 3칸
    sight = set()      # 확인할 격자 좌표 셋
    cnt = 0             # 총 잡은 인원수 세기
    if cd == 0:
        for row in range(3):
            if ci-row > 0:
                sight.add((ci-row,cj))
    # 방향 우
    elif cd == 1:
        for col in range(3):
            if cj + col < n+1:
                sight.add((ci,cj+col))
    # 방향 하
    elif cd == 2:
        for row in range(3):
            if ci+row < n+1:
                sight.add((ci+row,cj))
    # 방향 좌
    elif cd == 3:
        for col in range(3):
            if cj - col > 0:
                sight.add((ci,cj-col))

    # 술래의 시야 안의 격자에서
    for fi, fj in sight:
        # 나무가 없으면 죽이기
        if arr[fi][fj][1] != 'tree':
            cnt += len(arr[fi][fj][2])  # 잡힌 사람만큼 카운트 높이기
            for die in arr[fi][fj][2]:
                run[die] = [-1,-1,-1,False]     # 잡혀서 죽음 처리
            arr[fi][fj][2] = []         # 다잡으면 빈칸처리

    ans += cnt * t                  # 잡은사람 * 현재 라운드 점수 획득

print(ans)