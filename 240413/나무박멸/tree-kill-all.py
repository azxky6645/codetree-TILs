n, m, k, c = map(int, input().split())

arr = [[-1001]*(n+2)] + [[-1001]+list(map(int, input().split()))+[-1001] for _ in range(n)] + [[-1001]*(n+2)]

di = [-1,1,0,0]     #나무 인접칸 성장용
dj = [0,0,1,-1]

mi = [-1,-1,1,1]    #우상, 좌상, 우하, 좌하
mj = [1,-1,1,-1]

j_arr = [[0]*(n+2) for i in range(n+2)]     #제초제 배열

ans = 0

for i in range(1, n + 1):
    for j in range(1, n + 1):
        if arr[i][j] == -1:
            arr[i][j] = -1001
            j_arr[i][j] = 1001

for t in range(1,m+1):
    # [1] 나무 성장
    temp_arr = [[0]*(n+2) for i in range(n+2)]  # 여기에 나무 성장 저장 --> 덧셈 처리

    # 각 나무들 돌면서 인접나무만큼 성장
    for i in range(1,n+1):
        for j in range(1,n+1):
            for d in range(4):
                ai, aj = i+di[d], j+dj[d]
                if arr[i][j] > 0 and arr[ai][aj] > 0:   #나무위치에서 인접한 나무가있으면,
                    temp_arr[i][j] += 1

    # 나무 번식 덧셈
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            arr[i][j] += temp_arr[i][j]


    # [2] 나무 번식
    temp_arr = [i[:] for i in arr]     # 여기에 나무 번식 저장 --> 복사저장처리
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            can = []
            for d in range(4):
                ai, aj = i+di[d], j+dj[d]
                # 현재 위치가 나무인 경우, 번식가능한 위치: 제초제, 벽 아닌 경우, 빈공간
                if arr[i][j] > 0 and arr[ai][aj] == 0 and j_arr[ai][aj] <= t:
                    can.append((ai,aj))

            for ai,aj in can:
                temp_arr[ai][aj] += arr[i][j]//len(can)      # 번식나무 더하기

    arr = [i[:] for i in temp_arr]              # 번식 내용까지 저장하기

    # [3] 제초제 뿌리기
    # 가장 많이 나무가 죽을 곳을 찾아야함

    # 각 좌표에 뿌릴때 죽을 사람들
    mx = 0
    ti, tj = n+2, n+2
    go_list = set()
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            # 나무가 있는 위치에 뿌린 경우,
            if arr[i][j] > 0:
                temp_list = set()    # i,j에서 뿌렸을 때, 제초제 확산 좌표
                cnt = 0         # i,j 위치에서 제거될 잡초
                not_go = set()  # 대각선 중 막힌 방향
                for s in range(k+1): # 처음엔 자기자리~ k번째 칸까지
                    for d in range(4):  #우상, 좌상, 우하, 좌하
                        # 이미 막힌 방향이면 안봄
                        if d in not_go:
                            continue
                        # 안막힌 방향이면 봄
                        else:
                            ni, nj = i + mi[d]*s, j + mj[d]*s
                            #자기자리면 한번만돌고 끝
                            if (ni,nj) == (i,j):
                                cnt += arr[ni][nj]
                                temp_list.add((ni,nj))
                                break
                            # 격자밖이면, 안감
                            if 0 >= ni or ni >= n+1 or 0 >= nj or nj >= n+1:
                                not_go.add(d)
                                continue
                            # 나무가없거나 벽이면 거기까지만 뿌림
                            if arr[ni][nj] <= 0:
                                temp_list.add((ni,nj))
                                not_go.add(d)
                                continue
                            if arr[ni][nj] > 0:
                                cnt += arr[ni][nj]
                                temp_list.add((ni, nj))

                # 제초제를 뿌릴자리가 제일크거나 행작 열작이면,
                if (cnt > mx) or (cnt == mx and ti > i) or (cnt == mx and ti == i and tj>j):
                    mx = cnt
                    ti, tj = i, j
                    go_list = temp_list



    # [4] 나무 제거
    temp_arr = [i[:] for i in arr]
    for i,j in go_list:
        j_arr[i][j] = t+c+1
        if arr[i][j] >= 0:
            arr[i][j] = 0

    ans += mx

print(ans)