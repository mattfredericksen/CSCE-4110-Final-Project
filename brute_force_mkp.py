from itertools import combinations, permutations
from delivery import DeliveryPath, Delivery


def brute_force_mkp(D, W):
    best_path = DeliveryPath()

    for count in range(1, len(D)):
        for haul in combinations(D, count):
            shortest_path = DeliveryPath(haul, make_mst=False)

            if shortest_path.weight > W:
                continue

            for path in permutations(haul):
                path = DeliveryPath(haul, make_mst=False)
                if path.length < shortest_path.length:
                    shortest_path = path

            if shortest_path > best_path:
                best_path = shortest_path

    return best_path


if __name__ == '__main__':
    deliveries = Delivery.generate(200)
    weight_limit = 250
    path = brute_force_mkp(D=deliveries, W=weight_limit)
    path.plot(all_deliveries=deliveries)
    print(f"best profit: ${path.profit:.2f}")
    print(f"capacity used: {path.weight / weight_limit:.1%}")
