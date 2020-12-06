from brute_force_mkp import brute_force_mkp
from mkp_mst import mkp_mst
from mkp_mst_ratio import mkp_mst_ratio
from mkp_mst_ratio_dist import mkp_mst_ratio_dist
from delivery import Delivery

from time import perf_counter
from pprint import pprint

algorithms = [
    brute_force_mkp,
    mkp_mst,
    mkp_mst_ratio,
    mkp_mst_ratio_dist
]


def results_init():
    return {
        algo.__name__: {'time': 0, 'profit': 0} for algo in algorithms
    }


def compare_mkp_solutions():
    print("Comparing up to brute force limits (n=8)")
    results = results_init()
    for i in range(10):
        deliveries = Delivery.generate(8)
        weight_limit = 250
        for algo in algorithms:
            t0 = perf_counter()
            path = algo(D=deliveries, W=weight_limit)
            results[algo.__name__]['time'] += perf_counter() - t0
            results[algo.__name__]['profit'] += path.profit
        print(f"Round {i+1}/10")
    pprint(results, width=50)

    print('Compared to brute force:')
    bf_res = results[algorithms[0].__name__]
    for algo in algorithms[1:]:
        n = algo.__name__
        print(f"{n}: "
              f"{results[n]['profit'] / bf_res['profit']:.1%} profit, "
              f"{bf_res['time'] / results[n]['time']:.0f}x faster")

    del algorithms[0]

    print("\nComparing up to combinatorial mst limits (n=16)")
    results = results_init()
    for i in range(10):
        deliveries = Delivery.generate(16)
        weight_limit = 250
        for algo in algorithms:
            t0 = perf_counter()
            path = algo(D=deliveries, W=weight_limit)
            results[algo.__name__]['time'] += perf_counter() - t0
            results[algo.__name__]['profit'] += path.profit
        print(f"Round {i+1}/10")
    pprint(results, width=50)

    print('Compared to combinatorial mst:')
    cmst_res = results[algorithms[0].__name__]
    for algo in algorithms[1:]:
        n = algo.__name__
        print(f"{n}: "
              f"{results[n]['profit'] / cmst_res['profit']:.1%} profit, "
              f"{cmst_res['time'] / results[n]['time']:.0f}x faster")

    del algorithms[0]

    print("\nComparing the two fast approximation algorithms (n=200)")
    results = results_init()
    for i in range(10):
        deliveries = Delivery.generate(250)
        weight_limit = 2000
        for algo in algorithms:
            t0 = perf_counter()
            path = algo(D=deliveries, W=weight_limit)
            results[algo.__name__]['time'] += perf_counter() - t0
            results[algo.__name__]['profit'] += path.profit
        print(f"Round {i+1}/10")
    pprint(results, width=50)

    print('Comparing:')
    for index in (0, 1):
        n1 = algorithms[index].__name__
        n2 = algorithms[not index].__name__
        print(f"{n1}: "
              f"{results[n1]['profit'] / results[n2]['profit']:.1%} profit, "
              f"{results[n2]['time'] / results[n1]['time']:.2f}x faster")


if __name__ == '__main__':
    compare_mkp_solutions()
