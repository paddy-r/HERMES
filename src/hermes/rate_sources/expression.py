import numexpr as ne
from hermes.rate_sources.base import FunctionalForm


class Expression(FunctionalForm):

    def __init__(self, domains, parameters, expression, **kwargs):
        super().__init__(domains, parameters, **kwargs)
        self.expression = expression

    def evaluate(self, domains):
        context = {}

        for domain in self.domains:
            context[domain] = domains[domain]

        for name, value in self.parameters.items():
            context[name] = value

        return ne.evaluate(self.expression,
                           local_dict=context)
