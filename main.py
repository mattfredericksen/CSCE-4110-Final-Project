from itertools import combinations, permutations
from delivery import DeliveryPath, Delivery


def main(deliveries):
    W = 250
    D = deliveries

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

    print(f"best profit: ${best_path.profit:.2f}")
    print(f"capacity used: {best_path.weight / W :.1%}")
    print("best path:")
    for d in best_path:
        print(f'\t{d}')
    best_path.plot(all_deliveries=D)


if __name__ == '__main__':
    main(Delivery.generate(10))
