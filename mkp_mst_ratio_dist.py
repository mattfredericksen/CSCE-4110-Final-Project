from heapq import heappush, heappop
from delivery import Delivery, DeliveryPath


def main(deliveries):
    # maximum weight capacity
    W = 2000
    D = deliveries

    # heuristic: sort deliveries by their item's value-to-weight ratio
    D.sort(reverse=True)

    w = 0
    heap = []
    total_distance = {}
    best_approx = DeliveryPath()

    # This part seems to improve over just taking the
    # delivery items with the highest value/weight ratio.
    # Its effectiveness likely depends on how dense the
    # delivery graph is.
    for d in D:
        heappush(heap, d)

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
            d = heappop(heap)
            for delivery in total_distance:
                total_distance[delivery] -= d.item.weight
            del total_distance[d]
            new_w -= d.item.weight
        w = new_w

        furthest = sorted(total_distance, key=lambda k: total_distance[k])
        approx = DeliveryPath(furthest)

        # Check if dropping the "furthest" delivery improves profits.
        # After testing the algorithm with and without this heuristic,
        # the results are often the same, but this one sometimes
        # performs better
        while furthest:
            furthest.pop()
            shorter_approx = DeliveryPath(furthest)
            if shorter_approx > approx:
                approx = shorter_approx
            else:
                break

        if approx > best_approx:
            best_approx = approx

    print(f"best profit: ${best_approx.profit:.2f}")
    print(f"capacity used: {best_approx.weight / W :.1%}")
    best_approx.plot(all_deliveries=D)


if __name__ == '__main__':
    main(Delivery.generate(200))
