n, m, k = map(int,input().split())

#arr는 전부 -1로 둘러싸주기
# g_arr = [[-1]*(n+2)]+ [[-1] + list(map(int,input().split()))+[-1] for i in range(n)] + [[-1]*(n+2)]

g_arr = [[-1]*(n+2)] + [[-1] + [0]*(n)+[-1] for _ in range(n)] + [[-1]*(n+2)]
# 총 지도는 각 격자가 리스트형태로 있어야, 총이 여러개 있을 수 있음
for i in range(1,n+1):
    gun_list = list(map(int, input().split()))
    for j in range(1,n+1):
        g_arr[i][j] = [gun_list[j-1]]

h_arr = [[-1]*(n+2)] + [[-1] + [0]*(n)+[-1] for _ in range(n)] + [[-1]*(n+2)]
p_list = [0]     #사람 객체 담기용도 (n+1)

direct = [(-1,0),(0,1),(1,0), (0,-1)]


class People():
    def __init__(self, idx, s, gun_s, i ,j, d):
        self.idx = idx      #번호
        self.s = s          #능력치
        self.gun_s = gun_s  #총의 능력치
        self.have_gun = False
        self.i = i          #행
        self.j = j          #열
        self.d = d  #방향 (튜플)
        self.total_s = self.gun_s + self.s   #전체 공격력
        self.point = 0


    def get_gun(self, gun_s):    #총을 줍는 경우 실행할 함수 (total을 일일히 바꾸기 싫어서)
        self.gun_s = gun_s
        self.total_s = self.s + gun_s
        self.have_gun = True

    def drop_gun(self):
        self.gun_s = 0
        self.total_s = self.s
        self.have_gun = False

for idx in range(1,m+1):
    i, j, d, s = map(int, input().split())
    p = People(idx, s, 0, i, j, d)
    p_list.append(p)
    h_arr[i][j] = idx

#k만큼 라운드 시작 1라운드부터
for T in range(1,k+1):
    for idx in range(1,len(p_list)):    # 1번사람부터 순서대로
        si, sj = p_list[idx].i, p_list[idx].j   #초기 사람 위치
        ni, nj = si + direct[p_list[idx].d][0], sj + direct[p_list[idx].d][1] #한칸움직인 위치

       # [1] 벽에 부딪힌 경우 반대로 움직임, 방향 처리
        if h_arr[ni][nj] == -1:
            if p_list[idx].d + 2 > 3:   #180도 바꿈
                p_list[idx].d -= 2
            else:
                p_list[idx].d += 2
        ni, nj = si + direct[p_list[idx].d][0], sj + direct[p_list[idx].d][1] #한칸움직인 위치

        p_list[idx].i, p_list[idx].j = ni, nj   #사람 좌표도 바꿔주고
        h_arr[ni][nj] += idx                     #사람맵에서 격자이동도 해주고
        h_arr[si][sj] = 0                    # 빼주고

        #[2] 만약 이동한 방향에 사람이 있다면 싸우기
        if h_arr[ni][nj] != idx:
            other_idx = h_arr[ni][nj]-idx
            if (p_list[idx].total_s > p_list[other_idx].total_s) or \
                (p_list[idx].total_s == p_list[other_idx].total_s and
                 p_list[idx].s > p_list[other_idx].s):
                winner_idx = idx
                loser_idx = other_idx
            else:
                loser_idx = idx
                winner_idx = other_idx

            # 싸워 이긴쪽의 포인트는 total 의 차이만큼 추가
            p_list[winner_idx].point += abs(p_list[winner_idx].total_s - p_list[loser_idx].total_s)

            # 진사람은 총을 버리고 떠남
            if p_list[loser_idx].have_gun:          #총이 있는사람만
                losers_gun = p_list[loser_idx].gun_s       #총을 집고
                p_list[loser_idx].drop_gun()                #내려놓고
                g_arr[ni][nj].append(losers_gun)            # 격자에 총 추가

            for dr in range(4):
                rotate_d = (p_list[loser_idx].d+dr) % 4
                lni, lnj = ni + direct[rotate_d][0], nj + direct[rotate_d][1] # 1칸
                if h_arr[lni][lnj] == 0:          # 제대로 옮겨졌으면 고
                    break
                else:       #근데 벽이거나 사람이 있으면 90도 회전
                    continue
            p_list[loser_idx].d = rotate_d
            h_arr[lni][lnj] += loser_idx
            h_arr[ni][nj] -= loser_idx
            p_list[loser_idx].i, p_list[loser_idx].j = lni, lnj

            if sum(g_arr[lni][lnj]) > 0:  # 바닥에 총이 있다면,
                g_arr[lni][lnj].sort()  # 바닥의 총을 정렬(오름차순)
                mx_gun = g_arr[lni][lnj][-1]  # 맨뒤에것이 가장큰것
                p_list[loser_idx].get_gun(mx_gun)  # 그냥 줍고
                g_arr[lni][lnj].pop()           #격자에서 없어짐 처리

            # 이긴사람은 바닥의 총들중 제일쎈걸 줍고 들고있던걸 버림
            if sum(g_arr[ni][nj]) > 0:
                g_arr[ni][nj].sort()
                mx_gun = g_arr[ni][nj][-1]
                if mx_gun > p_list[winner_idx].gun_s:  # 바닥 중 제일 큰게 내총보다 크면 바꾸기
                    new = g_arr[ni][nj].pop()  # 일단 총을 줍고
                    g_arr[ni][nj].append(p_list[winner_idx].gun_s)  # 내 총을 내려놓고,
                    p_list[winner_idx].get_gun(new)

        else:
        # [3] 만약 움직인 위치에 총이 있다면 판단해서 줍기
            if sum(g_arr[ni][nj]) > 0:   # 바닥에 총이 있다면,
                g_arr[ni][nj].sort()      #바닥의 총을 정렬(오름차순)
                mx_gun = g_arr[ni][nj][-1]    # 맨뒤에것이 가장큰것

                if not p_list[idx].have_gun:  # 총을 안갖고있으면 바로줍기
                    p_list[idx].get_gun(mx_gun) #그냥 줍고
                    g_arr[ni][nj].pop()         # 맨뒤에거 없애기

                else:   #갖고있으면
                    if mx_gun > p_list[idx].gun_s:  #바닥 중 제일 큰게 내총보다 크면 바꾸기
                        new = g_arr[ni][nj].pop()       #일단 총을 줍고
                        g_arr[ni][nj].append(p_list[idx].gun_s)   #내 총을 내려놓고,
                        p_list[idx].get_gun(new)           #바닥의 총을 내껄로 만들기


for i in range(1,m+1):
   print(p_list[i].point, end=' ')