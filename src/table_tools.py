from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from beran_core import LOGS_DIR


BASE = 97
TABLE_SIZE = BASE * BASE * BASE


def table_index(outer: int, left: int, right: int) -> int:
    return (outer * BASE + left) * BASE + right


def load_composition_table(path: Path | None = None) -> list[int]:
    input_path = path if path is not None else LOGS_DIR / "beran_composition_table.csv"
    table = [0] * TABLE_SIZE

    with input_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            outer = int(row["outer"])
            left = int(row["left"])
            right = int(row["right"])
            result = int(row["result"])
            table[table_index(outer, left, right)] = result

    return table


def superpose(table: list[int], outer: int, left: int, right: int) -> int:
    return table[table_index(outer, left, right)]


def closure_from_ids(generators: Iterable[int], table: list[int]) -> frozenset[int]:
    closed = set(int(x) for x in generators)

    changed = True
    while changed:
        changed = False
        current = sorted(closed)
        new_items: set[int] = set()

        for outer in current:
            for left in current:
                for right in current:
                    result = superpose(table, outer, left, right)
                    if result not in closed:
                        new_items.add(result)

        if new_items:
            closed.update(new_items)
            changed = True

    return frozenset(closed)


def elements_to_string(elements: Iterable[int]) -> str:
    return " ".join(str(x) for x in sorted(elements))


def string_to_elements(text: str) -> frozenset[int]:
    if not text.strip():
        return frozenset()
    return frozenset(int(x) for x in text.split())
