import pytest
from app.scripts import intel_score


@pytest.fixture(scope="module")
def samples():
    y_pred = [
        "when he speaks he voices egisabe crant and quimus nus tramfl",
        "van polly like to be modern in his language",
        "night after night they receive a noin fron has",
        "how grag to pick a pack up tails",
        "he played basketball there while working towards a law degree",
    ]
    y_true = [
        "When he speaks, his voice is just a bit cracked and quivers a trifle.",
        "Grandfather likes to be modern in his language.",
        "Night after night, they received annoying phone calls.",
        "Help Greg to pick a peck of potatoes.",
        "He played basketball there while working toward a law degree.",
    ]
    return y_pred, y_true


def test_evaluate(samples):
    y_pred, y_true = samples
    assert (
        str(intel_score.evaluate(y_pred=y_pred, y_true=y_true))
        == "{'sequence_matcher': [0.6875, 0.8, 0.8484848484848485, 0.6956521739130435, 0.9836065573770492], " + \
        "'cer': [0.5333333333333333, 0.7441860465116279, 0.7173913043478262, 0.53125, 0.9508196721311475], " + \
        "'metaphone_match': [0.6428571428571428, 0.75, 0.7857142857142857, 0.7727272727272727, 0.972972972972973]}"
    )
