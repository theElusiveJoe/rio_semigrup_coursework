from algebra.universe import Universe
from algebra.monoid import MonoidController
from algebra.graph import Node, Graph


class MonoidMap:
    S1: MonoidController
    G1: Graph

    all_map: dict[Node, Node]
    s1_unmatched_generatos: set[Node]

    def __init__(self, initObjects:tuple[MonoidController, Graph]|None=None) -> None:
        if initObjects is None:
            return
        
        self.S1, self.G1 = initObjects
        self.all_map = dict()
        self.s1_unmatched_generatos = set([self.G1.val2node[val] for val in self.S1.generators])

    def is_gen_set_done(self):
        # TODO: add gen_set_map
        return len(self.s1_unmatched_generatos) == 0
    
    def map_set(self, a: Node, b: Node):
        # remove from unmatched generator, if there
        try:
            self.s1_unmatched_generatos.remove(a)
        except KeyError:
            pass
        assert a not in self.all_map.keys()
        self.all_map[a] = b

    def map_get(self, a: Node):
        return self.all_map.get(a)

    def __getitem__(self, key: Node):
        return self.all_map[key]
    
    def make_copy(self):
        newMap = MonoidMap()
        newMap.S1 = self.S1
        newMap.all_map = self.all_map.copy()
        newMap.s1_unmatched_generatos = self.s1_unmatched_generatos.copy()
        return newMap