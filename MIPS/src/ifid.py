import unittest
from cpuElement import CPUElement
from testElement import TestElement

class IFID(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 8), 'IF/ID should have eight input'
        assert(len(outputValueNames) == 8), 'IF/ID has eight output'
        assert(len(control) == 0), 'IF/ID does not have any control signal'
        assert(len(outputSignalNames) == 0), 'IF/ID does not have any control output'

        self.adder = inputSources[0][1]    # Incremented next address
        self.inst1 = inputSources[1][1]    # 31-26 part of instruction
        self.inst2 = inputSources[2][1]    # 25-21 part of instruction
        self.inst3 = inputSources[3][1]    # 20-15 part of instruction
        self.inst4 = inputSources[4][1]    # 15-11 part of instruction
        self.inst5 = inputSources[5][1]    # 15-0 part of instruction
        self.inst6 = inputSources[6][1]    # 5-0 part of instruction
        self.inst7 = inputSources[7][1]    # 26-0 part of instruction


    def writeOutput(self):
        self.outputValues[self.adder] = self.inputValues.get(self.adder, 0)
        self.outputValues[self.inst1] = self.inputValues.get(self.inst1, 0)
        self.outputValues[self.inst2] = self.inputValues.get(self.inst2, 0)
        self.outputValues[self.inst3] = self.inputValues.get(self.inst3, 0)
        self.outputValues[self.inst4] = self.inputValues.get(self.inst4, 0)
        self.outputValues[self.inst5] = self.inputValues.get(self.inst5, 0)
        self.outputValues[self.inst6] = self.inputValues.get(self.inst6, 0)
        self.outputValues[self.inst7] = self.inputValues.get(self.inst7, 0)
