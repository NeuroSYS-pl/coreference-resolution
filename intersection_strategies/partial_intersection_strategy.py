from .intersection_strategy import IntersectionStrategy


class PartialIntersectionStrategy(IntersectionStrategy):

    def get_intersected_clusters(self):
        intersected_clusters = []
        for allen_cluster in self.allen_clusters:
            intersected_cluster = []
            for hugging_cluster in self.hugging_clusters:
                allen_set = set(tuple([tuple(span) for span in allen_cluster]))
                hugging_set = set(tuple([tuple(span) for span in hugging_cluster]))
                intersect = sorted([list(el) for el in allen_set.intersection(hugging_set)])
                if len(intersect) > 1:
                    intersected_cluster += intersect
            if intersected_cluster:
                intersected_clusters.append(intersected_cluster)
        return intersected_clusters
