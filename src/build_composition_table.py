from __future__ import annotations

import csv

from beran_core import LOGS_DIR, compose_operation, load_beran96, operation_index


def main() -> None:
    LOGS_DIR.mkdir(exist_ok=True)

    operations = load_beran96()
    pair_to_id = operation_index(operations)

    output_path = LOGS_DIR / "beran_composition_table.csv"
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["outer", "left", "right", "result"])
        for outer in operations:
            for left in operations:
                for right in operations:
                    result = compose_operation(outer, left, right, pair_to_id)
                    writer.writerow([outer.beran_id, left.beran_id, right.beran_id, result])

    print(f"Wrote {output_path}")
    print("Rows:", 96 * 96 * 96)


if __name__ == "__main__":
    main()
