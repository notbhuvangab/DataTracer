import numpy as np


class Transformer:

    def __init__(self, tables, foreign_keys):
   
        self.tables = tables
        self.foreign_keys = foreign_keys

    def forward(self, table, field):

        df = self.tables[table]
        df = df.select_dtypes("number")
        df = df.fillna(0.0)
        X, y = df.drop([field], axis=1), df[field]
        self.columns = [(table, col_name) for col_name in X.columns]
        X, y = X.values, y.values

        X_new, columns_new = self._get_counts(table)
        if columns_new:
            X = np.concatenate([X, X_new], axis=1)
            self.columns.extend(columns_new)

        X_new, columns_new = self._get_aggregations(table)
        if columns_new:
            X = np.concatenate([X, X_new], axis=1)
            self.columns.extend(columns_new)

        return X, y

    def _get_counts(self, table):
  
        X, columns = [], []
        for fk in self.foreign_keys:
            if fk["ref_table"] != table:
                continue

            # Count the number of rows for each key.
            child_table = self.tables[fk["table"]].copy()
            child_table["_dummy_"] = 0.0
            child_counts = child_table.groupby(fk["field"]).count().iloc[:, 0:1]
            child_counts.columns = ["_tmp_"]

            # Merge the counts into the parent table
            parent_table = self.tables[table]
            parent_table = parent_table.set_index(fk["ref_field"])
            parent_table = parent_table.join(child_counts).reset_index()

            X.append(parent_table["_tmp_"].fillna(0.0).values)
            columns.append((fk["table"], fk["field"]))

        return np.array(X).transpose(), columns

    def _get_aggregations(self, table):

        X, columns = [], []
        for fk in self.foreign_keys:
            if fk["ref_table"] != table:
                continue

            for op, op_name in [
                (lambda x: x.sum(), "SUM"),
                (lambda x: x.max(), "MAX"),
                (lambda x: x.min(), "MIN"),
                (lambda x: x.std(), "STD"),
            ]:
                # Count the number of rows for each key.
                child_table = self.tables[fk["table"]].copy()
                if len(child_table.columns) <= 1:
                    continue

                child_counts = op(child_table.groupby(fk["field"]))
                old_column_names = list(child_counts.columns)
                child_counts.columns = ["%s(%s)" % (op_name, col_name)
                                        for col_name in old_column_names]

                # Merge the counts into the parent table
                parent_table = self.tables[table]
                parent_table = parent_table.set_index(fk["ref_field"])
                parent_table = parent_table.join(child_counts).reset_index()

                for old_name, col_name in zip(old_column_names, child_counts.columns):
                    if parent_table[col_name].dtype.kind == "f":
                        X.append(parent_table[col_name].fillna(0.0).values)
                        columns.append((fk["table"], old_name))

        return np.array(X).transpose(), columns

    def backward(self, feature_importances):
  
        obj = {}
        for column, importance in zip(self.columns, feature_importances):
            obj[column] = importance

        return obj
