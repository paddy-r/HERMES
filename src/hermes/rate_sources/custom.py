import numexpr as ne
from hermes.base_classes import FunctionalForm


class Custom(FunctionalForm):

    name = "custom"

    def __init__(self, expression):
        self.expression = expression

    def evaluate(self, x):
        return ne.evaluate(
            self.expression,
            local_dict={"x": x}
        )
    