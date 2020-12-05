from itertools import combinations, permutations
from functools import lru_cache
from collections import defaultdict
from heapq import heapify, heappush, heappop

from random import randint, uniform
from math import log10
from time import time

import matplotlib.pyplot as plt


def create_mst_path(deliveries):
    """Returns a path through the MST formed from `deliveries`.
    Adapted from:
    https://bradfieldcs.com/algos/graphs/prims-spanning-tree-algorithm/
    """
    graph = defaultdict(dict)

    # using a simple heuristic here such as picking the left-most
    # vertex as a starting point yields less than 1% average performance
    # increase with dense input, but it's fast so why not?
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
    heapify(edges)

    travel_order = []
    while edges:
        cost, frm, to = heappop(edges)
        if to not in visited:
            visited.add(to)
            travel_order.append(to)
            for to_next, cost in graph[to].items():
                if to_next not in visited:
                    heappush(edges, (cost, to, to_next))
    return travel_order


class Item:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight
        self.ratio = value / weight

    def __lt__(self, other):
        return self.ratio < other.ratio

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value}, weight={self.weight})"


class Address:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
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

    def __lt__(self, other):
        return self.item < other.item

    def __repr__(self):
        return f"{self.__class__.__name__}({self.item}, {self.address})"


class DeliveryPath:
    def __init__(self, deliveries=()):
        if len(deliveries) > 2:
            self.path = create_mst_path(deliveries)
        else:
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

    def __lt__(self, other):
        return (self.profit, -self.weight) < (other.profit, -other.weight)


def plot_path(deliveries, path, label=False):
    min_x, min_y, max_x, max_y = (*[float('inf')]*2, *[float('-inf')]*2)
    for d in deliveries:
        x, y = d.address
        plt.plot(x, y, 'ro')
        if label:
            plt.annotate(repr(d.item), (x, y))
        min_x, min_y, max_x, max_y = min(x, min_x), min(y, min_y), max(x, max_x), max(y, max_y)

    plt.xlim(min_x - max_x*0.1, max_x * 1.1)
    plt.ylim(min_y - max_y*0.1, max_y * 1.1)
    for i in range(len(path) - 1):
        a1, a2 = (d.address for d in path[i:i+2])
        plt.annotate("", xy=(*a2,), xytext=(*a1,), arrowprops=dict(arrowstyle="->"))
        # plt.arrow(a1.x, a1.y, *(a2 - a1), head_width=0.5, length_includes_head=True)
    plt.show()


def generate_deliveries(n):
    return [
        Delivery(
            Item(value=randint(5, 200), weight=randint(1, 50)),
            Address(x=uniform(0, log10(n)), y=uniform(0, log10(n)))
        ) for _ in range(n)
    ]


def main(deliveries):
    W = 2000
    D = deliveries
    D.sort(reverse=True)

    w = 0
    heap = []
    best_approx = DeliveryPath()

    # This part doesn't actually improve things much.
    # We might do better by dropping the delivery which
    # is the furthest from all other deliveries, until
    # the result is less profitable than retaining the
    # furthest delivery.
    for d in D:
        heappush(heap, d)
        new_w = w + d.item.weight
        while new_w > W:
            new_w -= heappop(heap).item.weight

        w = new_w

        approx = DeliveryPath(heap)
        if approx > best_approx:
            best_approx = approx

    print(f"best profit: ${best_approx.profit:.2f}")
    print(f"capacity used: {best_approx.weight / W :.1%}")
    plot_path(D, best_approx)


if __name__ == '__main__':
    main(generate_deliveries(200))
