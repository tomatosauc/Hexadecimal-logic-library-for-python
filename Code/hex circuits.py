ins = {0:[0], 1:[2]}
'''
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
                            print(
                                f'Full adder for {hex(A2)[2:]}{hex(A1)[2:]} and {hex(B2)[2:]}{hex(B1)[2:]} broke.\nExpected: {RealSum}[2:], Actual: {hex(Cout)[2]}{hex(Sum2)[2]}{hex(Sum1)[2]}')
                            quit(1)
                    elif len(RealSum) == 4:
                        if hex(Sum1)[2] == RealSum[3] and hex(Sum2)[2] == RealSum[2]:
                            continue
                        else:
                            print(
                                f'Full adder for {hex(A2)[2:]}{hex(A1)[2:]} and {hex(B2)[2:]}{hex(B1)[2:]} broke.\nExpected: {RealSum}[2:], Actual: {hex(Cout)[2]}{hex(Sum2)[2]}{hex(Sum1)[2]}')
                            quit(1)
                    else:
                        if hex(Sum1)[2] == RealSum[2]:
                            continue
                        else:
                            print(
                                f'Full adder for {hex(A2)[2:]}{hex(A1)[2:]} and {hex(B2)[2:]}{hex(B1)[2:]} broke.\nExpected: {RealSum}[2:], Actual: {hex(Cout)[2]}{hex(Sum2)[2]}{hex(Sum1)[2]}')
                            quit(1)
'''