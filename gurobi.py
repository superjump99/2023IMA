from gurobipy import *
from function import *


data = data_proprecssing(df)
# print(data)

orders = mymethod(data)
# print(orders)

# step 1 : myalgorithm으로 얻은 값에 필요한 최소 CBM 찾기 -> 현재 주문에 대해서 5단위로 구성된 가장 적합한 CBM 찾기
result_CBM = []
wdh = []
for item in orders:
    SearchCBM = []
    WDH = orders[item][0]
    wdh.append(tuple(WDH))
    # print(WDH)
    for k in range(len(WDH)):
        i = 1
        while 5 * i <= WDH[k]:
            i += 1
        SearchCBM += [5 * i]
    result_CBM.append(tuple(SearchCBM))

# step 2 : 적정CBM(titrationCBM) 딕셔너리에 각 주문별 필요한 WDH 매칭
titration_CBM = dict()
for i in range(len(result_CBM)):
    titration_CBM[i + 1] = result_CBM[i]
# print(f'{titration_CBM=}')

order_volume = volumePerOrder(titration_CBM)            # 각 주문 번호별 부피 계산 해보기
# print(order_volume)

# 5단위로 만든 표준 박스의 부피(계수)
c = []
for val in order_volume.values():
    c.append(val)
print(c)

count, candi_volume = candidateVolume(order_volume)     # 가능한 부피 및 해당 개수 파악
print(count)
print(candi_volume)



################# gurobi #################
if __name__=="__main__":
    # Parameters
    k = 3               # CBM의 개수
    c = candi_volume    # 5단위로 만든 표준 박스의 부피(계수)
    p = wdh             # 주문번호에 해당하는 아이템셋의 부피

    # Model
    model = Model()

    # Decision Variables
    y = model.addVars(len(c), vtype=GRB.BINARY, name="pick")        # 표준 박스 i가 사용 되는지
    x = model.addVars(len(c),len(p), vtype=GRB.BINARY, name="box")  # 표준 박스 i에 주문 번호 j가 들어갈 수 있는지

    # Objective function  -> 표준 박스 i의 부피 최소화
    model.setObjective(quicksum(c[i]*y[i] for i in range(len(c))), GRB.MINIMIZE)

    # Constraints
    # 표준 박스 i의 개수는 k개
    model.addConstr(quicksum(y[i] for i in range(len(c))) == k)
    # 총 가능한 경우의 수는 주문 번호를 만족해야함
    model.addConstr(quicksum(quicksum(x[i, j] for j in range(len(p))) for i in range(len(c))) == 50)
    # 표준박스 i에 가능한 주문번호 j의 합은 50을 넘길 수 없음, 안 들어가는 것은 가능
    for i in range(len(c)):
        model.addConstr(quicksum(x[i,j] for j in range(len(p))) <= 50)
    # 사용되는 표준박스 i는 가능한 표준박스 i의 주문번호에 해당하는 부피보다 커야함
    for i in range(len(c)):
        model.addConstr(c[i]*y[i] - quicksum(p[j][0]*p[j][1]*p[j][2]*x[i,j] for j in range(len(p))) >= 0)

    model.write('IMA project.lp')
    model.optimize()
    if model.Solcount > 0:
        model.printAttr('X')

