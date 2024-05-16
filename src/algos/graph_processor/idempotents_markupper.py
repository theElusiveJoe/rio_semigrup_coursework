from algebra.graph import Graph


def markup_idempotents(graph: Graph):
    for node in graph.nodes:
        if node.val * node.val == node.val:
            node.is_idempotent = True
        else:
            node.is_idempotent = False
