from algos.isom_builder.models.chain import Chain

class ChainWinder:
    chain: Chain
    cur_degree: int

    def __init__(self, chain: Chain) -> None:
        self.chain = chain
        self.cur_degree = 0

    def next(self):
        self.cur_degree += 1
        if self.chain.is_completed == False:
            self.chain.build_next()
        return self.chain.get_degree(self.cur_degree)

    def at_the_end(self) -> bool:
        return self.chain.is_completed and self.cur_degree == self.chain.len()
