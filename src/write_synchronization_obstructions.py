from __future__ import annotations

import csv

from beran_core import LOGS_DIR, load_beran96
from table_tools import elements_to_string, string_to_elements


def main() -> None:
    operations = {op.beran_id: op for op in load_beran96()}

    input_path = LOGS_DIR / "maximal_obstructions.csv"
    output_path = LOGS_DIR / "synchronization_obstructions.csv"

    rows = []
    with input_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["type"] != "synchronization":
                continue

            elements = string_to_elements(row["elements"])

            fibers: dict[str, set[str]] = {}
            for i in elements:
                op = operations[i]
                fibers.setdefault(op.block, set()).add(op.shadow)

            fiber_text = []
            for block in ["ZERO", "X", "Y", "NOT_Y", "NOT_X", "ONE"]:
                shadows = " ".join(sorted(fibers.get(block, set())))
                fiber_text.append(f"{block}: {shadows}")

            rows.append({
                "obstruction_id": row["obstruction_id"],
                "source_closed_id": row["source_closed_id"],
                "size": row["size"],
                "contains_x": row["contains_x"],
                "contains_y": row["contains_y"],
                "block_count": row["block_count"],
                "shadow_count": row["shadow_count"],
                "fibers": " | ".join(fiber_text),
                "elements": elements_to_string(elements),
            })

    with output_path.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "obstruction_id",
            "source_closed_id",
            "size",
            "contains_x",
            "contains_y",
            "block_count",
            "shadow_count",
            "fibers",
            "elements",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {output_path}")
    print(f"Synchronization obstructions: {len(rows)}")


if __name__ == "__main__":
    main()
