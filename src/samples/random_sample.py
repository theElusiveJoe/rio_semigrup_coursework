import random
from algebra.monoid import MonoidController
from algebra.universe import Transformation
from algebra.utils import prepare_generating_set
from algebra.monoid.controller import EmptyGeneratorsSetException


def _random_transform(set_size: int):
    '''
    возвращает список длинны l с рандомными числами от a до b включительно
    '''
    return Transformation([random.randint(1, set_size)
                          for _ in range(set_size)])


def gen_random_sample(set_size: int, generators_num: int,
                      minimize=True) -> MonoidController:
    if set_size == 1:
        raise RuntimeError('а зачем тебе моноид из одного элемента? :)')
    if set_size < -0:
        raise RuntimeError('без комментариев...')
    while True:
        try:
            generators = [
                _random_transform(set_size)
                for _ in range(generators_num)
            ]
            S = prepare_generating_set(
                generators=generators, minimize=minimize)
        except EmptyGeneratorsSetException:
            continue
        else:
            return S
