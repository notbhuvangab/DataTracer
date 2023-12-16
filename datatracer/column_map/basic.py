import logging

from sklearn.ensemble import RandomForestRegressor

from datatracer.column_map.base import ColumnMapSolver
from datatracer.column_map.transformer import Transformer

LOGGER = logging.getLogger(__name__)


class BasicColumnMapSolver(ColumnMapSolver):
    def __init__(self, *args, **kwargs):
        self._model_args = args
        self._model_kwargs = kwargs

    def _get_importances(self, X, y):
        model = RandomForestRegressor(*self._model_args, **self._model_kwargs)
        model.fit(X, y)

        return model.feature_importances_

    def solve(self, tables, foreign_keys, target_table, target_field):
        transformer = Transformer(tables, foreign_keys)

        X, y = transformer.forward(target_table, target_field)

        importances = self._get_importances(X, y)
        return transformer.backward(importances)
