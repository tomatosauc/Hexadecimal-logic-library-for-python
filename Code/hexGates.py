class Gate:
    gateOutputs = {}
    gateInputs = {}
    values = {}
    gates = {}

    def __init__(self, gateType: str, gateFunc: str, gateId: int, inputIDs: list, outputIDs: list,
                 savefile: str = 'savedGates.dat'):
        self.savefile = savefile
        self.gateType = gateType
        self.gateId = gateId
        self.inputValues = {}
        self.outputValues = {}
        with open(self.savefile, 'r') as savefile:
            saved = False
            for line in savefile:
                if self.gateType in line.split('-', 1)[0]:
                    self.func = line.split('-')[1].split(',')[0]
                    ins = int(line.split(',')[1])
                    outs = int(line.split(',')[2])
                    saved = True
                    break
            if not saved:
                self.func = gateFunc
                ins = len(inputIDs)
                outs = len(outputIDs)
        if ins == len(inputIDs) and outs == len(outputIDs):
            self.inputIDs = inputIDs
            self.outputIDs = outputIDs
        else:
            exception = ValueError(
                f'Invalid number of {'inputs and outputs' if ins != len(inputIDs) and outs != len(outputIDs) else 'inputs' if ins != len(inputIDs) else 'outputs'}')
            raise exception
        self.gates.update({self.gateId: self})
        for i in self.inputIDs:
            self.inputValues.update({i: 0})
            if i not in self.gateInputs:
                self.gateInputs.update({i: [self.gateId]})
            else:
                if self.gateId not in self.gateInputs[i]:
                    self.gateInputs[i].append(self.gateId)
        for i in self.outputIDs:
            self.gateOutputs.update({i: self.gateId})
        self.updateGateValues([], [])

    def updateID(self, oldInputIDs: list, oldOutputIDs: list, inputIDs: list, outputIDs: list):
        for inputID in oldInputIDs:
            if inputID in self.inputIDs:
                self.inputIDs[self.inputIDs.index(inputID)] = inputIDs[oldInputIDs.index(inputID)]
                inputs = self.gateInputs[inputID].remove(self.gateId)
                if inputs is not None:
                    self.gateInputs.update({inputID: inputs})
                else:
                    self.gateInputs.pop(inputID)
                if inputIDs[oldInputIDs.index(inputID)] not in self.gateInputs:
                    self.gateInputs.update({inputIDs[oldInputIDs.index(inputID)]: [self.gateId]})
                else:
                    if self.gateId not in self.gateInputs[inputIDs[oldInputIDs.index(inputID)]]:
                        self.gateInputs[inputIDs[oldInputIDs.index(inputID)]].append(self.gateId)
                self.inputValues.pop(inputID)
                self.inputValues.update({inputIDs[oldInputIDs.index(inputID)]: 0})
                if inputIDs[oldInputIDs.index(inputID)] in self.values:
                    self.updateGateValues(inputIDs[oldInputIDs.index(inputID)], self.values[inputIDs[oldInputIDs.index(inputID)]])
                else:
                    self.updateGateValues(inputIDs[oldInputIDs.index(inputID)], 0)
        for outputID in oldOutputIDs:
            if outputID in self.outputIDs:
                self.outputIDs[self.outputIDs.index(outputID)] = outputIDs[oldOutputIDs.index(outputID)]
                self.gateOutputs.pop(outputID)
                if outputIDs[oldOutputIDs.index(outputID)] not in self.gateOutputs:
                    self.gateOutputs.update({outputIDs[oldOutputIDs.index(outputID)]: [self.gateId]})
                else:
                    if self.gateId not in self.gateOutputs[outputIDs[oldOutputIDs.index(outputID)]]:
                        self.gateOutputs[outputIDs[oldOutputIDs.index(outputID)]].append(self.gateId)
                temp = self.outputValues[outputID]
                self.outputValues.pop(outputID)
                self.outputValues.update({outputIDs[oldOutputIDs.index(outputID)]: temp})
                updateCircuit(outputID, 0)
                updateCircuit(outputIDs[oldOutputIDs.index(outputID)], temp)

    def updateGateValues(self, Input: int, value: int):
        if Input in self.inputIDs:
            self.inputValues.update({Input: value})
        inputs = []
        for inputID in self.inputIDs:
            inputs.append(self.inputValues[inputID])
        if type(eval(self.func)) == type(compare):
            out = (eval(self.func)(inputs),)
        else:
            out = (eval(self.func),)
        i = 0
        for output in self.outputIDs:
            if output in self.outputValues:
                temp = self.outputValues[output]
            else:
                temp = None
            self.outputValues.update({output: out[i]})
            if self.outputValues[output] != temp:
                updateCircuit(output, self.outputValues[output])
            i += 1

    def save(self):
        with open(self.savefile, 'r') as r:
            savedGates = []
            for line in r:
                savedGates.append(line)
            with open(self.savefile, 'w') as w:
                for line in savedGates:
                    if self.gateType not in line.strip().split('-', 1)[0]:
                        w.write(line)
                w.write(self.gateType + '-' + str(self.func) + ', ' + str(len(self.inputIDs)) + ',' + str(
                    len(self.outputIDs)) + '\n')

    def destroy(self):
        for i in self.inputIDs:
            if i in self.gateInputs:
                self.gateInputs[i].remove(self.gateId)
        for i in self.outputIDs:
            if i in self.gateOutputs:
                self.gateOutputs.pop(i)
            updateCircuit(i, 0)
        self.gates.pop(self.gateId)

    @staticmethod
    def clean():
        for gateID in Gate.gates.copy():
            Gate.gates[gateID].destroy()


