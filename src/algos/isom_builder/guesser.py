from algos.isom_builder.models import IsomState
from .checker import check
from algebra.graph import Node, Hclass


def get_candidate_to_guess(state: IsomState) -> tuple[Node, Hclass, Hclass] | None:
    for node in state.gs1_unmatched_nodes:
        hclass_image = state.hf.map_get(node.hclass)
        if hclass_image is None:
            continue
        return (node, node.hclass, hclass_image)
    
    return None

def guess_h_class(state: IsomState) -> tuple[(None | IsomState), bool]:
    '''
    guaranteed, that hclass of random_node doesn`t have hclass-image
    '''
    random_node = state.gs1_unmatched_nodes.pop()
    state.gs1_unmatched_nodes.add(random_node)
    random_hclass = random_node.hclass

    # TODO: remove after debug
    assert random_hclass not in state.hf.hclasses_map.keys()

    hclass_image_src = (state.hf.hi_unmatched if random_hclass.has_idempotent else state.hf.hni_unmatched)[random_hclass.size][1]
    for random_hclass_image in hclass_image_src:
        next_state = state.make_copy()
        next_state.hf.map_set(random_hclass, random_hclass_image)
        if random_hclass.has_idempotent:
            # TODO: add compatibility check for this set_f operation
            # TODO: resolve type error
            next_state.set_f(random_hclass.idempotent, random_hclass_image.idempotent) # type: ignore
        result_state, ok = guess_elem(next_state)
        if ok:
            return result_state, True
        continue

    return None, False


def guess_elem(state: IsomState) -> tuple[(None | IsomState), bool]:
    if state.f.is_gen_set_done():
        ok = check(state)
        if ok:
            return state, True
        return None, False

    guess_field = get_candidate_to_guess(state)
    if guess_field is None:
        return guess_h_class(state)
    
    
