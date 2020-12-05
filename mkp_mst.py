from itertools import combinations, permutations
from functools import lru_cache
from collections import defaultdict
import heapq
from random import randint, uniform

import matplotlib.pyplot as plt


def create_spanning_tree(deliveries):
    graph = defaultdict(dict)
    # does this actually help?
    starting_vertex = min(deliveries, key=lambda d: d.address.x)
    for i, d1 in enumerate(deliveries):
        for j in range(i+1, len(deliveries)):
            d2 = deliveries[j]
            graph[d1][d2] = d1.address.distance_to(d2.address)
            graph[d2][d1] = graph[d1][d2]

    visited = {starting_vertex}
    edges = [
        (cost, starting_vertex, to)
        for to, cost in graph[starting_vertex].items()
    ]
    heapq.heapify(edges)

    travel_order = []
    while edges:
        cost, frm, to = heapq.heappop(edges)
        if to not in visited:
            visited.add(to)
            travel_order.append(to)
            for to_next, cost in graph[to].items():
                if to_next not in visited:
                    heapq.heappush(edges, (cost, to, to_next))
    return travel_order


class Item:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value}, weight={self.weight})"


class Address:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError(f'{other} is not an {self.__class__.__name__}')
        return (self.x - other.x), (self.y - other.y)

    @lru_cache(maxsize=None)
    def distance_to(self, other):
        return sum(coord**2 for coord in (self - other)) ** 0.5

    def __iter__(self):
        return iter((self.x, self.y))

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x:.3}, y={self.y:.3})"


class Delivery:
    def __init__(self, item, address):
        self.item = item
        self.address = address

    def __repr__(self):
        return f"{self.__class__.__name__}({self.item}, {self.address})"


class DeliveryPath:
    def __init__(self, deliveries=()):
        self.path = deliveries

    @property
    @lru_cache(maxsize=1)
    def length(self):
        return sum(self.path[i].address.distance_to(self.path[i+1].address)
                   for i in range(len(self.path) - 1))

    @property
    @lru_cache(maxsize=1)
    def profit(self):
        return sum(d.item.value/100 for d in self.path) - 2 * self.length

    @property
    @lru_cache(maxsize=1)
    def weight(self):
        return sum(d.item.weight for d in self.path)

    def __iter__(self):
        return iter(self.path)

    def __getitem__(self, item):
        return self.path[item]

    def __len__(self):
        return len(self.path)

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplementedError(f'{other} is not an {self.__class__.__name__}')
        return (self.profit, -self.weight) > (other.profit, -other.weight)


def plot_path(deliveries, path):
    min_x, min_y, max_x, max_y = (*[float('inf')]*2, *[float('-inf')]*2)
    for d in deliveries:
        x, y = d.address
        plt.plot(x, y, 'ro')
        plt.annotate(repr(d.item), (x, y))
        min_x, min_y, max_x, max_y = min(x, min_x), min(y, min_y), max(x, max_x), max(y, max_y)

    plt.xlim(min_x - max_x*0.1, max_x * 1.1)
    plt.ylim(min_y - max_y*0.1, max_y * 1.1)
    for i in range(len(path) - 1):
        a1, a2 = (d.address for d in path[i:i+2])
        plt.annotate("", xy=(*a2,), xytext=(*a1,), arrowprops=dict(arrowstyle="->"))
        # plt.arrow(a1.x, a1.y, *(a2 - a1), head_width=0.5, length_includes_head=True)
    plt.show()


from time import time
def main(n):
    W = 250
    D = []
    for _ in range(n):
        item = Item(randint(10, 200), randint(1, 100))
        address = Address(uniform(0, 1), uniform(0, 1))
        D.append(Delivery(item, address))

    best_approx = DeliveryPath()

    for count in range(1, len(D)):
        continue_ = False
        for haul in combinations(D, count):
            shortest_path = DeliveryPath(haul)

            if shortest_path.weight > W:
                continue
            continue_ = True

            approx = DeliveryPath(create_spanning_tree(haul))
            if approx.profit > best_approx.profit:
                best_approx = approx
        if not continue_:
            break

    print(f"best profit: ${best_approx.profit:.2f}")
    print(f"capacity used: {best_approx.weight / W :.1%}")
    plot_path(D, best_approx)


if __name__ == '__main__':
    for i in range(10, 20):
        t0 = time()
        main(i)
        print(f"{i:02}: {time()-t0:.2f}")
