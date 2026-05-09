from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Tuple

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
LOGS_DIR = ROOT / "logs"

BOOL_INPUTS: Tuple[Tuple[int, int], ...] = ((0, 0), (0, 1), (1, 0), (1, 1))

SHADOW_TABLES: Dict[str, Tuple[int, int, int, int]] = {
    "ZERO": (0, 0, 0, 0),
    "AND": (0, 0, 0, 1),
    "LDIFF": (0, 0, 1, 0),
    "RDIFF": (0, 1, 0, 0),
    "NOR": (1, 0, 0, 0),
    "X": (0, 0, 1, 1),
    "Y": (0, 1, 0, 1),
    "EQ": (1, 0, 0, 1),
    "XOR": (0, 1, 1, 0),
    "NOT_Y": (1, 0, 1, 0),
    "NOT_X": (1, 1, 0, 0),
    "OR": (0, 1, 1, 1),
    "RIMP": (1, 0, 1, 1),
    "IMP": (1, 1, 0, 1),
    "NAND": (1, 1, 1, 0),
    "ONE": (1, 1, 1, 1),
}

TABLE_TO_SHADOW: Dict[Tuple[int, int, int, int], str] = {v: k for k, v in SHADOW_TABLES.items()}

BLOCKS = ("ZERO", "X", "Y", "NOT_Y", "NOT_X", "ONE")

BLOCK_COMPLEMENT = {
    "ZERO": "ONE",
    "ONE": "ZERO",
    "X": "NOT_X",
    "NOT_X": "X",
    "Y": "NOT_Y",
    "NOT_Y": "Y",
}


@dataclass(frozen=True)
class BeranOperation:
    beran_id: int
    block: str
    shadow: str


def load_beran96(path: Path | None = None) -> list[BeranOperation]:
    input_path = path if path is not None else DATA_DIR / "beran96.csv"
    operations: list[BeranOperation] = []
    with input_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            operations.append(
                BeranOperation(
                    beran_id=int(row["beran_id"]),
                    block=row["block"],
                    shadow=row["shadow"],
                )
            )

    if len(operations) != 96:
        raise ValueError(f"Expected 96 Beran operations, got {len(operations)}.")

    seen_ids = {op.beran_id for op in operations}
    if seen_ids != set(range(1, 97)):
        raise ValueError("Beran IDs must be exactly 1 through 96.")

    seen_pairs = {(op.block, op.shadow) for op in operations}
    if len(seen_pairs) != 96:
        raise ValueError("Each (block, shadow) pair must occur exactly once.")

    for op in operations:
        if op.block not in BLOCKS:
            raise ValueError(f"Unknown block: {op.block}")
        if op.shadow not in SHADOW_TABLES:
            raise ValueError(f"Unknown shadow: {op.shadow}")

    return operations


def operation_index(operations: Iterable[BeranOperation]) -> dict[tuple[str, str], int]:
    return {(op.block, op.shadow): op.beran_id for op in operations}


def eval_shadow(shadow: str, x: int, y: int) -> int:
    table = SHADOW_TABLES[shadow]
    index = BOOL_INPUTS.index((x, y))
    return table[index]


def compose_shadow(outer: str, left: str, right: str) -> str:
    values = []
    for x, y in BOOL_INPUTS:
        gx = eval_shadow(left, x, y)
        hy = eval_shadow(right, x, y)
        values.append(eval_shadow(outer, gx, hy))
    table = tuple(values)
    if table not in TABLE_TO_SHADOW:
        raise ValueError(f"Unknown composed Boolean table: {table}")
    return TABLE_TO_SHADOW[table]


def compose_block(outer: str, left: str, right: str) -> str:
    if outer == "ZERO":
        return "ZERO"
    if outer == "ONE":
        return "ONE"
    if outer == "X":
        return left
    if outer == "Y":
        return right
    if outer == "NOT_X":
        return BLOCK_COMPLEMENT[left]
    if outer == "NOT_Y":
        return BLOCK_COMPLEMENT[right]
    raise ValueError(f"Unknown outer block: {outer}")


def compose_operation(
    outer: BeranOperation,
    left: BeranOperation,
    right: BeranOperation,
    pair_to_id: dict[tuple[str, str], int],
) -> int:
    block = compose_block(outer.block, left.block, right.block)
    shadow = compose_shadow(outer.shadow, left.shadow, right.shadow)
    return pair_to_id[(block, shadow)]
