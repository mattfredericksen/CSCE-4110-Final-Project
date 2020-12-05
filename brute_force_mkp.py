from itertools import combinations, permutations
from delivery import DeliveryPath, Delivery


def brute_force_mkp(D, W):
    best_path = DeliveryPath()

    for count in range(len(D)):
        for haul in combinations(D, count + 1):
            new_path = DeliveryPath(haul, make_mst=False)

            if new_path.weight > W:
                continue

            for path in permutations(haul):
                path = DeliveryPath(path, make_mst=False)
                if path > new_path:
                    new_path = path

            if new_path.profit > best_path.profit:
                best_path = new_path

    return best_path


if __name__ == '__main__':
    deliveries = Delivery.generate(10)
    weight_limit = 250
    path = brute_force_mkp(D=deliveries, W=weight_limit)
    path.plot(all_deliveries=deliveries)
    print(f"best profit: ${path.profit:.2f}")
    print(f"capacity used: {path.weight / weight_limit:.1%}")
