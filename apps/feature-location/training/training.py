from typing import List, Tuple
from data import data
from training import tomotopy


def train(mdl, documents: List[data.Document], features, path, file_prefix='', iterations=100, burn_in=10) \
        -> Tuple[List[dict], object, bool]:

    return tomotopy.train(mdl, documents, features, path, file_prefix, iterations, burn_in)
