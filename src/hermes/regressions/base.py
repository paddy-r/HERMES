import pandas as pd


class RegressionModel:

    RESPONSE_COLUMN = "__response__"
    registry = {}
    minimum_waves = 1

    def __init_subclass__(
        cls,
        **kwargs
    ):
        super().__init_subclass__(**kwargs)

        RegressionModel.registry[
            cls.__name__
        ] = cls

    def create_response(
            self,
            merged,
            response
    ):
        current = merged[
            f"{response}_current"
        ]

        future = merged[
            f"{response}_next"
        ]

        return self.transform_response(
            current,
            future
        )

    def transform_response(
            self,
            current,
            future
    ):
        return future

    def create_training_dataset(
            self,
            merged,
            predictors,
            response
    ):
        training_data = pd.DataFrame()

        for predictor in predictors:
            training_data[predictor] = (
                merged[
                    predictor + "_current"
                    ]
            )

        training_data[self.RESPONSE_COLUMN] = (
            self.create_response(
                merged,
                response
            )
        )

        return training_data

    def fit(self, X, y):
        raise NotImplementedError

    def predict(
            self,
            X
    ):
        return self.model.predict(
            X
        )

    def get_metadata(self):
        raise NotImplementedError
