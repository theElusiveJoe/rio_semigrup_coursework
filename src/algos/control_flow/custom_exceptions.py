class ControlFlowException(Exception):
    pass


class NoDecision(ControlFlowException):
    pass


class HclassesMissmatch(NoDecision):
    pass
