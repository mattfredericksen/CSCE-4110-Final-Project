from heapq import heapify, heappush, heappop
from delivery import Delivery, DeliveryPath


def mkp_mst_ratio_dist(D, W):
    # heuristic: sort deliveries by their item's value-to-weight ratio
    D.sort(reverse=True)

    w = 0
    delivery_heap = []
    total_distance = {}
    best_approx = DeliveryPath()

    # This part seems to improve over just taking the
    # delivery items with the highest value/weight ratio.
    # Its effectiveness likely depends on how dense the
    # delivery graph is.
    for d in D:
        heappush(delivery_heap, d)

        # Heuristic: we keep track of the sum of distances
        # from each node to every other node. Then, we will
        # attempt to increase profits by dropping the
        # node with the greatest summed distance
        new_distance = 0
        for delivery in total_distance:
            dist = delivery.address.distance_to(d.address)
            total_distance[delivery] += dist
            new_distance += dist
        total_distance[d] = new_distance

        # while our weight exceeds the limit, drop the
        # delivery with the least value/weight ratio
        new_w = w + d.item.weight
        while new_w > W:
            d = heappop(delivery_heap)
            for delivery in total_distance:
                total_distance[delivery] -= delivery.address.distance_to(d.address)
            del total_distance[d]
            new_w -= d.item.weight
        w = new_w

        furthest = [(-v, k) for k, v in total_distance.items()]
        heapify(furthest)
        approx = DeliveryPath(delivery_heap)

        # Check if dropping the "furthest" delivery improves profits.
        # After testing the algorithm with and without this heuristic,
        # the results are often significantly worse using with this process.
        while len(furthest) > 10:
            _, removed_delivery = heappop(furthest)
            shorter_approx = DeliveryPath(delivery for _, delivery in furthest)
            if shorter_approx > approx:
                approx = shorter_approx
                for d in total_distance:
                    total_distance[d] -= d.address.distance_to(removed_delivery.address)
                del total_distance[d]
                delivery_heap = shorter_approx.path
            else:
                break
        heapify(delivery_heap)

        if approx > best_approx:
            best_approx = approx

    return best_approx


if __name__ == '__main__':
    deliveries = Delivery.generate(200)
    weight_limit = 2000
    path = mkp_mst_ratio_dist(D=deliveries, W=weight_limit)
    path.plot(all_deliveries=deliveries)
    print(f"best profit: ${path.profit:.2f}")
    print(f"capacity used: {path.weight / weight_limit:.1%}")
