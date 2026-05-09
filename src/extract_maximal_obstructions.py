from __future__ import annotations

import csv

from beran_core import LOGS_DIR, load_beran96
from table_tools import elements_to_string, string_to_elements


UNIVERSE = frozenset(range(1, 97))
X_ID = 22
Y_ID = 39


def to_mask(elements: frozenset[int]) -> int:
    mask = 0
    for x in elements:
        mask |= 1 << (x - 1)
    return mask


def is_subset_mask(a: int, b: int) -> bool:
    return (a & ~b) == 0


def classify_obstruction(elements: frozenset[int], operations: dict[int, object]) -> str:
    blocks = {operations[i].block for i in elements}
    shadows = {operations[i].shadow for i in elements}

    if len(blocks) < 6:
        return "block"
    if len(shadows) < 16:
        return "shadow"
    return "synchronization"


def main() -> None:
    operations = {op.beran_id: op for op in load_beran96()}

    input_path = LOGS_DIR / "closed_subalgebras.csv"
    maximal_path = LOGS_DIR / "maximal_obstructions.csv"
    projection_path = LOGS_DIR / "projection_obstructions.csv"

    closed_rows = []
    with input_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            elements = string_to_elements(row["elements"])
            if elements == UNIVERSE:
                continue
            closed_rows.append({
                "closed_id": row["closed_id"],
                "elements": elements,
                "size": len(elements),
                "mask": to_mask(elements),
            })

    closed_rows.sort(key=lambda r: r["size"], reverse=True)

    maximal_rows = []
    for row in closed_rows:
        mask = row["mask"]
        if any(is_subset_mask(mask, m["mask"]) for m in maximal_rows):
            continue
        maximal_rows.append(row)

    output_rows = []
    for idx, row in enumerate(maximal_rows, start=1):
        elements = row["elements"]
        blocks = {operations[i].block for i in elements}
        shadows = {operations[i].shadow for i in elements}
        obstruction_type = classify_obstruction(elements, operations)
        output_rows.append({
            "obstruction_id": f"M{idx}",
            "source_closed_id": row["closed_id"],
            "type": obstruction_type,
            "size": len(elements),
            "contains_x": X_ID in elements,
            "contains_y": Y_ID in elements,
            "block_count": len(blocks),
            "shadow_count": len(shadows),
            "elements": elements_to_string(elements),
        })

    with maximal_path.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "obstruction_id",
            "source_closed_id",
            "type",
            "size",
            "contains_x",
            "contains_y",
            "block_count",
            "shadow_count",
            "elements",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    projection_rows = [
        row for row in output_rows
        if row["contains_x"] is True and row["contains_y"] is True
    ]

    with projection_path.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "obstruction_id",
            "source_closed_id",
            "type",
            "size",
            "contains_x",
            "contains_y",
            "block_count",
            "shadow_count",
            "elements",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(projection_rows)

    type_counts = {}
    for row in output_rows:
        type_counts[row["type"]] = type_counts.get(row["type"], 0) + 1

    projection_type_counts = {}
    for row in projection_rows:
        projection_type_counts[row["type"]] = projection_type_counts.get(row["type"], 0) + 1

    print(f"Wrote {maximal_path}")
    print(f"Wrote {projection_path}")
    print("Maximal obstructions:", len(output_rows), type_counts)
    print("Projection containing obstructions:", len(projection_rows), projection_type_counts)


if __name__ == "__main__":
    main()
