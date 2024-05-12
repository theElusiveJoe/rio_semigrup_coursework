from algebra.graph import Graph


def search_idempotents(graph: Graph):
    for node in graph.nodes:
        if node.val * node.val == node.val:
            node.is_idempotent = True
        else:
            node.is_idempotent = False


def search_cc(graph: Graph):
    pass

def prettify_graph(graph: Graph):
    search_idempotents(graph)
