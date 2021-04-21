from typing import List, Tuple
from data import data
from training import tomotopy


def train(mdl, documents: List[data.Document], features, path, file_prefix='') \
        -> Tuple[List[dict], object, bool]:

    return tomotopy.train(mdl, documents, features, path, file_prefix)
