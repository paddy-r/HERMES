class RegressionModel:

    registry = {}

    def __init_subclass__(
        cls,
        **kwargs
    ):
        super().__init_subclass__(**kwargs)

        RegressionModel.registry[
            cls.__name__
        ] = cls

    def fit(self, X, y):
        raise NotImplementedError

    def predict(
            self,
            X
    ):
        return self.model.predict(
            X
        )

    def save(self, filepath):
        raise NotImplementedError

    @classmethod
    def load(cls, filepath):
        raise NotImplementedError

    def get_metadata(self):
        raise NotImplementedError
