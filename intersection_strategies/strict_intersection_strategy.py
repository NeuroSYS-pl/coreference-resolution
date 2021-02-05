from .intersection_strategy import IntersectionStrategy


class StrictIntersectionStrategy(IntersectionStrategy):

    def get_intersected_clusters(self):
        intersected_clusters = []
        for allen_cluster in self.allen_clusters:
            for hugging_cluster in self.hugging_clusters:
                if allen_cluster == hugging_cluster:
                    intersected_clusters.append(allen_cluster)
        return intersected_clusters
