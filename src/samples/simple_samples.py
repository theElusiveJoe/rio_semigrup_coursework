from algebra.monoid import MonoidController
from algebra.universe import Transformation

from algebra.utils import prepare_generating_set_from_description as build_gs

SIMPLE_SAMPLES_LIST: list[MonoidController] = [
    obj for name, obj in __import__(__name__).__dict__.items() if str.isupper(name)
]


'''
пример из статьи
'''

T6_PAPER_SAMPLE = build_gs(
    Transformation,
    [2, 2, 4, 4, 5, 6],
    [5, 3, 4, 4, 6, 6],
)

'''
порождающие всю полугруппу трансформаций
'''

T4_ENTIRE = build_gs(
    Transformation,
    [1, 1, 3, 4],  # merge
    [2, 3, 4, 1],  # cyclew
    [2, 1, 3, 4],  # swap
)

T3_ENTIRE = build_gs(
    Transformation,
    [1, 1, 3],  # merge
    [2, 3, 1],  # cycle
    [2, 1, 3],  # swap
)


'''
порождающие всю группу перестановок
'''

T6_PERMUTATIONS = build_gs(
    Transformation,
    [2, 3, 4, 5, 6, 1],  # cycle
    [2, 1, 3, 4, 5, 6],  # swap
)


'''
ничего нового не порождается
'''

T6_TEO_ELEMS = build_gs(
    Transformation,
    [1, 1, 1, 1, 1, 1],
    [2, 2, 2, 2, 2, 2],
)

'''
главные идеалы
'''

T6_PRINCIPAL_IDEAL = build_gs(
    Transformation,
    [2, 3, 4, 5, 6, 1],
)