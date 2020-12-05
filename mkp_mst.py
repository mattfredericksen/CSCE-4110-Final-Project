from itertools import combinations
from delivery import DeliveryPath, Delivery


def main(deliveries):
    W = 250
    D = deliveries

    best_approx = DeliveryPath()

    for count in range(1, len(D)):
        continue_ = False
        for haul in combinations(D, count):
            shortest_path = DeliveryPath(haul)

            if shortest_path.weight > W:
                continue
            continue_ = True

            approx = DeliveryPath(haul)
            if approx > best_approx:
                best_approx = approx
        if not continue_:
            break

    print(f"best profit: ${best_approx.profit:.2f}")
    print(f"capacity used: {best_approx.weight / W :.1%}")
    best_approx.plot(all_deliveries=D)


if __name__ == '__main__':
    main(Delivery.generate(20))
