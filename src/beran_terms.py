from __future__ import annotations

from dataclasses import dataclass
from functools import reduce


@dataclass(frozen=True)
class Expr:
    op: str
    args: tuple["Expr", ...] = ()


def V(name: str) -> Expr:
    return Expr(name)


def Z() -> Expr:
    return Expr("0")


def O() -> Expr:
    return Expr("1")


def N(a: Expr) -> Expr:
    return Expr("not", (a,))


def M(a: Expr, b: Expr) -> Expr:
    return Expr("meet", (a, b))


def J(a: Expr, b: Expr) -> Expr:
    return Expr("join", (a, b))


def MM(*args: Expr) -> Expr:
    return reduce(M, args)


def JJ(*args: Expr) -> Expr:
    return reduce(J, args)


x = V("x")
y = V("y")
nx = N(x)
ny = N(y)

xy = M(x, y)
xny = M(x, ny)
nxy = M(nx, y)
nxny = M(nx, ny)

TERMS: dict[int, Expr] = {}

TERMS[1] = Z()
TERMS[2] = xy
TERMS[3] = xny
TERMS[4] = nxy
TERMS[5] = nxny
TERMS[6] = J(xy, xny)
TERMS[7] = J(xy, nxy)
TERMS[8] = J(xy, nxny)
TERMS[9] = J(xny, nxy)
TERMS[10] = J(nxny, xny)
TERMS[11] = J(nxny, nxy)
TERMS[12] = JJ(xy, xny, nxy)
TERMS[13] = JJ(xy, xny, nxny)
TERMS[14] = JJ(xy, nxy, nxny)
TERMS[15] = JJ(xny, nxy, nxny)
TERMS[16] = JJ(xy, xny, nxy, nxny)

TERMS[17] = MM(x, J(nx, y), J(nx, ny))
TERMS[18] = M(x, J(nx, y))
TERMS[19] = M(x, J(nx, ny))
TERMS[20] = J(nxy, MM(x, J(nx, y), J(nx, ny)))
TERMS[21] = J(nxny, MM(x, J(nx, y), J(nx, ny)))
TERMS[22] = x
TERMS[23] = M(J(nx, y), J(x, M(nx, y)))
TERMS[24] = M(J(nx, y), J(x, M(nx, ny)))
TERMS[25] = M(J(nx, ny), J(x, M(nx, y)))
TERMS[26] = M(J(nx, ny), J(x, M(nx, ny)))
TERMS[27] = MM(J(nx, ny), J(nx, y), J(x, J(M(nx, y), M(nx, ny))))
TERMS[28] = J(x, M(nx, y))
TERMS[29] = J(x, M(nx, ny))
TERMS[30] = M(J(nx, y), J(x, J(M(nx, y), M(nx, ny))))
TERMS[31] = M(J(nx, ny), J(x, J(M(nx, y), M(nx, ny))))
TERMS[32] = J(x, J(M(nx, y), M(nx, ny)))

TERMS[33] = MM(y, J(x, ny), J(nx, ny))
TERMS[34] = M(y, J(x, ny))
TERMS[35] = J(xny, MM(y, J(x, ny), J(nx, ny)))
TERMS[36] = M(y, J(nx, ny))
TERMS[37] = J(nxny, MM(y, J(x, ny), J(nx, ny)))
TERMS[38] = M(J(x, ny), J(y, M(x, ny)))
TERMS[39] = y
TERMS[40] = M(J(x, ny), J(y, M(nx, ny)))
TERMS[41] = M(J(nx, ny), J(y, M(x, ny)))
TERMS[42] = MM(J(nx, ny), J(x, ny), J(y, J(M(x, ny), M(nx, ny))))
TERMS[43] = M(J(nx, ny), J(y, M(nx, ny)))
TERMS[44] = J(y, M(x, ny))
TERMS[45] = M(J(x, ny), J(y, J(M(x, ny), M(nx, ny))))
TERMS[46] = J(y, M(nx, ny))
TERMS[47] = M(J(nx, ny), J(y, J(M(x, ny), M(nx, ny))))
TERMS[48] = J(y, J(M(x, ny), M(nx, ny)))

