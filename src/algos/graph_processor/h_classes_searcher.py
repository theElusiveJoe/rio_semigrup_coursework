import itertools
from algebra.graph import Graph, Node, Hclass


def search_H_classes(graph: Graph):
    Lclasses = _CCSearch(graph, True).run()
    Rclasses = _CCSearch(graph, False).run()

    Hclasses = list(
        map(Hclass,
            filter(lambda x: len(x) > 0,
                   map(lambda xy: xy[0] & xy[1],
                       itertools.product(Lclasses, Rclasses)))))
    return Hclasses


class _CCSearch():
    graph: Graph
    inv_graph: dict[Node, set[Node]]
    mode: bool

    def __init__(self, graph: Graph, mode: bool) -> None:
        self.graph = graph
        self.mode = mode

    def run(self):
        self.build_inv_graph()
        topo_order = self.topo_sort()
        res = self.color_cc(topo_order)
        return res

    def build_inv_graph(self):
        self.inv_graph = dict((node, set()) for node in self.graph.nodes)

        for v1 in self.graph.nodes:
            for v2 in (v1.cay_l.values() if self.mode else v1.cay_r.values()):
                self.inv_graph[v2].add(v1)

    def topo_sort(self):
        for node in self.inv_graph.keys():
            node.flag1 = False

        stack = []

        def dfs(v1: Node):
            v1.flag1 = True
            for v2 in self.inv_graph[v1]:
                if v2.flag1:
                    continue
                dfs(v2)
            stack.append(v1)

        for v in self.inv_graph.keys():
            if v.flag1:
                continue
            dfs(v)

        return stack[::-1]

    def color_cc(self, topo_order):
        for node in self.graph.nodes:
            node.flag1 = False

        def dfs(v1: Node):
            v1.flag1 = True
            cc = {v1}
            for v2 in (v1.cay_l.values() if self.mode else v1.cay_r.values()):
                if v2.flag1:
                    continue
                cc |= dfs(v2)
            return cc

        ccs: list[set[Node]] = []
        for v in topo_order:
            if v.flag1:
                continue
            ccs.append(dfs(v))

        return ccs