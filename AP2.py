import math
import queue
from queue import PriorityQueue

import matplotlib.pyplot as plt
import numpy as np

def get_data(data,x):
    ans=[]
    for i in x:
        ans.append(data[i])
    return ans

def euclidean_norm(x):
    s=0
    for i in range(len(x)):
        s+= x[i] * x[i]
    return math.sqrt(s)

def distance(x,y,norm):
    z=[0 for _ in range(len(x))]
    for i in range(len(x)):
        z[i]=x[i]-y[i]
    return norm(z)

def DB_scan(data,e,minpts):
    core_points=[]
    for i in range(len(data)):
        close=0
        for j in range(len(data)):
            if i==j: continue
            if distance(data[i], data[j], euclidean_norm)<=e: close+=1
        if close>=minpts: core_points.append(i)

    cluster=[0 for _ in range(len(data))]
    que=queue.Queue()
    clusters=0
    for i in core_points:
        if cluster[i]!=0: continue
        clusters+=1
        cluster[i]=clusters
        que.put(i)
        while que.qsize()>0:
            a=que.get()
            for j in core_points:
                if j==a: continue
                if cluster[j]!=0 : continue
                if distance(data[j], data[a], euclidean_norm)<=e:
                    cluster[j]=clusters
                    que.put(j)

    # clustering non core-points
    for i in range(len(data)):
        if cluster[i]!=0: continue
        for j in range(len(core_points)):
            if distance(data[i]  , data[core_points[j]], euclidean_norm)<=e :
                cluster[i]=cluster[core_points[j]]
                break


    # colors = plt.cm.plasma(np.linspace(0, 1, clusters+1))
    #
    # plt.figure(figsize=(6, 6))
    # for i in range(len(data)):
    #     plt.scatter(data[i, 0], data[i, 1], color=colors[cluster[i]], label=f'point {i + 1}')
    #
    # plt.grid(True)
    # plt.show()

    clst=[[] for _ in range(clusters)]
    for i in range(len(data)):
        if cluster[i]!=0: clst[cluster[i] - 1].append(i) # if it is not noise

    return clst,clusters


def get_core_distance(x,y):
    sor=sorted(x)
    return sor[y-1]


def optics(data, e, minpts):
    core_points=[]
    for i in range(len(data)):
        close=0
        for j in range(len(data)):
            if i==j: continue
            if distance(data[i], data[j], euclidean_norm)<=e: close+=1
        if close>=minpts: core_points.append(i)

    is_core=[0 for _ in range(len(data))]

    for i in core_points:
        is_core[i]=1

    pq=PriorityQueue()

    D=[0 for _ in range(len(data))]
    reachability=[-1 for _ in range(len(data))]
    seen=[0 for _ in range(len(data))]
    order=[]
    for core in core_points:
        if seen[core]!=0: continue
        pq.put((0, core))
        while not pq.empty() :
            score , idx =pq.get()
            if seen[idx]==1: continue
            order.append(idx)
            seen[idx]=1

            if is_core[idx]==0: continue

            for i in range(len(data)):
                D[i]= distance(data[i],data[idx], euclidean_norm)

            dist=get_core_distance(D,minpts)

            for i in range(len(data)):
                if reachability[i]==-1 :
                    reachability[i]=max(dist,D[i])
                    pq.put((reachability[i],i))
                if reachability[i]>max(dist,D[i]):
                    reachability[i]=max(dist,D[i])
                    pq.put((reachability[i],i))

    return order,reachability



# to test optics
# np.random.seed(42)
# cluster1 = np.random.normal(loc=[1, 1], scale=0.15, size=(300, 2))
# cluster2 = np.random.normal(loc=[5, 5], scale=0.2, size=(350, 2))
# cluster3 = np.random.normal(loc=[8, 1], scale=0.15, size=(300, 2))
# noise = np.random.uniform(low=0, high=10, size=(50, 2))
# data = np.vstack((cluster1, cluster2, cluster3, noise))
#
# # Run OPTICS
# order, reachability = optics(data, e=1.0, minpts=5)
#
# print(order)
#
# reachability = np.array(reachability)
# # Plot reachability
# plt.figure(figsize=(10, 4))
# plt.plot(range(len(order)), reachability[order], color='blue')
# plt.xlabel("Points (in OPTICS order)")
# plt.ylabel("Reachability distance")
# plt.title("OPTICS Reachability Plot")
# plt.grid(True)
# plt.show()


