from algebra.monoid import MonoidController, MonoidElem
from algebra.graph import Graph, Node


def military_algo(S: MonoidController):
    return _MilitaryAlgo().run(S)


class _MilitaryAlgo():
    S: MonoidController
    graph: Graph
    queue: list[Node]
    queue2: list[Node]

    def run(self, S: MonoidController) -> Graph:
        self.S = S

        self.setup()
        self.main_cycle()

        return self.graph

    def setup(self):
        self.graph = Graph(self.S)
        self.queue = []
        self.queue2 = []

        Ne = Node(
            val=self.S.generators[0].identity(),
            str=MonoidElem.identity()
        )
        self.graph.add_node(Ne)

        for i in range(len(self.S)):
            val, str = self.S.get_value_i(i), self.S.get_string_i(i)
            N = Node(val=val, str=str)
            self.graph.add_node(N)
            Ne.set_cay_l(val, N)
            Ne.set_cay_r(val, N)
            self.queue.append(N)

    def main_cycle(self):
        while len(self.queue) > 0:
            N = self.queue.pop(0)
            self.queue2.append(N)
            b = N.str.first()
            s = N.str.suffix()

            for i in range(len(self.S)):
                ai = self.S.get_string_i(i)
                vai = self.S.get_value_i(i)

                sai = s+ai
                Nsai = self.graph.str2node.get(sai)

                if Nsai is None:  # sai редуцируется
                    Nr = self.graph.str2node[s].cay_r[vai]
                    if Nr.is_identity():
                        N.cay_r[vai] = self.graph.str2node[b]
                    else:
                        N.cay_r[vai] = self.graph.str2node[Nr.str.prefix()] \
                            .cay_l[self.graph.str2node[b].val] \
                            .cay_r[self.graph.str2node[Nr.str.last()].val]
                else:
                    v = N.val * vai

                    Nv = self.graph.val2node.get(v)
                    if Nv is not None:
                        N.cay_r[vai] = Nv
                    else:
                        Nv = Node(val=v, str=N.str+ai)
                        self.graph.add_node(Nv)
                        self.queue.append(Nv)
                        N.cay_r[vai] = Nv

            if len(self.queue) > 0 and len(self.queue2) > 0 and \
                    self.queue[0].str.len() > self.queue2[0].str.len() or len(self.queue) == 0:
                while len(self.queue2) > 0:
                    N = self.queue2.pop(0)

                    for i in range(len(self.S)):
                        ai = self.S.get_string_i(i)
                        vai = self.S.get_value_i(i)
                        N.cay_l[vai] = self.graph.str2node[N.str.prefix()] \
                            .cay_l[self.graph.str2node[ai].val] \
                            .cay_r[self.graph.str2node[N.str.last()].val]
