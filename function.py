import pandas as pd

fileName = '박스규격_최적화_data.xlsx'
df = pd.read_excel(fileName, index_col=0)

def data_proprecssing(df):
    groups = df.groupby("주문번호")
    dataSet = dict(list(groups))
    matrix = {}
    for i in range(1,len(dataSet)+1):
        row = dataSet[i].values.tolist()
        matrix[i] = row

    result = {}
    for orderNumber, items in matrix.items():
        group = []
        for item in range(len(items)):
            group.append(items[item][1:])
        result[orderNumber] = group
    return result


def mymethod(data):
    result = {}
    for orderNumber, items in data.items():

        if len(items) > 1:
            while len(items) != 1:
                a = items.pop((items.index(items[0])))
                b = items.pop((items.index(items[0])))
                box = []
                while a != []:
                    val = a.pop(a.index(max(a)))
                    val += b.pop(b.index(min(b)))
                    box.append(val)
                items.append(box)

        result[orderNumber] = items
    return result

def constraints(orders):
    # step 1 : mymethod으로 얻은 값에 필요한 최소 CBM 찾기 -> 현재 주문에 대해서 5단위로 구성된 가장 적합한 CBM 찾기
    result_CBM = []
    for item in orders:
        SearchCBM = []
        WDH = orders[item][0]
        # print(WDH)
        for k in range(len(WDH)):
            i = 1
            while 5 * i <= WDH[k]:
                i += 1
            SearchCBM += [5 * i]
        result_CBM.append(tuple(SearchCBM))

    # step 2 : 적정CBM(titrationCBM) 딕셔너리에 각 주문별 필요한 WDH 매칭
    result = dict()
    for i in range(len(result_CBM)):
        result[i + 1] = result_CBM[i]
    return result


# 주문별 부피 계산
def volumePerOrder(const_order):
    order_volume = dict()
    for i in range(len(const_order)):
        ith_volume = const_order[i+1][0] * const_order[i+1][1] * const_order[i+1][2]
        order_volume[i+1] = ith_volume
    return order_volume


 # 부피별로 개수 카운트
def candidateVolume(order_volume):
    count = {}
    candi_volume = []
    for i in order_volume.values():
        try:
            count[i] += 1
        except:
            count[i] = 1
        finally:
            if i not in candi_volume:
                candi_volume.append(i)
    count = (sorted(count.items(), key=lambda x: x[1], reverse=True))

    return count, candi_volume