TERMS[49] = MM(ny, J(x, y), J(nx, y))
TERMS[50] = J(xy, MM(ny, J(x, y), J(nx, y)))
TERMS[51] = M(ny, J(x, y))
TERMS[52] = J(nxy, MM(ny, J(x, y), J(nx, y)))
TERMS[53] = M(ny, J(nx, y))
TERMS[54] = M(J(x, y), J(ny, M(x, y)))
TERMS[55] = MM(J(x, y), J(nx, y), J(ny, J(M(x, y), M(nx, y))))
TERMS[56] = M(J(nx, y), J(ny, M(x, y)))
TERMS[57] = M(J(x, y), J(ny, M(nx, y)))
TERMS[58] = ny
TERMS[59] = M(J(nx, y), J(ny, M(nx, y)))
TERMS[60] = M(J(x, y), J(ny, J(M(x, y), M(nx, y))))
TERMS[61] = J(ny, M(x, y))
TERMS[62] = M(J(nx, y), J(ny, J(M(x, y), M(nx, y))))
TERMS[63] = J(ny, M(nx, y))
TERMS[64] = J(ny, J(M(x, y), M(nx, y)))

TERMS[65] = MM(nx, J(x, y), J(x, ny))
TERMS[66] = J(xy, MM(nx, J(x, y), J(x, ny)))
TERMS[67] = J(xny, MM(nx, J(x, y), J(x, ny)))
TERMS[68] = M(nx, J(x, y))
TERMS[69] = M(nx, J(x, ny))
TERMS[70] = MM(J(x, y), J(x, ny), J(nx, J(M(x, y), M(x, ny))))
TERMS[71] = M(J(x, y), J(nx, M(x, y)))
TERMS[72] = M(J(x, ny), J(nx, M(x, y)))
TERMS[73] = M(J(x, y), J(nx, M(x, ny)))
TERMS[74] = M(J(x, ny), J(nx, M(x, ny)))
TERMS[75] = nx
TERMS[76] = M(J(x, y), J(nx, J(M(x, y), M(x, ny))))
TERMS[77] = M(J(x, ny), J(nx, J(M(x, y), M(x, ny))))
TERMS[78] = J(nx, M(x, y))
TERMS[79] = J(nx, M(x, ny))
TERMS[80] = J(nx, J(M(x, y), M(x, ny)))

TERMS[81] = MM(J(x, y), J(x, ny), J(nx, y), J(nx, ny))
TERMS[82] = MM(J(x, y), J(x, ny), J(nx, y))
TERMS[83] = MM(J(x, y), J(x, ny), J(nx, ny))
TERMS[84] = MM(J(x, y), J(nx, y), J(nx, ny))
TERMS[85] = MM(J(x, ny), J(nx, y), J(nx, ny))
TERMS[86] = M(J(x, y), J(x, ny))
TERMS[87] = M(J(x, y), J(nx, y))
TERMS[88] = M(J(x, ny), J(nx, y))
TERMS[89] = M(J(x, y), J(nx, ny))
TERMS[90] = M(J(x, ny), J(nx, ny))
TERMS[91] = M(J(nx, y), J(nx, ny))
TERMS[92] = J(x, y)
TERMS[93] = J(x, ny)
TERMS[94] = J(nx, y)
TERMS[95] = J(nx, ny)
TERMS[96] = O()


BLOCK_COMPLEMENT = {
    "ZERO": "ONE",
    "ONE": "ZERO",
    "X": "NOT_X",
    "NOT_X": "X",
    "Y": "NOT_Y",
    "NOT_Y": "Y",
}


def block_meet(a: str, b: str) -> str:
    if a == "ZERO" or b == "ZERO":
        return "ZERO"
    if a == "ONE":
        return b
    if b == "ONE":
        return a
    if a == b:
        return a
    return "ZERO"


def block_join(a: str, b: str) -> str:
    if a == "ONE" or b == "ONE":
        return "ONE"
    if a == "ZERO":
        return b
    if b == "ZERO":
        return a
    if a == b:
        return a
    return "ONE"


def eval_block(expr: Expr, x_value: str, y_value: str) -> str:
    if expr.op == "x":
        return x_value
    if expr.op == "y":
        return y_value
    if expr.op == "0":
        return "ZERO"
    if expr.op == "1":
        return "ONE"
    if expr.op == "not":
        return BLOCK_COMPLEMENT[eval_block(expr.args[0], x_value, y_value)]
    if expr.op == "meet":
        return block_meet(eval_block(expr.args[0], x_value, y_value), eval_block(expr.args[1], x_value, y_value))
    if expr.op == "join":
        return block_join(eval_block(expr.args[0], x_value, y_value), eval_block(expr.args[1], x_value, y_value))
    raise ValueError(f"Unknown expression operation: {expr.op}")


def validate_terms() -> None:
    if set(TERMS) != set(range(1, 97)):
        raise ValueError("TERMS must contain exactly Beran IDs 1 through 96.")
