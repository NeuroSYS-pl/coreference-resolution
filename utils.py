import spacy
import neuralcoref
from allennlp.predictors.predictor import Predictor

from intersection_strategies.intersection_strategy import IntersectionStrategy
from intersection_strategies.strict_intersection_strategy import StrictIntersectionStrategy
from intersection_strategies.partial_intersection_strategy import PartialIntersectionStrategy
from intersection_strategies.fuzzy_intersection_strategy import FuzzyIntersectionStrategy


def load_models():
    allen_url = 'https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2020.02.27.tar.gz'
    predictor = Predictor.from_path(allen_url)
    nlp = spacy.load('en_core_web_sm')
    neuralcoref.add_to_pipe(nlp)
    return predictor, nlp


def get_cluster_head_idx(doc, cluster):
    noun_indices = IntersectionStrategy.get_span_noun_indices(doc, cluster)
    return noun_indices[0] if noun_indices else 0


def print_clusters(doc, clusters):
    def get_span_words(span, allen_document):
        return ' '.join(allen_document[span[0]:span[1]+1])

    allen_document, clusters = [t.text for t in doc], clusters
    for cluster in clusters:
        cluster_head_idx = get_cluster_head_idx(doc, cluster)
        if cluster_head_idx >= 0:
            cluster_head = cluster[cluster_head_idx]
            print(get_span_words(cluster_head, allen_document) + ' - ', end='')
            print('[', end='')
            for i, span in enumerate(cluster):
                print(get_span_words(span, allen_document) + ("; " if i+1 < len(cluster) else ""), end='')
            print(']')


def print_comparison(resolved_original_text, resolved_improved_text):
    print(f"~~~ AllenNLP original replace_corefs ~~~\n{resolved_original_text}")
    print(f"\n~~~ Our improved replace_corefs ~~~\n{resolved_improved_text}")
