import csv
from pathlib import Path
from collections import Counter


ROOT = Path(__file__).resolve().parents[1]
LOGS = ROOT / "logs"


def read_csv(name):
    with (LOGS / name).open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def test_maximal_obstruction_counts():
    rows = read_csv("maximal_obstructions.csv")
    assert len(rows) == 17
    assert Counter(row["type"] for row in rows) == {
        "block": 4,
        "shadow": 10,
        "synchronization": 3,
    }


def test_projection_obstruction_counts():
    rows = read_csv("projection_obstructions.csv")
    assert len(rows) == 9
    assert Counter(row["type"] for row in rows) == {
        "block": 2,
        "shadow": 4,
        "synchronization": 3,
    }
    assert all(row["contains_x"] == "True" for row in rows)
    assert all(row["contains_y"] == "True" for row in rows)


def test_closed_subalgebra_count():
    rows = read_csv("closed_subalgebras.csv")
    assert len(rows) == 21748
