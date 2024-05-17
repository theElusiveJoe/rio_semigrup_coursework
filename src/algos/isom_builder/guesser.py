from algos.isom_builder.models import IsomState
from .checker import check
from algebra.graph import Node, Hclass


def get_candidate_to_guess(state: IsomState) -> tuple[Node, Hclass, Hclass] | None:
    '''
    doesn`t changes IsomState, just drops a field for guesses
    '''
    for node in state.gs1_unmatched_nodes:
        hclass_image = state.hf.map_get(node.hclass)
        if hclass_image is None:
            continue
        return (node, node.hclass, hclass_image)

    return None


def guess_hclass(state: IsomState) -> tuple[(None | IsomState), bool]:
    '''
    guaranteed, that hclass of random_node doesn`t have hclass-image
    '''
    random_node = state.gs1_unmatched_nodes.pop()
    state.gs1_unmatched_nodes.add(random_node)
    random_hclass = random_node.hclass

    # TODO: remove after debug
    assert random_hclass not in state.hf.hclasses_map.keys()

    hclass_image_src = (state.hf.hi_unmatched if random_hclass.has_idempotent else state.hf.hni_unmatched)[
        random_hclass.size][1]
    for random_hclass_image in hclass_image_src:
        next_state = state.make_copy()
        next_state.hf.map_set(random_hclass, random_hclass_image)
        if random_hclass.has_idempotent:
            # TODO: add compatibility check for this set_f operation
            # TODO: resolve type error
            next_state.set_f(random_hclass.idempotent,          # type: ignore
                             random_hclass_image.idempotent)    # type: ignore
        result_state, ok = guess_elem(next_state)
        if ok:
            return result_state, True
        continue

    return None, False


def check_guess(state: IsomState, a: Node, b: Node) -> bool:
    '''
    insert an and bn chains isomorphisms,
    so it changes IsomState.f
    '''
    # TODO: add cache for an chain --- we dont need to compute it
    # each time we check guess for a

    # TODO: may be remove after debug
    # use only to check map purpose for generating value
    assert a.val in IsomState.G1.S.generators

    # TODO: may be remove after debug
    # use only for unmatched values
    assert a in IsomState.gs1_unmatched_nodes

    # TODO: remove after debug or cache gs2_unmatched_nodes
    assert b not in IsomState.f.all_map.values()

    # firstly we should match hclasses
    assert state.hf[a.hclass] == b.hclass

    degree = 1
    seen_a = [a]
    seen_b = [b]
    an, bn = a, b

    while True:
        degree += 1
        an = state.G1.mult_nodes(an, a, use_cay=True)
        # TODO: cmp with use_monoid=True
        bn = state.G2.mult_nodes(bn, b, use_cay=False, use_monoid=False)

        try:
            ia = seen_a.index(an)
        except ValueError:
            ia = -1
        try:
            ib = seen_b.index(bn)
        except ValueError:
            ib = -1

        # closures are inconsistent
        if ia != ib:
            return False

        # closures are consistent
        if ia == -1:
            # closure not completed
            # set new chain elem into isomorphism
            # TODO: add (an,bn) consistency check
            state.set_f(an, bn)
            # TODO: add some additional consistency checks
            continue
        else:
            # closure completed, parrallel chain looped
            return True


def guess_elem(state: IsomState) -> tuple[(None | IsomState), bool]:
    if state.f.is_gen_set_done():
        ok = check(state)
        if ok:
            return state, True
        return None, False

    guess_field = get_candidate_to_guess(state)
    if guess_field is None:
        return guess_hclass(state)

    a, ha, hb = guess_field
    for b in hb.elems:
        # TODO: make it faster!!!
        if b in IsomState.f.all_map.values():
            continue
        next_state = state.make_copy()
        # TODO: add simple consistency check
        next_state.f.map_set(a, b)
        # and here is deep consistency check
        ok = check_guess(next_state, a, b)
        if ok:
            final_state, deep_ok = guess_elem(next_state)
            if deep_ok:
                return final_state, True

    return None, False
