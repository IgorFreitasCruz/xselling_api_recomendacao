import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder


class Apriori:
    def __init__(
        self,
        *,
        TransactionEncoder: TransactionEncoder,
        apriori: apriori,
        association_rules: association_rules,
    ) -> None:
        self._transactional_encoder = TransactionEncoder
        self._apriori = apriori
        self._association_rules = association_rules

    def matriz_incidencia(self, *, produtos: list) -> pd.DataFrame:
        transaction_encoder = self._transactional_encoder()
        matrix_incidencia = transaction_encoder.fit(produtos).transform(
            produtos
        )
        return pd.DataFrame(
            matrix_incidencia, columns=transaction_encoder.columns_
        )

    def apriori(
        self,
        *,
        matrix_incidencia: pd.DataFrame,
        min_support: float,
        use_colnames=True,
    ):
        return self._apriori(
            matrix_incidencia,
            min_support=min_support,
            use_colnames=use_colnames,
        )

    def association_rules(
        self,
        *,
        conjuntos_produtos: pd.DataFrame,
        metric: str,
        min_threshold: float,
    ):
        regras = self._association_rules(
            conjuntos_produtos, metric=metric, min_threshold=min_threshold
        )
        return regras


apriori_driver = Apriori(
    TransactionEncoder=TransactionEncoder,
    apriori=apriori,
    association_rules=association_rules,
)
