from algebra.monoid import MonoidController
from algebra.universe import Transformation

from algebra.utils import prepare_generating_set_from_description

build_gs = lambda *x: prepare_generating_set_from_description(
    *x, minimize=False)

FUNNY_SAMPLES_LIST: list[MonoidController] = [
    obj for name, obj in __import__(__name__).__dict__.items() if str.isupper(name)
]

FUNNY_LOOP_WITH_CENTER = build_gs(
    Transformation,
    *[(1, 1, 2, 5, 3), (4, 5, 4, 3, 3), (5, 1, 2, 4, 2), (3, 1, 2, 1, 5), (1, 3, 3, 5, 2)]
)



