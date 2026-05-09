from __future__ import annotations

import csv

from beran_core import LOGS_DIR


def main() -> None:
    LOGS_DIR.mkdir(exist_ok=True)

    s_mid = set(range(1, 17)) | {27, 42, 55, 70} | set(range(81, 97))
    s_mid_with_projections = set(s_mid) | {22, 39}

    output_path = LOGS_DIR / "example_smid_beran_numbers.csv"
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["set_name", "beran_numbers", "size"])
        writer.writerow(["S_mid", " ".join(str(x) for x in sorted(s_mid)), len(s_mid)])
        writer.writerow([
            "S_mid_with_projections",
            " ".join(str(x) for x in sorted(s_mid_with_projections)),
            len(s_mid_with_projections),
        ])

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
