from . import testing, sql, python, apitesting, playwright, git, agile
from .cards import CARDS

LEVELS = ["easy", "medium", "advanced", "expert"]
TOPICS = [m.TOPIC for m in (testing, sql, python, apitesting, playwright, git, agile)]
BY_SLUG = {t["slug"]: t for t in TOPICS}
