def compare(A, B):
    return A if A >= B else 0


def subtract(A, B):
    return A - B if A - B >= 0 else 0


def repeat(A):
    return 15 if A > 0 else 0


def partialNOT(A):
    return 15 if A == 0 else 0


def NOT(A):
    return subtract(15, A) if 15 - A >= 0 else 0


def OR(A, B):
    return A if A >= B else B


def XOR(A, B):
    return OR(subtract(compare(A, B), B), subtract(compare(B, A), A))


def AND0(A, B):
    return repeat(subtract(B, NOT(A)))


def AND15(A, B):
    return AND0(compare(A, 15), compare(B, 15))


def AND(A, B):
    return subtract(OR(A, B), NOT(AND0(A, B)))


def XNOR(A, B):
    return partialNOT(OR(subtract(A, B), subtract(B, A)))


def XAND(A, B):
    return AND(compare(A, B), compare(B, A))


def halfAdder(A, Cin):
    B = compare(A, NOT(subtract(Cin, 1)))
    C = compare(subtract(A, 1), NOT(Cin))
    D = subtract(B, AND0(A, subtract(A, 1)))
    E = OR(C, D)
    F = subtract(A, repeat(E))
    G = NOT(subtract(Cin, repeat(E)))
    H = NOT(subtract(G, F))
    I = subtract(A, partialNOT(E))
    J = subtract(I, NOT(Cin))
    K = subtract(J, 1)
    Sum = OR(H, K)
    Cout = subtract(J, K)
    return Sum, Cout


def halfAdderTest():
    for A in range(16):
        for B in range(16):
            Sum, Cout = halfAdder(A, B)
            if len(hex(A + B)) > 3:
                if hex(Sum)[2] == hex(A + B)[3] and hex(Cout)[2] == hex(A + B)[2]:
                    continue
                else:
                    print(
                        f'Half adder for {A} and {B} broke.\nExpected: {hex(A + B)[2]}{hex(A + B)[3]}, Actual: {hex(Cout)[2]}{hex(Sum)[2]}')
                    break
            else:
                if hex(Sum)[2] == hex(A + B)[2]:
                    continue
                else:
                    print(
                        f'Half adder for {A} and {B} broke.\nExpected: 0{hex(A + B)[2]}, Actual: {hex(Cout)[2]}{hex(Sum)[2]}')
                    break


def fullAdder(A, B, Cin):
    out, cout1 = halfAdder(A, B)
    Sum, cout2 = halfAdder(Cin, out)
    return Sum, NOT(subtract(NOT(cout1), cout2))


def fullAdderTest():
    for A in range(16):
        for B in range(16):
            for Cin in range(16):
                Sum, Cout = fullAdder(A, B, Cin)
                if len(hex(A + B + Cin)) > 3:
                    if hex(Sum)[2] == hex(A + B + Cin)[3] and hex(Cout)[2] == hex(A + B + Cin)[2]:
                        continue
                    else:
                        print(
                            f'Half adder for {A}, {B} and {Cin} broke.\nExpected: {hex(A + B + Cin)[2:]}, Actual: {hex(Cout)[2]}{hex(Sum)[2]}')
                        break
                else:
                    if hex(Sum)[2] == hex(A + B + Cin)[2]:
                        continue
                    else:
                        print(
                            f'Half adder for {A}, {B} and {Cin} broke.\nExpected: 0{hex(A + B + Cin)[2]}, Actual: {hex(Cout)[2]}{hex(Sum)[2]}')
                        break


def chainFullAdderTest():
    for A2 in range(16):
        for B2 in range(16):
            for A1 in range(16):
                for B1 in range(16):
                    Sum1, Cout1 = fullAdder(A1, B1, 0)
                    Sum2, Cout = fullAdder(A2, B2, Cout1)
                    RealSum = hex(A1 + B1 + 16 * (A2 + B2))
                    if len(RealSum) == 5:
                        if hex(Sum1)[2] == RealSum[4] and hex(Sum2)[2] == RealSum[3] and hex(Cout)[2] == RealSum[2]:
                            continue
                        else:
                            print(f'Full adder for {hex(A2)[2:]}{hex(A1)[2:]} and {hex(B2)[2:]}{hex(B1)[2:]} broke.\nExpected: {RealSum}[2:], Actual: {hex(Cout)[2]}{hex(Sum2)[2]}{hex(Sum1)[2]}')
                            quit(1)
                    elif len(RealSum) == 4:
                        if hex(Sum1)[2] == RealSum[3] and hex(Sum2)[2] == RealSum[2]:
                            continue
                        else:
                            print(f'Full adder for {hex(A2)[2:]}{hex(A1)[2:]} and {hex(B2)[2:]}{hex(B1)[2:]} broke.\nExpected: {RealSum}[2:], Actual: {hex(Cout)[2]}{hex(Sum2)[2]}{hex(Sum1)[2]}')
                            quit(1)
                    else:
                        if hex(Sum1)[2] == RealSum[2]:
                            continue
                        else:
                            print(f'Full adder for {hex(A2)[2:]}{hex(A1)[2:]} and {hex(B2)[2:]}{hex(B1)[2:]} broke.\nExpected: {RealSum}[2:], Actual: {hex(Cout)[2]}{hex(Sum2)[2]}{hex(Sum1)[2]}')
                            quit(1)
