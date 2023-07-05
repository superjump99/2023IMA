from function import *
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans



data = data_proprecssing(df)
print(data)

orders = mymethod(data)
print(orders)

titration_CBM = constraints(orders)
# print(f'{titration_CBM=}')

order_volume = volumePerOrder(titration_CBM)            # 각 주문 번호별 부피 계산 해보기
# print(order_volume)

count, candi_volume = candidateVolume(order_volume)     # 가능한 부피 및 해당 개수 파악
# print(count)
# print(candi_volume)


############## kmeans를 통한 CBM 찾아보기 ##############
if __name__ == '__main__':
    transpose_df = pd.DataFrame(titration_CBM).transpose()
    print(transpose_df)

    ### 적잘한 K 찾기 ###
    # Inertia(군집 내 거리제곱합의 합) value (적정 군집수)
    ks = range(1, 10)
    inertias = []
    for k in ks:
        model = KMeans(n_clusters=k)
        model.fit(transpose_df)
        inertias.append(model.inertia_)

    # plot
    plt.figure(figsize=(4, 4))
    plt.plot(ks, inertias, '-o')
    plt.xlabel('number of clusters, k')
    plt.ylabel('inertia')
    plt.xticks(ks)
    plt.show()

    ### K-Means clustering 학습 ###
    clust_model = KMeans(n_clusters=3, random_state = 23)

    clust_model.fit(transpose_df)  # unsupervised learning

    centers = clust_model.cluster_centers_  # 각 군집의 중심점
    print(pd.DataFrame(centers))

    pred = clust_model.predict(transpose_df)  # 각 예측군집
    # print(pred)

    clust_df = transpose_df.copy()
    clust_df['clust'] = pred
    print(clust_df)

    cluster_mean = clust_df.groupby('clust').mean()
    print(cluster_mean)
