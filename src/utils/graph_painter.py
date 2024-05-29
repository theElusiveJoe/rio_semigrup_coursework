
import graphviz
import os
import pathlib

from algebra.graph import Graph, Hclass
from algos.isom_builder.models.monoid_map import MonoidMap


def _paint_graph(dot: graphviz.Digraph, graph: Graph):
    # вершины
    for node in graph.nodes:
        dot.node(str(id(node)), label=node.label())

    # ребра правого графа Кейли
    for v1 in graph.nodes:
        for x, v2 in v1.cay_l.items():
            dot.edge(str(id(v1)), str(id(v2)),
                     graph.val2node[x].label(), color='grey')

    label = ""
    for i, x in enumerate(graph.S.generators):
        label += f"{graph.S.get_string_i(i)} = {x}\n"
    dot.graph_attr['label'] = label
    dot.graph_attr['labelloc'] = "b"


def _paint_hclasses(dot: graphviz.Digraph, hclasses: set[Hclass]):
    for hclass in hclasses:
        # autopep8: off
        with dot.subgraph(name=f"cluster_{id(hclass)}") as subgraph: # type: ignore
        # autopep8: on
            subgraph.graph_attr['label'] = ""
            subgraph.graph_attr['style'] = "rounded"
            subgraph.graph_attr['fillcolor'] = "red"
            for node in hclass.elems:
                subgraph.node(str(id(node)))


def _paint_isom(dot: graphviz.Digraph, isom: MonoidMap):
    for v1, v2 in isom.gen_set_map.items():
        dot.edge(str(id(v1)), str(id(v2)), color='green')


def paint_graph(
        graph1: Graph | None = None, graph2: Graph | None = None,
        hclasses1: set[Hclass] | None = None, hclasses2: set[Hclass] | None = None,
        isom: MonoidMap | None = None,
        filename: str = 'result') -> str:
    dot = graphviz.Digraph(
        node_attr={
            'color': 'lightblue2',
            'style': 'filled'})

    for i, (graph, hclasses) in enumerate(
            [(graph1, hclasses1), (graph2, hclasses2)]):
        if graph is not None:
            with dot.subgraph(name=f"cluster_{i}") as subgraph:  # type: ignore
                subgraph.graph_attr['style'] = 'dotted'
                _paint_graph(subgraph, graph)
                if hclasses is not None:
                    _paint_hclasses(subgraph, hclasses)

    if isom is not None:
        _paint_isom(dot, isom)

    path = pathlib.Path(
        f'{os.environ["PYTHONPATH"]}/../output/{filename}_graph').resolve()
    res = dot.render(path, format='png', cleanup=True)
    return res
