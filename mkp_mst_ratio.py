from heapq import heappush, heappop
from delivery import DeliveryPath, Delivery


def mkp_mst_ratio(D, W):
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

    return best_approx


if __name__ == '__main__':
    deliveries = Delivery.generate(200)
    weight_limit = 2000
    path = mkp_mst_ratio(D=deliveries, W=weight_limit)
    path.plot(all_deliveries=deliveries)
    print(f"best profit: ${path.profit:.2f}")
    print(f"capacity used: {path.weight / weight_limit:.1%}")
