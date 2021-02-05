import neuralcoref
import en_core_web_sm

from abc import ABC, abstractmethod
from os import environ
from warnings import warn
from typing import Dict, List
from spacy.tokens import Doc


class IntersectionStrategy(ABC):

    def __init__(self, allen_model, hugging_model):
        self.allen_clusters = []
        self.hugging_clusters = []
        self.allen_model = allen_model
        self.hugging_model = hugging_model
        self.document = []
        self.doc = None

    @abstractmethod
    def get_intersected_clusters(self):
        raise NotImplementedError

    @staticmethod
    def get_span_noun_indices(doc: Doc, cluster: List[List[int]]):
        spans = [doc[span[0]:span[1]+1] for span in cluster]
        spans_pos = [[token.pos_ for token in span] for span in spans]
        span_noun_indices = [i for i, span_pos in enumerate(spans_pos)
            if any(pos in span_pos for pos in ['NOUN', 'PROPN'])]
        return span_noun_indices

    @staticmethod
    def get_cluster_head(doc: Doc, cluster: List[List[int]], noun_indices: List[int]):
        head_idx = noun_indices[0]
        head_start, head_end = cluster[head_idx]
        head_span = doc[head_start:head_end+1]
        return head_span, [head_start, head_end]

    @staticmethod
    def is_containing_other_spans(span: List[int], all_spans: List[List[int]]):
        return any([s[0] >= span[0] and s[1] <= span[1] and s != span for s in all_spans])

    def coref_resolved_improved(self, doc: Doc, clusters: List[List[List[int]]]):
        resolved = [tok.text_with_ws for tok in doc]
        all_spans = [span for cluster in clusters for span in cluster]  # flattened list of all spans

        for cluster in clusters:
            noun_indices = self.get_span_noun_indices(doc, cluster)
            if noun_indices:
                mention_span, mention = self.get_cluster_head(doc, cluster, noun_indices)

                for coref in cluster:
                    if coref != mention and not self.is_containing_other_spans(coref, all_spans):
                        final_token = doc[coref[1]]
                        if final_token.tag_ in ["PRP$", "POS"]:
                            resolved[coref[0]] = mention_span.text + "'s" + final_token.whitespace_
                        else:
                            resolved[coref[0]] = mention_span.text + final_token.whitespace_

                        for i in range(coref[0] + 1, coref[1] + 1):
                            resolved[i] = ""

        return "".join(resolved)

    def clusters(self, text):
        self.acquire_models_clusters(text)
        return self.get_intersected_clusters()

    def resolve_coreferences(self, text: str):
        clusters = self.clusters(text)
        resolved_text = self.coref_resolved_improved(self.doc, clusters)
        return resolved_text

    def acquire_models_clusters(self, text: str):
        allen_prediction = self.allen_model.predict(text)
        self.allen_clusters = allen_prediction['clusters']
        self.document = allen_prediction['document']
        self.doc = self.hugging_model(text)
        hugging_clusters = self._transform_huggingface_answer_to_allen_list_of_clusters()
        self.hugging_clusters = hugging_clusters

    def _transform_huggingface_answer_to_allen_list_of_clusters(self):
        list_of_clusters = []
        for cluster in self.doc._.coref_clusters:
            list_of_clusters.append([])
            for span in cluster:
                list_of_clusters[-1].append([span[0].i, span[-1].i])
        return list_of_clusters
