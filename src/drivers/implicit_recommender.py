from abc import ABC, abstractmethod

import numpy as np
from implicit.als import AlternatingLeastSquares
from implicit.bpr import BayesianPersonalizedRanking
from implicit.nearest_neighbours import bm25_weight
from implicit.recommender_base import RecommenderBase
from pandas import DataFrame
from scipy.sparse import csr_matrix


class RecommendationOutputFormatter(ABC):
    @abstractmethod
    def format_output(self) -> DataFrame:
        pass


class MatrixBuilder(ABC):
    @abstractmethod
    def build_csr_matrix(self, client_products_df: DataFrame) -> csr_matrix:
        ...


class SimilarUsersFormatter(RecommendationOutputFormatter):
    def __init__(
        self,
        item_to_index: dict,
        ids: np.array,
        client_id: int,
        scores: np.array,
        client_prod: csr_matrix,
    ):
        self._item_to_index = item_to_index
        self._ids = ids
        self._client_id = client_id
        self._scores = scores
        self._client_prod = client_prod

    def format_output(self) -> DataFrame:
        return DataFrame(
            {
                'Item': np.array(list(self._item_to_index.keys()))[self._ids],
                'score': self._scores,
                'already_liked': np.in1d(
                    self._ids, self._client_prod[self._client_id].indices
                ),
            }
        )


class SimilarItemsFormatter(RecommendationOutputFormatter):
    def __init__(self, item_to_index: dict, ids: np.array, scores: np.array):
        self._item_to_index = item_to_index
        self._ids = ids
        self._scores = scores

    def format_output(self) -> DataFrame:
        return DataFrame(
            {
                'Item': np.array(list(self._item_to_index.keys()))[self._ids],
                'score': self._scores,
            }
        )


class SparseMatrixBuilder(MatrixBuilder):
    """
    A class that builds a sparse matrix representation of client-product
    interactions from a DataFrame.

    Methods:
    - build_csr_matrix(client_products_df: DataFrame) -> csr_matrix:
        Builds a sparse matrix representation of client-product interactions
        using the CSR format.
    """

    @staticmethod
    def build_csr_matrix(client_products_df: DataFrame) -> csr_matrix:
        """
        Builds a sparse matrix representation of client-product interactions
        using the CSR format.

        Args:
        - client_products_df (DataFrame): A DataFrame containing client-product
        interactions.

        Returns:
        - csr_matrix: A sparse matrix representation of the client-product
        interactions.
        - item_to_index: A mapper of items names to its index value
        """
        unique_items = list(
            set(
                item
                for items in client_products_df['categorias']
                for item in items
            )
        )
        # Create a mapping of item names to unique indices
        item_to_index = {
            item: index for index, item in enumerate(unique_items)
        }

        rows = []
        cols = []
        data = []

        for user_id, items in zip(
            client_products_df['id'], client_products_df['categorias']
        ):
            for item in items:
                rows.append(item_to_index[item])
                cols.append(user_id)
                data.append(1)
                matrix_shape = (max(rows) + 1, max(cols) + 1)

        return (
            csr_matrix((data, (rows, cols)), shape=matrix_shape),
            item_to_index,
        )


class ImplicitRecommenderDriver:
    """Recommender system using implicit feedback."""

    def __init__(self, implicit_model: RecommenderBase):
        """Initialize the recommender with the specified implicit model."""
        self.implicit_model = implicit_model

    @classmethod
    def build_recommender(cls, algo_type: str, **kwargs):
        """Build and return a recommender based on the specified algorithm type.

        Args:
            algo_type (str): The choice of algorithm. Options are 'als' and 'bpr'.

        Raises:
            ValueError: Raises value error for unsupported algorithm type.

        Returns:
            Union[
            AlternatingLeastSquares,
            BayesianPersonalizedRanking,
        ]: Provided types of recommender algorithms
        """

        supported_algorithms = {
            'als': cls._build_als_recommender,
            'bpr': cls._build_bpr_recommender,
        }

        builder_func = supported_algorithms.get(algo_type)

        if builder_func is None:
            raise ValueError(
                f"""Unsupported algorithm type {algo_type}. Supported types are {', '.join(supported_algorithms.keys())}."""
            )

        implicit_model = builder_func(**kwargs)
        return cls(implicit_model)

    @staticmethod
    def matrix_weighting(
        *, interaction_matrix: csr_matrix, method: str, **kwargs
    ) -> csr_matrix:
        """Weight the matrix, both to reduce impact of clients that have
        purchased the same product thousands of times and to reduce the weight
        given to popular products

        Args:
            interaction_matrix (csr_matrix): A client products sparse matrix
            K1 (int, optional): Saturation of term frequency. Defaults to 10.
            B (float, optional): Controls the importance of length normalization. Defaults to 0.8.

        Returns:
            csr_matrix: A weighted client products sparse matrix
        """
        if method == 'bm25':
            # Return the transpose since the most of the functions in implicit
            # expect (user, item) sparse matrices instead of (item, user)
            return bm25_weight(interaction_matrix, **kwargs).T.tocsr()
        else:
            raise ValueError(f'Unsupported weighting method: {method}')

    @classmethod
    def _build_als_recommender(
        cls,
        *,
        factors: int = 100,
        regularization: float = 0.01,
        alpha: float = 1,
    ):
        """Build an Alternating Least Squares recommender."""
        return AlternatingLeastSquares(
            factors=factors, regularization=regularization, alpha=alpha
        )

    @classmethod
    def _build_bpr_recommender(
        cls,
        *,
        factors: int = 100,
        learning_rate: float = 0.01,
        regularization: float = 0.01,
    ):
        """Build an Bayesian Personalized Ranking recommender."""
        return BayesianPersonalizedRanking(
            factors=factors,
            learning_rate=learning_rate,
            regularization=regularization,
        )

    def fit(self, client_products_matrix: csr_matrix) -> None:
        """Fit the model the the client products matrix

        Args:
            client_products_matrix (scipy.sparse.csr_matrix): client products
            sparse matrix
        """
        self.implicit_model.fit(client_products_matrix)


implicit_driver = ImplicitRecommenderDriver
