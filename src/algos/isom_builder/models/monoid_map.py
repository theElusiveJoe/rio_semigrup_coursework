from algebra.universe import Universe
from algebra.monoid import MonoidController
from algebra.graph import Node, Graph


class MonoidMap:
    S1: MonoidController
    G1: Graph

    # TODO: переписать через двусторонний словарь

    all_map: dict[Node, Node]
    gen_set_map: dict[Node, Node]
    s1_unmatched_generatos: set[Node]

    def __init__(self, initObjects: tuple[MonoidController, Graph] | None = None) -> None:
        if initObjects is None:
            return

        self.S1, self.G1 = initObjects
        self.all_map = dict()
        self.gen_set_map = dict()
        self.s1_unmatched_generatos = set(
            [self.G1.val2node[val] for val in self.S1.generators])

    def __str__(self):
        strs = []
        strs.append("MONOID_MAP{")
        # strs.append(f"    unmatched_generators: {self.s1_unmatched_generatos}")
        # strs.append(
        #     f"    all_map: {{{''.join([f'{x} -> {y}' for x,y in self.all_map.items()])}}}")
        strs.append("    gen_set_map:")
        for x, y in self.gen_set_map.items():
            strs.append(f'        {x} -> {y}')
        strs.append('}')
        return '\n'.join(strs)

    def is_gen_set_done(self):
        return len(self.s1_unmatched_generatos) == 0

    def map_set(self, a: Node, b: Node):
        # remove from unmatched generator, if there
        is_generator = True
        try:
            self.s1_unmatched_generatos.remove(a)
        except KeyError:
            is_generator = False

        assert a not in self.all_map.keys()

        self.all_map[a] = b
        if is_generator:
            self.gen_set_map[a] = b

    def map_get(self, a: Node):
        return self.all_map.get(a)

    def make_copy(self):
        newMap = MonoidMap()
        newMap.S1 = self.S1
        newMap.all_map = self.all_map.copy()
        newMap.s1_unmatched_generatos = self.s1_unmatched_generatos.copy()
        newMap.gen_set_map = self.gen_set_map.copy()
        return newMap
