from __future__ import annotations

import csv

from beran_core import LOGS_DIR
from closure_tools import closure_of, contains_projections


EXAMPLES = [
    ("nand_basis", [15], True),
    ("complete_binary_basis", [63, 69, 78, 95], True),
    ("shadow_meet_basis", [2], True),
]


def main() -> None:
    LOGS_DIR.mkdir(exist_ok=True)

    output_path = LOGS_DIR / "example_basis_closures.csv"
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "generators", "with_projections", "closure_size", "is_full"])
        for name, generators, add_projections in EXAMPLES:
            gens = contains_projections(generators) if add_projections else set(generators)
            closure = closure_of(gens)
            writer.writerow([
                name,
                " ".join(str(x) for x in sorted(gens)),
                add_projections,
                len(closure),
                len(closure) == 96,
            ])

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