def compare(inputs: list):
    return inputs[0] if inputs[0] >= inputs[1] else 0


def subtract(inputs: list):
    return inputs[0] - inputs[1] if inputs[0] - inputs[1] >= 0 else 0


def repeat(inputs: list):
    return 15 if inputs[0] > 0 else 0


def partialNOT(inputs: list):
    return 15 if inputs[0] == 0 else 0


def NOT(inputs: list):
    return subtract([15, inputs[0]]) if 15 - inputs[0] >= 0 else 0


def weightedOR(inputs: list):
    return OR([inputs[0], subtract([inputs[1], repeat([inputs[0]])])])


def OR(inputs: list):
    return inputs[0] if inputs[0] >= inputs[1] else inputs[1]


def XOR(inputs: list):
    return OR([subtract([compare([inputs[0]], inputs[1]), inputs[1]]),
               subtract([compare([inputs[1], inputs[0]]), inputs[0]])])


def AND0(inputs: list):
    return repeat([subtract([inputs[1], NOT([inputs[0]])])])


def AND15(inputs: list):
    return AND0([compare([inputs[0], 15]), compare([inputs[1], 15])])


def AND(inputs: list):
    return subtract([OR([inputs[0], inputs[1]]), NOT([AND0([inputs[0], inputs[1]])])])


def XNOR(inputs: list):
    return partialNOT([OR([subtract([inputs[0], inputs[1]]), subtract([inputs[1], inputs[0]])])])


def XAND(inputs: list):
    return AND([compare([inputs[0], inputs[1]]), compare([inputs[1], inputs[0]])])


def halfAdder(inputs: list):
    B = compare([inputs[0], NOT([subtract([inputs[1], 1])])])
    C = compare([subtract([inputs[0], 1]), NOT([inputs[1]])])
    D = subtract([B, AND0([inputs[0], subtract([inputs[0], 1])])])
    E = OR([C, D])
    F = subtract([inputs[0], repeat([E])])
    G = NOT([subtract([inputs[1], repeat([E])])])
    H = NOT([subtract([G, F])])
    L = subtract([inputs[0], partialNOT([E])])
    J = subtract([L, NOT([inputs[1]])])
    K = subtract([J, 1])
    Sum = OR([H, K])
    Cout = subtract([J, K])
    return Sum, Cout


