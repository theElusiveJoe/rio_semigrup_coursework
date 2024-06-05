from dataclasses import dataclass
import itertools

from algebra.graph.graph import MultipleType


OPT_SECOND_CHAIN_MULT_TYPE = [
    MultipleType.graph_traverse, MultipleType.monoid_multiply]
OPT_CACHE_PROTO_CHAINS = [True, False]
OPT_CACHE_IMAGE_CHAINS = [True, False]
OPT_CACHE_IMAGE_SET = [True, False]
OPT_CACHE_H_IMAGE_SET = [True, False]
OPT_CHAIN_MAX_LEN = [1, 10, 100, float('infinity')]


@dataclass
class AlgoConfig():
    second_chain_mult_type: MultipleType = MultipleType.graph_traverse

    cache_proto_chains: bool = True
    cache_image_chains: bool = True
    chain_max_len: float = float('infinity')

    cache_isom_images_set: bool = False
    cache_isom_h_images_set: bool = False


def get_all_configs():
    configs = []

    for chain_mult, proto_chain, image_chain, image_set, h_image_set, chain_max_len in itertools.product(
        OPT_SECOND_CHAIN_MULT_TYPE,
        OPT_CACHE_PROTO_CHAINS,
        OPT_CACHE_IMAGE_CHAINS,
        OPT_CACHE_IMAGE_SET,
        OPT_CACHE_H_IMAGE_SET,
        OPT_CHAIN_MAX_LEN
    ):
        configs.append(AlgoConfig(
            second_chain_mult_type=chain_mult,

            cache_proto_chains=proto_chain,
            cache_image_chains=image_chain,
            chain_max_len=chain_max_len,

            cache_isom_images_set=image_set,
            cache_isom_h_images_set=h_image_set,

        ))

    return configs
