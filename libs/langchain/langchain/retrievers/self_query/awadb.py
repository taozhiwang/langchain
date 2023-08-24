from typing import Dict, Tuple, Union

from langchain.chains.query_constructor.ir import (
    Comparator,
    Comparison,
    Operation,
    Operator,
    StructuredQuery,
    Visitor,
)

COMPARATOR_TO_TQL = {
    Comparator.EQ: "",
    Comparator.GT: "max_",
    Comparator.GTE: "maxe_",
    Comparator.LT: "min_",
    Comparator.LTE: "mine_",
}

class AwaDBTranslator(Visitor):
    """Translate `AwaDB` internal query language elements to valid filters."""

    allowed_operators = [Operator.AND, Operator.OR]
    """Subset of allowed logical operators."""
    allowed_comparators = [
        Comparator.EQ,
        Comparator.GT,
        Comparator.GTE,
        Comparator.LT,
        Comparator.LTE,
    ]
    """Subset of allowed logical comparators."""

    def _format_func(self, func: Union[Operator, Comparator]) -> str:
        self._validate_func(func)
        if isinstance(func, Operator):
            return f"${func.value}"  # type: ignore
        elif isinstance(func, Comparator):
            return COMPARATOR_TO_TQL[func.value]

    def visit_operation(self, operation: Operation) -> Dict:
        args = [arg.accept(self) for arg in operation.arguments]
        return {self._format_func(operation.operator): args}

    def visit_comparison(self, comparison: Comparison) -> Dict:
        comparator = self._format_func(comparison.comparator)
        attribute = comparator + comparison.attribute
        print("11111111111111111")
        print("meta_filter = " + str({attribute : comparison.value}))
        return "meta_filter = " + str({attribute : comparison.value})

    def visit_structured_query(
        self, structured_query: StructuredQuery
    ) -> Tuple[str, dict]:
        if structured_query.filter is None:
            kwargs = {}
        else:
            kwargs = {"filter": structured_query.filter.accept(self)}
        return structured_query.query, kwargs
