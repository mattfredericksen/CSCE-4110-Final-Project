from itertools import combinations, permutations
from functools import lru_cache
from random import randint, uniform

import matplotlib.pyplot as plt


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

    def __add__(self, other):
        """Warning: this algorithm is flawed.
        A TSP solution cannot be iteratively developed. A new "city"
        can invalidate the entire previous solution.
        """
        if not isinstance(other, Delivery):
            raise NotImplementedError(f'{other} is not a Delivery')
        new_path = DeliveryPath([other] + self.path)
        deliveries = new_path.path
        shortest_insertion_point = 0
        # shortest = new_path.length
        for i in range(0, len(self.path)):
            deliveries[i], deliveries[i+1] = deliveries[i+1], deliveries[i]
            # if new_path.length <= shortest:
            #     shortest_insertion_point = i + 1
        deliveries.insert(shortest_insertion_point, other)
        deliveries.pop()
        return new_path

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


if __name__ == '__main__':
    W = 250
    D = []
    for _ in range(11):
        item = Item(randint(10, 200), randint(1, 100))
        address = Address(uniform(0, 1), uniform(0, 1))
        D.append(Delivery(item, address))

    best_path = DeliveryPath()

    for count in range(1, len(D)):
        for haul in combinations(D, count):
            shortest_path = DeliveryPath(haul)

            if shortest_path.weight > W:
                continue

            for path in map(DeliveryPath, permutations(haul)):
                if path.length < shortest_path.length:
                    shortest_path = path

            if shortest_path.profit > best_path.profit:
                best_path = shortest_path

    print(f"best profit: ${best_path.profit:.2f}")
    print(f"capacity used: {best_path.weight / W :.1%}")
    print("best path:")
    for d in best_path:
        print(f'\t{d}')
    plot_path(D, best_path)
