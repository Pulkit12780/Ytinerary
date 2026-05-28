"""Cluster geocoded places by geography using scikit-learn k-means."""
from __future__ import annotations
import numpy as np
from sklearn.cluster import KMeans


def cluster_places(
    places: list[dict],
    num_days: int | None = None,
) -> dict[str, list]:
    """
    Groups places into at most `num_days` day clusters, capping each at 5 places.
    Overflow places go into a separate list.

    Returns {"clusters": list[list[dict]], "overflow": list[dict]}
    where clusters[i] is a list of places for day i+1.
    """
    n = len(places)
    if n == 0:
        return {"clusters": [], "overflow": []}

    k = num_days if num_days else min(5, max(1, (n + 4) // 5))
    k = min(k, n)

    if k == 1:
        return {"clusters": [places[:5]], "overflow": places[5:]}

    coords = np.array([[p["lat"], p["lng"]] for p in places], dtype=float)
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(coords)
    centroids = km.cluster_centers_

    buckets: dict[int, list] = {i: [] for i in range(k)}
    for place, label in zip(places, labels.tolist()):
        buckets[label].append(place)

    result_clusters: list[list[dict]] = []
    overflow: list[dict] = []

    for i in range(k):
        bucket = buckets[i]
        if len(bucket) <= 5:
            result_clusters.append(bucket)
        else:
            # Keep 5 closest to centroid; rest overflow
            cx, cy = centroids[i]
            ranked = sorted(
                bucket,
                key=lambda p: (p["lat"] - cx) ** 2 + (p["lng"] - cy) ** 2,
            )
            result_clusters.append(ranked[:5])
            overflow.extend(ranked[5:])

    return {"clusters": result_clusters, "overflow": overflow}
