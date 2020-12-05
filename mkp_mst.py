from itertools import combinations
from delivery import DeliveryPath, Delivery


def mkp_mst(D, W):
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

    return best_approx


if __name__ == '__main__':
    deliveries = Delivery.generate(20)
    weight_limit = 250
    path = mkp_mst(D=deliveries, W=weight_limit)
    path.plot(all_deliveries=deliveries)
    print(f"best profit: ${path.profit:.2f}")
    print(f"capacity used: {path.weight / weight_limit:.1%}")
