from __future__ import annotations

import csv
from collections import Counter

from beran_core import LOGS_DIR


def read_csv(name: str) -> list[dict[str, str]]:
    with (LOGS_DIR / name).open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    closed = read_csv("closed_subalgebras.csv")
    maximal = read_csv("maximal_obstructions.csv")
    projection = read_csv("projection_obstructions.csv")
    synchronization = [row for row in maximal if row["type"] == "synchronization"]

    maximal_counts = Counter(row["type"] for row in maximal)
    projection_counts = Counter(row["type"] for row in projection)

    output_path = LOGS_DIR / "verification_summary.csv"
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["quantity", "value"])
        writer.writerow(["closed_subalgebras", len(closed)])
        writer.writerow(["maximal_obstructions_total", len(maximal)])
        writer.writerow(["maximal_block_obstructions", maximal_counts["block"]])
        writer.writerow(["maximal_shadow_obstructions", maximal_counts["shadow"]])
        writer.writerow(["maximal_synchronization_obstructions", maximal_counts["synchronization"]])
        writer.writerow(["projection_obstructions_total", len(projection)])
        writer.writerow(["projection_block_obstructions", projection_counts["block"]])
        writer.writerow(["projection_shadow_obstructions", projection_counts["shadow"]])
        writer.writerow(["projection_synchronization_obstructions", projection_counts["synchronization"]])
        writer.writerow(["synchronization_obstructions_total", len(synchronization)])

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
