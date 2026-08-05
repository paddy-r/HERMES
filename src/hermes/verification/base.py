class Verifier:

    registry = {}

    priority = 0

    def __init_subclass__(cls, **kwargs):

        super().__init_subclass__(**kwargs)

        Verifier.registry[
            cls.__name__
        ] = cls

        # print(
        #     f"Registering verifier: "
        #     f"{cls.__name__}"
        # )

    def verify(self, simulation):

        print(
            f"Running verifier: "
            f"{self.__class__.__name__}"
        )

        self._verify(simulation)

    def _verify(self, simulation):
        pass