# to test dbscan
# np.random.seed(42)
#
# data = np.array([
#     # Cluster 1 (around [1, 1])
#     [1.0, 1.1],
#     [0.9, 0.8],
#     [1.2, 1.0],
#     [1.1, 0.9],
#     [0.8, 1.0],
#
#     # Cluster 2 (around [5, 5])
#     [5.0, 5.1],
#     [5.2, 5.0],
#     [4.9, 5.1],
#     [5.1, 4.8],
#     [5.0, 4.9],
#
#     # Cluster 3 (around [8, 1])
#     [8.0, 1.0],
#     [8.1, 1.1],
#     [7.9, 0.9],
#     [8.2, 1.0],
#     [8.0, 0.8],
#
#     # Noise points
#     [0.0, 7.0],
#     [6.0, 0.0],
#     [3.0, 3.0],
#     [10.0, 10.0]
# ])

# testing dbscan+optics with 2-vectors
# np.random.seed(42)
#
# # --- Cluster 1: around (1,1), two subclusters (dense & sparse)
# sub1a = np.random.normal(loc=[0.8, 1.0], scale=0.05, size=(60, 2))   # dense core
# sub1b = np.random.normal(loc=[1.3, 1.1], scale=0.15, size=(100, 2))  # looser part
#
# # --- Cluster 2: around (5,5), two subclusters (different variance)
# sub2a = np.random.normal(loc=[4.8, 5.0], scale=0.10, size=(80, 2))
# sub2b = np.random.normal(loc=[5.4, 5.3], scale=0.25, size=(120, 2))
#
# # --- Cluster 3: around (8,1), two subclusters
# sub3a = np.random.normal(loc=[8.0, 1.0], scale=0.05, size=(70, 2))
# sub3b = np.random.normal(loc=[8.5, 1.2], scale=0.20, size=(110, 2))
#
# # --- Noise scattered around the plane
# noise = np.random.uniform(low=0, high=10, size=(40, 2))
#
# # Combine everything
# data = np.vstack((sub1a, sub1b, sub2a, sub2b, sub3a, sub3b, noise))

# --- Cluster 1: Attackers
attackers = np.random.normal(
    loc=[85, 85, 88, 40, 70, 65],  # mean values for each skill
    scale=[5, 5, 4, 5, 5, 4],
    size=(300, 6)
)

# --- Cluster 2: Midfielders
midfielders = np.random.normal(
    loc=[70, 75, 75, 60, 82, 70],
    scale=[5, 4, 5, 5, 4, 4],
    size=(300, 6)
)

# --- Cluster 3: Defenders
defenders = np.random.normal(
    loc=[60, 50, 55, 85, 65, 80],
    scale=[4, 5, 5, 4, 5, 4],
    size=(300, 6)
)

# --- Cluster 4: Goalkeepers / Outliers (noise)
goalkeepers = np.random.normal(
    loc=[50, 30, 40, 70, 55, 85],
    scale=[6, 6, 6, 6, 6, 6],
    size=(100, 6)
)

# Combine all data
data = np.vstack((attackers, midfielders, defenders, goalkeepers))


clusters, _=DB_scan(data, e=10, minpts=10)
# print(clusters)
rad=0

final = 0
diff = 3

final_clusters=[
    [] for _ in range(len(clusters))
]


for i in range(len(clusters)):
    # print(get_data(data,clusters[i]))
    order,reachability=optics(get_data(data,clusters[i]),e=10, minpts=10)
    if len(order)==0: continue
    # print(order)
    rad=1
    cur=[clusters[i][order[0]]]
    # print(f"current{cur}")
    for j in range(len(order)):
        if(j==0): continue
        if reachability[j]-reachability[j-1]>diff:
            final_clusters[i].append(cur.copy())
            cur.clear()
            cur.append(clusters[i][order[j]])
            rad+=1
        else:
            cur.append(clusters[i][order[j]])

    final_clusters[i].append(cur.copy())
    cur.clear()

    final+=rad


print(f"final number of clusters is: {final}")

print(final_clusters)
# print(final_clusters[0])
# print(final_clusters[1])
