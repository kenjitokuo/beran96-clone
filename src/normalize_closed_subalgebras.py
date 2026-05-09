from __future__ import annotations

import csv

from beran_core import LOGS_DIR, load_beran96
from table_tools import elements_to_string, string_to_elements


X_ID = 22
Y_ID = 39


def main() -> None:
    operations = {op.beran_id: op for op in load_beran96()}

    input_path = LOGS_DIR / "beran_closed_algebras_with_minimum_generator_summary.csv"
    output_path = LOGS_DIR / "closed_subalgebras.csv"

    rows = []
    with input_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            elements = string_to_elements(row["elements"])
            blocks = {operations[i].block for i in elements}
            shadows = {operations[i].shadow for i in elements}
            rows.append({
                "closed_id": int(row["algebra_id"]),
                "size": len(elements),
                "contains_x": X_ID in elements,
                "contains_y": Y_ID in elements,
                "block_count": len(blocks),
                "shadow_count": len(shadows),
                "rank": row.get("rank", ""),
                "num_minimum_generating_sets": row.get("num_minimum_generating_sets", ""),
                "first_minimum_generators": row.get("first_minimum_generators", ""),
                "elements": elements_to_string(elements),
            })

    rows.sort(key=lambda r: (int(r["size"]), r["closed_id"]))

    with output_path.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "closed_id",
            "size",
            "contains_x",
            "contains_y",
            "block_count",
            "shadow_count",
            "rank",
            "num_minimum_generating_sets",
            "first_minimum_generators",
            "elements",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {output_path}")
    print(f"Closed subalgebras: {len(rows)}")


if __name__ == "__main__":
    main()
