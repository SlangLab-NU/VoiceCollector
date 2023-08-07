import intel_score
from ..log import logger

logger = logger.load_log()

y_pred = ["when he speaks he voices egisabe crant and quimus nus tramfl", "van polly like to be modern in his language"]
y_true = ["When he speaks, his voice is just a bit cracked and quivers a trifle.", "Grandfather likes to be modern in his language."]

logger.info(f"{intel_score.evaluate(y_pred, y_true)}")
