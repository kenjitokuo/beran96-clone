from __future__ import annotations

from typing import Iterable, Set

from beran_core import BeranOperation, compose_operation, load_beran96, operation_index


def operations_by_id() -> dict[int, BeranOperation]:
    return {op.beran_id: op for op in load_beran96()}


def closure_of(generators: Iterable[int]) -> set[int]:
    operations = operations_by_id()
    pair_to_id = operation_index(operations.values())

    closed: Set[int] = set(generators)
    if not closed:
        return set()

    changed = True
    while changed:
        changed = False
        current = sorted(closed)
        for outer_id in current:
            outer = operations[outer_id]
            for left_id in current:
                left = operations[left_id]
                for right_id in current:
                    right = operations[right_id]
                    result = compose_operation(outer, left, right, pair_to_id)
                    if result not in closed:
                        closed.add(result)
                        changed = True

    return closed


def contains_projections(generators: Iterable[int]) -> set[int]:
    result = set(generators)
    result.add(22)  # x
    result.add(39)  # y
    return result