def fullAdder(inputs: list):
    # 0 - A, 1 - B, 2 - Cin
    out, cout1 = halfAdder([inputs[0], inputs[1]])
    Sum, cout2 = halfAdder([inputs[2], out])
    return Sum, NOT([subtract([NOT([cout1]), cout2])])


def updateCircuit(connection: int, value: int):
    Gate.values.update({connection: value})
    if connection in Gate.gateInputs:
        for gate in Gate.gateInputs[connection]:
            Gate.gates[gate].updateGateValues(connection, value)


class Chip:
    chips = [0]
    chipList = {}

    def __init__(self, name: str, inputIDs: list, outputIDs: list, savefile: str = 'savedCircuits.dat', gates=None):
        self.name = name
        self.gates = []
        self.savefile = savefile
        self.id = self.chips[len(self.chips) - 1] + 1
        self.chips.append(self.id)
        self.inputIDs = inputIDs
        self.outputIDs = outputIDs
        with open(self.savefile, 'r') as savefile:
            saved = False
            lines = []
            for line in savefile:
                lines += line
            for line in lines:
                if line.startswith(self.name):
                    oldInputIDs = eval(line.split("-")[1])
                    oldOutputIDs = eval(line.split("-")[2])
                    lineID = lines.index(line) + 1
                    for i in lines[lineID:]:
                        if i.startswith(' - '):
                            i = i[3:]
                            ids = []
                            for ID in Gate.gates:
                                ids.append(ID)
                            ids.sort(reverse=True)
                            NextID = ids[0] + 1
                            inputIDs = eval(i.split('-')[2])
                            outputIDs = eval(i.split('-')[3])
                            inputID = []
                            outputID = []
                            for ID in inputIDs:
                                if ID in oldInputIDs:
                                    inputID.append(inputIDs[oldInputIDs.index(ID)])
                                else:
                                    inputID.append(int(ID) + self.id * 10000)
                            for ID in outputIDs:
                                if ID in oldOutputIDs:
                                    outputID.append(outputIDs[oldOutputIDs.index(ID)])
                                else:
                                    outputID.append(int(ID) + self.id * 10000)
                            Gate(i.split('-')[0], i.split('-')[1], NextID, inputID, outputID)
                            self.gates.append(NextID)
                        else:
                            break
                    saved = True
                    break
            if not saved:
                for gateID in Gate.gates:
                    if gates is None or gateID in gates:
                        self.gates.append(gateID)
                        gate = Gate.gates[gateID]
                        for inputID in gate.inputIDs:
                            if inputID not in inputIDs and inputID not in outputIDs:
                                newInputID = inputID + self.id * 10000
                                gate.updateID([inputID], [], [newInputID], [])
                        for outputID in gate.outputIDs:
                            if outputID not in outputIDs:
                                newOutputID = outputID + self.id * 10000
                                gate.updateID([], [outputID], [], [newOutputID])
        self.chipList.update({self.id: self})

    def save(self):
        with open(self.savefile, 'r') as r:
            savedGates = []
            for line in r:
                savedGates.append(line)
            with open(self.savefile, 'w') as w:
                for line in savedGates:
                    replace = False
                    if not (line.startswith(self.name) and replace):
                        w.write(line)
                    elif line.startswith(self.name) or line.startswith(" - "):
                        replace = True
                    else:
                        w.write(line)
                        replace = False
                w.write(f'{self.name}-{self.inputIDs}-{self.outputIDs}')
                for gate in self.gates:
                    gate = Gate.gates[gate]
                    inputIDs = []
                    for inputID in gate.inputIDs:
                        inputIDs.append(inputID % (self.id * 10000))
                    outputIDs = []
                    for outputID in gate.outputIDs:
                        outputIDs.append(outputID % (self.id * 10000))
                    w.write(f'\n - {gate.gateType}-{gate.func}-{inputIDs}-{outputIDs}')

# Compare = Gate('compare', 'compare', 0, [0, 1], [0])

# And0 = Gate('And0', 'inputs[0] - inputs[1] if inputs[0] - inputs[1] >= 0 else 0', 1, [0,1], [2])
