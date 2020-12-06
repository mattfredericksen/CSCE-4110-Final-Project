from functools import lru_cache
from collections import defaultdict
from heapq import heapify, heappush, heappop

from random import randint, uniform
from math import log10

try:
    import matplotlib.pyplot as plt
except Exception as e:
    print(e)
    plt = None
    print("WARNING: matplotlib is not installed.")
    print("Graphs will not be displayed.")


class Item:
    """A class representing the item weight and value for a Delivery."""
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight
        self.ratio = value / weight

    def __lt__(self, other):
        """Comparisons are based on value/weight ratio"""
        return self.ratio < other.ratio

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value}, weight={self.weight})"


class Address:
    """A class representing the location of a Delivery."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return (self.x - other.x), (self.y - other.y)

    @lru_cache(maxsize=None)
    def distance_to(self, other):
        """Gets the Euclidean distance between two Addresses.
        The calculation is stored in an unlimited cache, so
        comparing n=1000 Addresses to each other will consume
        O(n^2)=1_000_000 space, which isn't very much."""
        return sum(coord**2 for coord in (self - other)) ** 0.5

    def __iter__(self):
        return iter((self.x, self.y))

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x:.3}, y={self.y:.3})"


class Delivery:
    """A class for combining an Item and Address into a Delivery."""
    def __init__(self, item, address):
        self.item = item
        self.address = address

    @staticmethod
    def generate(n):
        """Returns `n` randomly generated Deliveries."""
        # The bounds below are reasonable but arbitrary.
        return [
            Delivery(
                Item(value=randint(5, 200), weight=randint(1, 50)),
                Address(x=uniform(0, log10(n)), y=uniform(0, log10(n)))
            ) for _ in range(n)
        ]

    def __lt__(self, other):
        return self.item < other.item

    def __repr__(self):
        return f"{self.__class__.__name__}({self.item}, {self.address})"


class DeliveryPath:
    """This class is used to directly compare the profitability
    of two sets of deliveries. Its properties are cached, so
    their values will be stored after the initial calculation.
    The initial input is transformed into a path through an MST.
    """
    def __init__(self, deliveries=(), make_mst=True):
        self.path = tuple(deliveries)
        if len(self.path) > 2 and make_mst:
            self.create_mst_path()

    def __lt__(self, other):
        """Comparisons are based on profitability."""
        return (self.profit, -self.weight) < (other.profit, -other.weight)

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

    def create_mst_path(self):
        """Returns a path through the MST formed from `deliveries`.
        Adapted from:
        https://bradfieldcs.com/algos/graphs/prims-spanning-tree-algorithm/
        """
        graph = defaultdict(dict)

        # using a simple heuristic here such as picking the left-most
        # vertex as a starting point yields less than 1% average performance
        # increase with dense input, but it's fast so why not?
        starting_vertex = min(self.path, key=lambda d: d.address.x)

        for i, d1 in enumerate(self.path):
            for j in range(i + 1, len(self.path)):
                d2 = self.path[j]
                graph[d1][d2] = d1.address.distance_to(d2.address)
                graph[d2][d1] = graph[d1][d2]

        visited = {starting_vertex}
        edges = [
            (cost, starting_vertex, to)
            for to, cost in graph[starting_vertex].items()
        ]
        heapify(edges)

        self.path = []
        while edges:
            cost, frm, to = heappop(edges)
            if to not in visited:
                visited.add(to)
                self.path.append(to)
                for to_next, cost in graph[to].items():
                    if to_next not in visited:
                        heappush(edges, (cost, to, to_next))

    def plot(self, all_deliveries=(), label=False):
        """Helper function to visualize paths."""
        if not plt:
            return

        all_deliveries = all_deliveries or self.path

        min_x, min_y, max_x, max_y = (*[float('inf')] * 2, *[float('-inf')] * 2)
        for d in all_deliveries:
            x, y = d.address
            plt.plot(x, y, 'ro')
            if label:
                plt.annotate(repr(d.item), (x, y))
            min_x, min_y, max_x, max_y = min(x, min_x), min(y, min_y), max(x, max_x), max(y, max_y)

        plt.xlim(min_x - max_x * 0.1, max_x * 1.1)
        plt.ylim(min_y - max_y * 0.1, max_y * 1.1)
        for i in range(len(self.path) - 1):
            a1, a2 = (d.address for d in self.path[i:i + 2])
            plt.annotate("", xy=(*a2,), xytext=(*a1,), arrowprops=dict(arrowstyle="->"))
        plt.show()

    # def stats(self, all_deliveries, weight_limit):
    #     avg_ratio = sum(d.item.ratio for d in all_deliveries) / len(all_deliveries)
    #     avg_limited_value = avg_ratio * weight_limit
    #
    #     avg_random_distance = sum(
    #         d1.address.distance_to(d2.address) for d1 in all_deliveries for d2 in all_deliveries
    #     ) / (len(all_deliveries) - 1)
    #
    #     value_from_average_selection = (avg_limited_value * 0.01) - (avg_random_distance * 2)

    def __iter__(self):
        return iter(self.path)

    def __getitem__(self, item):
        return self.path[item]

    def __len__(self):
        return len(self.path)
