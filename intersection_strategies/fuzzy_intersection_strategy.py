from copy import deepcopy
from .partial_intersection_strategy import PartialIntersectionStrategy


class FuzzyIntersectionStrategy(PartialIntersectionStrategy):
    """ Is treated as a PartialIntersectionStrategy, yet first must map AllenNLP spans and Huggingface spans. """

    @staticmethod
    def flatten_cluster(list_of_clusters):
        return [span for cluster in list_of_clusters for span in cluster]

    def _check_whether_spans_are_within_range(self, allen_span, hugging_span):
        allen_range = range(allen_span[0], allen_span[1]+1)
        hugging_range = range(hugging_span[0], hugging_span[1]+1)
        allen_within = allen_span[0] in hugging_range and allen_span[1] in hugging_range
        hugging_within = hugging_span[0] in allen_range and hugging_span[1] in allen_range
        return allen_within or hugging_within

    def _add_span_to_list_dict(self, allen_span, hugging_span):
        if (allen_span[1]-allen_span[0] > hugging_span[1]-hugging_span[0]):
            self._add_element(allen_span, hugging_span)
        else:
            self._add_element(hugging_span, allen_span)

    def _add_element(self, key_span, val_span):
        if tuple(key_span) in self.swap_dict_list.keys():
            self.swap_dict_list[tuple(key_span)].append(tuple(val_span))
        else:
            self.swap_dict_list[tuple(key_span)] = [tuple(val_span)]

    def _filter_out_swap_dict(self):
        swap_dict = {}
        for key, vals in self.swap_dict_list.items():
            if self.swap_dict_list[key] != vals[0]:
                swap_dict[key] = sorted(vals, key=lambda x: x[1]-x[0], reverse=True)[0]
        return swap_dict

    def _swap_mapped_spans(self, list_of_clusters, model_dict):
        for cluster_idx, cluster in enumerate(list_of_clusters):
            for span_idx, span in enumerate(cluster):
                if tuple(span) in model_dict.keys():
                    list_of_clusters[cluster_idx][span_idx] = list(model_dict[tuple(span)])
        return list_of_clusters

    def get_mapped_spans_in_lists_of_clusters(self):
        self.swap_dict_list = {}
        for allen_span in self.flatten_cluster(self.allen_clusters):
            for hugging_span in self.flatten_cluster(self.hugging_clusters):
                if self._check_whether_spans_are_within_range(allen_span, hugging_span):
                    self._add_span_to_list_dict(allen_span, hugging_span)
        swap_dict = self._filter_out_swap_dict()

        allen_clusters_mapped = self._swap_mapped_spans(deepcopy(self.allen_clusters), swap_dict)
        hugging_clusters_mapped = self._swap_mapped_spans(deepcopy(self.hugging_clusters), swap_dict)
        return allen_clusters_mapped, hugging_clusters_mapped

    def get_intersected_clusters(self):
        allen_clusters_mapped, hugging_clusters_mapped = self.get_mapped_spans_in_lists_of_clusters()
        self.allen_clusters = allen_clusters_mapped
        self.hugging_clusters = hugging_clusters_mapped
        return super().get_intersected_clusters()
