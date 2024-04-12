L, N, Q = map(int, input().split())

trap_arr = [[-2]*(L+2)] + [[-2] + list(map(int, input().split())) + [-2] for i in range(L)] + [[-1]*(L+2)]

k_arr = [[-2]*(L+2)] + [[-2] + [0]*L + [-2] for i in range(L)] + [[-2]*(L+2)]

first_hp = [0]*(N+1)
cur_hp = [0]*(N+1)
first_hp[0] = 0
cur_hp[0] = 0

knights = {}

di = [-1,0,1,0] # 상 우 하 좌
dj = [0,1,0,-1]

for i in range(1,L+1):
    for j in range(1, L+1):
        if trap_arr[i][j] != 0:
            trap_arr[i][j] *= -1

for idx in range(1, N+1):
    i, j, h, w, k = map(int, input().split())
    knights[idx] = [i,j,h,w]
    first_hp[idx], cur_hp[idx] = k, k


for idx in range(1, N+1):
    ki, kj, kh, kw = knights[idx]
    for r in range(kh):
        for c in range(kw):
            k_arr[ki+r][kj+c] = idx

from collections import deque

def bfs(idx, d):
    push_set = set()
    q = deque()
    q.append(idx)

    while q:
        cidx = q.popleft()
        ci, cj, ch, cw = knights[cidx]
        push_set.add(cidx)

        for r in range(ch):
            for c in range(cw):
                ni, nj = ci + di[d]+r, cj + dj[d]+c
                # 격자 밖이거나 벽에 부딪히면 그냥 셋비우고 종료
                if 0 >= ni or ni > L or 0 >= nj or nj >L or trap_arr[ni][nj] == -2:
                    push_set = set()
                    return push_set

                # 사람에게 부딪히면, 그사람추가
                if k_arr[ni][nj] > 0:
                    n_idx = k_arr[ni][nj]
                    if n_idx not in push_set:
                        push_set.add(n_idx)
                        q.append(n_idx)

    return push_set


for t in range(1,Q+1):
    # 왕의 명령, oidx 기사에게 od 방향으로 한칸 움직여라: order
    oidx, od = map(int, input().split())

    # [1] 기사 이동
    # [1-1] 살아있는 기사만 움직임
    if cur_hp[oidx] <= 0: # 죽었으면 라운드종료
        continue
    else:
        oi, oj, oh, ow = knights[oidx]  #명령받은기사 좌표 높이폭

    # [1-2-1] 움직이려는 위치에 다른 기사가 있으면 밀어낼 기사들 목록 확보
    push_set = bfs(oidx, od)

    if len(push_set) > 0:       # 여기서 밀어낼 목록이 채워져있으면, 밀고 아니면 벽에 막힌것
        for idx in push_set:
            pi, pj, ph, pw = knights[idx]
            npi, npj = pi + di[od], pj + dj[od]
            knights[idx] = [npi, npj, ph, pw]       #옮긴 좌표 저장

        # [2] 대결 데미지,
        # 모든 좌표 이동처리
            for r in range(ph):
                for c in range(pw):
                    k_arr[pi + r][pj + c] -= idx
                    k_arr[npi+r][npj+c] += idx
                    # 이동이 끝나고 함정에 대한 점수 처리, 단, oidx 기사는 점수 안깎임 사망도 같이 처리됨
                    if idx != oidx and trap_arr[npi+r][npj+c] == -1:
                        cur_hp[idx] -= 1
            # 점수 다깎고나서, 체력이 0이하되면 제거
            if cur_hp[idx] <= 0:
                for i in range(1,L+1):
                    for j in range(1, L+1):
                        if k_arr[i][j] == idx:
                            k_arr[i][j] = 0
    print()

ans = 0

for idx in range(1,N+1):
    if cur_hp[idx] > 0:
        ans += first_hp[idx] - cur_hp[idx]

print(ans)