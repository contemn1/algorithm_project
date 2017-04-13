import heapq
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances


class ClusterPair(object):
    def __init__(self, cluster1_id, cluster2_id, distance, size1, size2):
        self.cluster1 = cluster1_id
        self.cluster2 = cluster2_id
        self.distance = distance
        self.initial_size1 = size1
        self.initial_size2 = size2


class Node(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.left_instance = None
        self.right_instance = None
        self.left_length = 0
        self.right_length = 0
        self.height = 0
    
    def set_height(self, left_height, right_height):
        self.height = left_height
        self.left_length = left_height
        if self.left:
            self.left_length -= self.left.height
        self.right_length = right_height
        if self.right:
            self.right_length -= self.right.height

    def set_length(self, left_length, right_length):
        self.left_length = left_length
        self.right_length = right_length
        self.height = left_length
        if self.left:
            self.height += self.left.height


class MyHeap(object):
    def __init__(self, initial=None, key=lambda x:x):
        self.key = key
        if initial:
            self._data = [(key(item), item) for item in initial]
            heapq.heapify(self._data)
        else:
            self._data = []

    def push(self, item):
        heapq.heappush(self._data, (self.key(item), item))

    def pop(self):
        return heapq.heappop(self._data)[1]


class HierarchicalClusterer(object):
    def __init__(self, distance_matrix, linkage_function, minium_clusters=2):
        self.distance_matrix = distance_matrix
        self.linkage_function = linkage_function
        self.minium_clusters = minium_clusters

    def build_clusters(self):
        print 'a'

    def do_link_clustering(self, cluster_id_list, cluster_nodes):

        def small_big(first, second):
            return (first, second) if first < second else (second, first)

        def merge(cluster1, cluster2, distance, cluster_ids, cluster_nodes):
            cluster1, cluster2 = small_big(cluster1, cluster2)
            cluster_ids[cluster1].extend(cluster_ids[cluster2])
            cluster_ids[cluster2] = []
            node = Node()

            if cluster_nodes[cluster1]:
                node.left = cluster_nodes[cluster1]
                cluster_nodes[cluster1].parent = node
            else:
                node.left_instance = cluster1

            if cluster_nodes[cluster2]:
                node.right = cluster_nodes[cluster2]
                cluster_nodes[cluster2].parent = node
            else:
                node.right_instance = cluster2

            node.set_height(distance, distance)
            cluster_nodes[cluster1] = node

        length = self.distance_matrix.shape[0]
        cluster_number = self.distance_matrix.shape[0]
        distance_list = [ClusterPair(first, second, self.distance_matrix[first][second], 1, 1)
                         for first in range(length) for second in range(first + 1, length)]

        distance_queue = MyHeap(initial=distance_list, key=lambda x: x.distance)

        while cluster_number - self.minium_clusters > 0:
            pair = distance_queue.pop()
            if not pair:
                break

            if not valid_pair(pair, cluster_id_list):
                continue

            merge(pair.cluster1, pair.cluster2, pair.distance, cluster_id_list, cluster_nodes)

            for index in range(length):
                if index != pair.cluster1 and cluster_id_list[index]:
                    smaller, bigger = small_big(pair.cluster1, index)

                    new_distance = self.linkage_function(
                        self.distance_matrix,
                        cluster_id_list[smaller],
                        cluster_id_list[bigger])

                    distance_queue.push(ClusterPair(smaller,
                                                    bigger,
                                                    new_distance,
                                                    len(cluster_id_list[smaller]),
                                                    len(cluster_id_list[bigger])))
            cluster_number -= 1


def valid_pair(pair, cluster_id_list):
    return pair.initial_size1 == len(cluster_id_list[pair.cluster1]) and \
           pair.initial_size2 == len(cluster_id_list[pair.cluster2])


def single_linkage(distance_matrix, cluster_list1, cluster_list2):
    distances = [distance_matrix[i][j] for i in cluster_list1 for j in cluster_list2]
    return min(distances)


def simple_test():
    a = np.random.multivariate_normal([10, 0], [[3, 1], [1, 4]], size=[100, ])
    b = np.random.multivariate_normal([0, 20], [[3, 1], [1, 4]], size=[50, ])
    X = np.concatenate((a, b), )
    X_new = pairwise_distances(X, n_jobs=4)
    id_list = [[x] for x in range(X_new.shape[0])]
    clusterer = HierarchicalClusterer(
        distance_matrix=X_new,
        linkage_function=single_linkage,
        minium_clusters=5)
    cluster_nodes = [None] * X_new.shape[0]
    clusterer.do_link_clustering(cluster_id_list=id_list, cluster_nodes=cluster_nodes)
    for ele in id_list:
        if ele:
            print ele

if __name__ == '__main__':
    simple_test()