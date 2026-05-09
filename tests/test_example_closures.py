from closure_tools import closure_of, contains_projections


def test_nand_basis_generates_all_96():
    assert len(closure_of(contains_projections([15]))) == 96


def test_complete_binary_basis_generates_all_96():
    assert len(closure_of(contains_projections([63, 69, 78, 95]))) == 96


def test_meet_basis_is_not_full():
    assert len(closure_of(contains_projections([2]))) < 96
