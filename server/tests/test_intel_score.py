import pytest
from app.scripts import intel_score


@pytest.fixture(scope='module')
def samples():
    y_pred = ["when he speaks he voices egisabe crant and quimus nus tramfl", "van polly like to be modern in his language"]
    y_true = ["When he speaks, his voice is just a bit cracked and quivers a trifle.", "Grandfather likes to be modern in his language."]
    return y_pred, y_true

def test_evaluate(samples):
    y_pred, y_true = samples
    assert str(intel_score.evaluate(y_pred=y_pred, y_true=y_true)) == "{'sequence_matcher_diff': [0.3125, 0.19999999999999996], 'cer': [0.4666666666666667, 0.2558139534883721], 'metaphone_match': [0.35714285714285715, 0.25]}"
