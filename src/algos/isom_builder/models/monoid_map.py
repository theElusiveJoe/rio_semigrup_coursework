from algebra.universe import Universe
from algebra.monoid import MonoidController
from algebra.graph import Hclass, Node


class MonoidMap:
    S1: MonoidController
    S2: MonoidController

    all_map: dict[Node, Node]

    def __init__(self, initObjects:tuple[MonoidController, MonoidController]|None=None) -> None:
        if initObjects is None:
            return
        
        self.S1, self.S2 = initObjects
        self.all_map = dict()

    def is_gen_set_done(self):
        # TODO: add gen_set_map
        return all(map(lambda x: x in self.all_map.keys(), self.S1.generators))
    
    def map_set(self, a: Node, b: Node):
        self.all_map[a] = b

    def map_get(self, a: Node):
        return self.all_map.get(a)

    def __getitem__(self, key: Node):
        return self.all_map[key]
    
    def make_copy(self):
        newMap = MonoidMap()
        newMap.S1 = self.S1
        newMap.S2 = self.S2
        newMap.all_map = self.all_map.copy()
        return newMap