from algebra.monoid import MonoidController
from algebra.universe import Transformation

from algebra.utils import prepare_generating_set_from_description

build_gs = lambda *x: prepare_generating_set_from_description(
    *x, minimize=False)

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

'''
что-то для отладки
'''

T3_SPIN = build_gs(
    Transformation,
    [2, 3, 1]
)


T3_SPIN_PLUS = build_gs(
    Transformation,
    [2, 3, 1],
    [3, 1, 2],
    [1, 1, 1],
    [2, 2, 2],
)


SIMPLE_SAMPLES_LIST: list[MonoidController] = [
    eval(name) for name in dir() if name.startswith("SIMPLE")
]
