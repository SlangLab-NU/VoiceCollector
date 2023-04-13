"""
This script contains implementations of several intelligibility scoring functions. The score is a float within the range [0, 1]. 
A higher score indicates better intelligibility. 

Some readings:
- String metric From Wikipedia (https://en.wikipedia.org/wiki/String_metric#:~:text=In%20mathematics%20and%20computer%20science)
- Soundex and Levenshtein distance in Python (https://medium.com/@yash_agarwal2/soundex-and-levenshtein-distance-in-python-8b4b56542e9e#:~:text=What%20is%20Levenshtein%20distance%3F)
- Phonetics based Fuzzy string matching algorithms (https://medium.com/data-science-in-your-pocket/phonetics-based-fuzzy-string-matching-algorithms-8399aea04718)
- Fuzzy String Matching Algorithms (https://towardsdatascience.com/fuzzy-string-matching-algorithms-e0d483c2a9ea#:~:text=Phonetic%20matching%20algorithms%20match%20strings)

https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher

"""
import re
from typing import Union, Sequence
from difflib import SequenceMatcher
import jiwer
from metaphone import doublemetaphone


def evaluate(y_pred: Union[Sequence[str], str], y_true: Union[Sequence[str], str]):
    if type(y_pred) != type(y_true):
        raise TypeError("y_pred and y_true should have same types.")
    elif isinstance(y_pred, str) and isinstance(y_true, str):
        return {
            "sequence_matcher": sequence_matcher(y_pred, y_true),
            "cer": cer(y_pred, y_true),
            "metaphone_match": metaphone_match(y_pred, y_true) 
        }
    elif isinstance(y_pred, Sequence) and isinstance(y_true, Sequence):
        assert len(y_pred) == len(y_true)
        return {
            "sequence_matcher": [sequence_matcher(pred, label) for (pred, label) in zip(y_pred, y_true)],
            "cer": [cer(pred, label) for (pred, label) in zip(y_pred, y_true)],
            "metaphone_match": [metaphone_match(pred, label) for (pred, label) in zip(y_pred, y_true)]
        }
    else:
        raise TypeError("Error type for either y_pred or y_true.")


def normalize(s: str):
    """
    Remove all non-letter characters
    """
    return re.sub("[^a-zA-Z]+", " ", s.lower())


def sequence_matcher(y_pred, y_true):
    """
    Sequence matcher
    https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher
    """
    y_pred, y_true = normalize(y_pred), normalize(y_true)
    s = SequenceMatcher(None, y_pred, y_true)
    return s.ratio()


def cer(y_pred, y_true):
    """
    Character error rate (CER)

    https://torchmetrics.readthedocs.io/en/stable/text/char_error_rate.html#char-error-rate
    https://github.com/jitsi/jiwer#usage
    """
    cer_score = jiwer.cer(y_pred, y_true)
    # Trim the score to [0, 1] since cer score can be greater than 1
    cer_score = min(cer_score, 1)
    return 1 - cer_score


def metaphone_match(y_pred, y_true):
    """
    Metapphone-CER
    https://github.com/oubiwann/metaphone
    """
    y_pred, y_true = normalize(y_pred), normalize(y_true)
    y_pred_meta = " ".join([doublemetaphone(x)[0] for x in y_pred.split()])
    y_true_meta = " ".join([doublemetaphone(x)[0] for x in y_true.split()])

    cer_score = jiwer.cer(y_pred_meta, y_true_meta)
    cer_score = min(cer_score, 1)
    return 1 - cer_score
